# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午4:37
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : selectModule.py
# @Software : PyCharm
# @IDE      : PyCharm

import re
import log_record
import pickle
import upyun

class select():
    def __init__(self, bucketName, operatorName, password):
        f = open("data/select.dat", "rb")
        dataDict = pickle.load(f)
        f.close()
        self.selectNum = dataDict['selectNum']
        self.pictureNum = dataDict['pictureNum']
        self.up = upyun.UpYun(bucketName, operatorName, password)

    def selectMain(self, response, code):
        '''
        外部程序调用的函数
        '''
        self.selectNum += 1
        if code == -1:  # code=-1，代表response获取失败，不需要进行筛选了
            return 0
        elif code == 0:  # code=0，代表response是page，需要进一步筛选获取图片链接列表
            result = self.getPicList(response.text)
            return result
        elif code == 1:  # code=1，代表获取到的response是图片，需要进行保存
            self.upyunSave(response)
            self.pictureNum += 1
            return 0

    def getPicList(self, html):
        '''
        用于清洗数据，获得去重的图片链接列表
        '''
        re_url = re.compile(r'(https://konachan[.]+net/(jpeg|image).*?[.]+jpg)')
        group = re.findall(re_url, html)
        # print("####")
        # print("##", group)
        # print("####")
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
            log_record.error_record(e, '保存图片错误', 'select')
            return -1

    def saveExit(self):
        '''
            用来保存当前的程序进度
            保存覆盖当前文件前，会先生成保存前的备份文件，防止出现错误后全部数据的丢失
            '''
        try:
            dataDict = {'selectNum': self.selectNum, 'pictureNum': self.pictureNum}
            f = open("data/select.dat", 'rb')
            bakDict = pickle.load(f)
            f.close()

            f = open("data/select.dat.last", 'wb')
            pickle.dump(bakDict, f)
            f.close()

            f = open("data/select.dat", 'wb')
            pickle.dump(dataDict, f)
            f.close()

            return 0
        except Exception as e:
            log_record.error_record(e, '安全退出保存数据', 'select')

    def upyunSave(self, response):
        '''
        直接保存到 又拍云OSS 数据桶
        如果又拍云保存出现错误，就先暂存本地
        '''
        result = response.content
        filename = response.url.split('/')[-1]
        self.flag = 0
        try:
            res = self.up.put('/'+filename, result, checksum=True, timeout=120)
            log_record.log_record("[UpYun][Message]", 'UpYun', str(res))
            return 1
        except Exception as e:
            log_record.error_record(e, '又拍云上传图片', 'select-upyun')
            self.flag = 1

        if self.flag == 1:
            try:
                with open('picture/'+filename, 'wb') as tempfile:
                    tempfile.write(result)
                self.flag = 0
                log_record.log_record("[UpYun][Message]", '本地保存', filename)
                return 0
            except Exception as e:
                log_record.error_record(e, '本地保存图片', 'select-upyun')
                self.flag = 0
                return 0