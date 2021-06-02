# -*-coding:utf-8-*-
import requests
import json
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler


def get_data():
    news = []
    top_url = 'https://s.weibo.com/top/summary/'
    r = requests.get(top_url)
    soup = BeautifulSoup(r.text, 'lxml')
    urls_titles = soup.select('#pl_top_realtimetop > table > tbody > tr > td.td-02 > a')
    hotness = soup.select('#pl_top_realtimetop > table > tbody > tr > td.td-02 > span')

    for i in range(len(urls_titles) - 1):
        top_news = {}
        top_news['rank'] = i + 1
        top_news['title'] = urls_titles[i + 1].get_text()
        top_news['url'] = "https://s.weibo.com" + urls_titles[i]['href']
        top_news['hotness'] = hotness[i].get_text()
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
