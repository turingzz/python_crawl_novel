# python_crawl_novel

Python爬取网络小说

## 依赖的包

```python

pip install requests
pip install beautifulsoup4
pip install fake_useragent

```

## 使用说明

填写该部分参数，爬取小说到文件中

```python

base_url = 'https://www.example.com/novel' # 主页面url
sub_base_url_prefix = 'https://www.example.com/chapter' # 子页面url前缀,不填默认使用base_url
book_name = 'test' # 书名
chapter_links_selector = '#list dl dd a' # 文件列表的定位
chapter_name_selector = '.bookname h1' # 章节名称的定位
chapter_content_selector = '#content' # 章节内容的定位


```

