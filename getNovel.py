import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from threading import Thread
import time
import random

base_url = 'https://www.example.com/novel' # 主页面url
sub_base_url_prefix = 'https://www.example.com/chapter' # 子页面url前缀,不填默认使用base_url
book_name = 'test' # 书名
chapter_links_selector = '#list dl dd a' # 文件列表的定位
chapter_name_selector = '.bookname h1' # 章节名称的定位
chapter_content_selector = '#content' # 章节内容的定位

chapter_count = 0  # 记录已经爬取的章节数量。通过该变量控制从第几个链接开始爬取，从0开始。
write_type = 'a' # 文件读写模式。写入模式（'w'），追加模式（'a'）
num_threads = 1  # 设置线程数量。多线程执行中途有错误则最后的文件会缺失部分章节，且对服务器压力较大，容易被封禁IP。
chapter_links = []  # 存储所有章节链接
chapter_contents = []  # 存储每个章节中内容



# 获取所有章节链接
def get_chapter_links():
    global chapter_links, chapter_contents, sub_base_url_prefix
    if sub_base_url_prefix == '':
        sub_base_url_prefix = base_url
    print('crawl ' + base_url)
    header = {'User-Agent': UserAgent().random}
    response = requests.get(base_url, headers = header)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.select(chapter_links_selector)
    # 拼接章节链接的方式
    chapter_links = [sub_base_url_prefix + link['href'] for link in content]
    chapter_contents = [''] * len(chapter_links)
    print('chapter number: ' + str(len(chapter_links)))


# 爬取章节内容的线程函数
def crawl_chapter_content(thread_id):
    global chapter_count, chapter_contents
    while chapter_count < len(chapter_links):
        index = chapter_count
        chapter_count += 1
        if index % num_threads != thread_id:
            continue
        chapter_link = chapter_links[index]
        print('crawling ' + str( index + 1 ) + ' url ' + chapter_link)
        header = {'User-Agent': UserAgent().random}
        response = requests.get(chapter_link, headers = header)
        soup = BeautifulSoup(response.text.encode(response.encoding), 'html.parser')
        # soup = BeautifulSoup(response.text, 'html.parser')
        chapter_name = soup.select(chapter_name_selector)[0]
        content = soup.select(chapter_content_selector)[0]
        content_all = chapter_name.text.strip() + content.text.strip()
        # 爬取章节名称 + 章节内容
        chapter_contents[index] = content_all
        # 随机睡眠。减轻对服务器的压力；防止被封禁
        time.sleep(3)


# 创建并启动所有线程
def start_threads():
    threads = []
    for i in range(num_threads):
        thread = Thread(target=crawl_chapter_content, args=(i,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


# 将所有章节内容拼接并写入文件
def write_to_file():
    with open(book_name + '.txt' , write_type, encoding='utf-8') as f:
        f.write('\n\n'.join(chapter_contents))


if __name__ == '__main__':
    try:
        get_chapter_links()
        start_threads()
    except IndexError:
        print('error')
    finally:
        # 写入内容
        write_to_file()
    print('done')