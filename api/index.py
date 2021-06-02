# -*-coding:utf-8-*-
import requests
import json
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler


def get_data():
    news = []
    # 新建数组存放热搜榜
    top_url = 'https://s.weibo.com/top/summary/'
    # 热搜榜链接
    r = requests.get(top_url)
    # 向链接发送get请求获得页面
    soup = BeautifulSoup(r.text, 'html.parser')
    # 解析页面
    urls_titles = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a')
    hotness = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > span')

    for i in range(len(urls_titles) - 1):
        top_news = {}
        top_news['rank'] = i + 1
        # 将信息保存到字典中
        top_news['title'] = urls_titles[i + 1].get_text()
        # get_text()获得a标签的文本
        top_news['url'] = "https://s.weibo.com" + urls_titles[i]['href']
        # ['href']获得a标签的链接，并补全前缀
        top_news['hotness'] = hotness[i].get_text()
        # 获得热度文本
        news.append(top_news)
        # 字典追加到数组中

    return news


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = get_data()
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return
