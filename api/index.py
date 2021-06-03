# -*-coding:utf-8-*-
import requests
import json
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler


def get_data():
    news = []
    top_url = 'https://s.weibo.com/top/summary/'
    r = requests.get(top_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    url = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a')
    num = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > span')
    hot = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-03')

    for i in range(1, len(url)):
        top_news = {}
        top_news['title'] = url[i].get_text()
        top_news['url'] = "https://s.weibo.com" + url[i]['href']
        top_news['num'] = num[i - 1].get_text()
        hotness = hot[i].get_text().replace('</i>', ''). \
            replace('<i class="icon-txt icon-txt-hot">', '').replace('<i class="icon-txt icon-txt-new">', '')
        top_news['hot'] = hotness
        # 去除广告链接
        if (hotness != '荐'):
            news.append(top_news)

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