# -*- coding: utf-8 -*-
# @Author    : Eurkon
# @Date      : 2021/6/5 10:16

import json
import requests
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler


def get_data():
    """微博热搜

    Args:
        params (dict): {}

    Returns:
        json: {title: 标题, url: 地址, num: 热度数值, hot: 热搜等级}
    """

    data = []
    response = requests.get('https://s.weibo.com/top/summary/')
    soup = BeautifulSoup(response.text, 'html.parser')
    url = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a')
    num = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > span')
    hot = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-03')

    for i in range(1, len(url)):
        news = {
            'title': url[i].get_text(),
            'url': "https://s.weibo.com" + url[i]['href'],
            'num': num[i - 1].get_text()
        }
        hotness = hot[i].get_text().replace('</i>', ''). \
            replace('<i class="icon-txt icon-txt-hot">', '').replace('<i class="icon-txt icon-txt-new">', '')
        news['hot'] = hotness
        # 去除广告链接
        if hotness != '荐' and hotness != '商':
            data.append(news)

    return data


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