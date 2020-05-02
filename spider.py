# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午4:28
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : spider.py.py
# @Software : PyCharm
# @IDE      : PyCharm

import requests
import error_record

class spider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        }

    def getHTML(self, url):
        '''
        用于获取网页html
        '''
        try:
            response = requests.get(url=url, headers=self.headers)
            response.encoding = r.apparent_encoding
            response.raise_for_status()
            return response
        except Exception as e:
            error_record.record(e, "获取网页html", 'spider')  # 记录错误的发生
            return -1

