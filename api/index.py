# -*- coding: utf-8 -*-
# @Author    : Eurkon
# @Date      : 2021/6/5 10:16

import json
import time
import requests
from http.server import BaseHTTPRequestHandler


def get_data():
    """微博热搜

    Args:
        params (dict): {}

    Returns:
        json: {title: 标题, url: 地址, num: 热度数值, hot: 热搜等级}
    """

    data = []
    t = time.time()
    timestamp = str(round(t * 10000))
    url = 'https://s.weibo.com/ajax/jsonp/gettopsug?_cb=STK_' + timestamp
    response = requests.get(url)
    # 返回js
    data_str = response.text.replace(')}catch(e){}', ''). \
        replace('try{window.STK_' + timestamp + '&STK_' + timestamp + '(', '')
    data_dict = json.loads(data_str)
    jyzy = {
        '电影': '影',
        '剧集': '剧',
        '综艺': '综',
        '音乐': '音'
    }

    for data_item in data_dict['data']['list']:
        hot = ''
        if 'flag_desc' in data_item:
            hot = jyzy.get(data_item['flag_desc'])
        if 'is_boom' in data_item:
            hot = '爆'
        if 'is_hot' in data_item:
            hot = '热'
        if 'is_boil' in data_item:
            hot = '沸'
        if 'is_new' in data_item:
            hot = '新'

        dic = {
            'title': data_item['note'],
            'url': 'https://s.weibo.com/weibo?q=' + data_item['word'].replace('#', '%23') + '&Refer=top',
            'num': data_item['num'],
            'hot': hot
        }
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
