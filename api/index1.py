# -*- coding: utf-8 -*-
# @Author    : Eurkon
# @Date      : 2021/6/5 10:16

import json
import requests
from http.server import BaseHTTPRequestHandler

from bs4 import BeautifulSoup


def get_data():
    """微博热搜（弃用）

    Args:
        params (dict): {}

    Returns:
        json: {title: 标题, url: 地址, num: 热度数值, hot: 热搜等级}
    """

    data = []
    url = 'https://s.weibo.com/top/summary/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}
    response = requests.get(url=url, headers=headers)
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    url = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a')
    num = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > span')
    hot = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-03')
    jyzy = {
        '电影': '影',
        '剧集': '剧',
        '综艺': '综',
        '音乐': '音'
    }

    for i in range(1, len(url)):
        # 去除广告链接
        num_string = num[i - 1].get_text().strip()
        print(url[i].get_text().strip())
        if num_string != '':
            num_split = num_string.split(' ')
            dic = {
                'title': url[i].get_text().strip(),
                'url': "https://s.weibo.com" + url[i]['href'].strip(),
                'num': num_split[len(num_split) - 1],
                'hot': hot[i].get_text().replace('<i class="icon-txt icon-txt-', '') \
                    .replace('</i>', '').replace('">', '') \
                    .replace('new', '').replace('hot', '').replace('boil', '').replace('boom', '').strip()
            }
            if len(num_split) > 1:
                dic['hot'] = jyzy[num_split[0]] if num_split[0] in jyzy.keys() else ''
            data.append(dic)

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


if __name__ == '__main__':
    print(get_data())
