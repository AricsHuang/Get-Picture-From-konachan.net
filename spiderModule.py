# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午4:28
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : spiderModule.py.py
# @Software : PyCharm
# @IDE      : PyCharm

import requests
import log_record
import pickle

class spider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        }
        self.successNum = 0
        self.falseNum = 0

    def getHTML(self, url):
        '''
        用于获取网页html
        '''
        try:
            response = requests.get(url=url, headers=self.headers)
            response.encoding = response.apparent_encoding
            response.raise_for_status()
            self.successNum += 1
            return response
        except Exception as e:
            self.falseNum += 1
            log_record.error_record(e, "获取网页html", 'spider')  # 记录错误的发生
            return -1

    def saveExit(self):
        '''
            用来保存当前的程序进度
            保存覆盖当前文件前，会先生成保存前的备份文件，防止出现错误后全部数据的丢失
            '''
        try:
            dataDict = {'successNum': self.successNum, 'falseNum': self.falseNum}
            f = open("data/spider.dat", 'rb')
            bakDict = pickle.load(f)
            f.close()

            f = open("data/spider.dat.last", 'wb')
            pickle.dump(bakDict, f)
            f.close()

            f = open("data/spider.dat", 'wb')
            pickle.dump(dataDict, f)
            f.close()

            return 0
        except Exception as e:
            log_record.error_record(e, '安全退出保存数据', 'spider')


