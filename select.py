# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午4:37
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : select.py
# @Software : PyCharm
# @IDE      : PyCharm

import re
import error_record

class select():
    def __init__(self):
        self.selectNum = 0
        self.pictureNum = 0

    def selectMain(self, response, code):
        '''
        外部程序调用的函数
        '''
        if code == '-1':  # code=-1，代表response获取失败，不需要进行筛选了
            return 0
        elif code == '0':  # code=0，代表response是page，需要进一步筛选获取图片链接列表
            result = self.getPicList(response.text)
            return result
        elif code == '1':  # code=1，代表获取到的response是图片，需要进行保存
            self.savePic()
            return 0

    def getPicList(self, html):
        '''
        用于清洗数据，获得去重的图片链接列表
        '''
        re_url = re.compile(r'(https://konachan[.]+net/(jpeg|image).*?[.]+jpg)')
        group = re.findall(re_url, html)
        urlList = []
        group = list(set(group))
        for each in group:
            urlList.append(each[0])
        self.selectNum += 1
        return urlList

    def savePic(self, response):
        '''
        用于保存图片
        '''
        name = response.url.split("/")[-1]
        try:
            with open("picture/"+name, "wb") as picture:
                picture.write(response.content)
            self.pictureNum += 1
            return 0
        except Exception as e:
            error_record.record(e, '保存图片错误', 'select')
            return -1
