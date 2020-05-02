# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午2:58
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : quequ_list.py
# @Software : PyCharm
# @IDE      : PyCharm

'''
这是一个链接队列对象
主要处理链接的储存、输入、输出、链接去重
'''

import pickle
import log_record

class quequ():
    def __init__(self):
        '''
        初始化队列
        '''
        f = open("data/quequ.dat", 'rb')
        dataDict = pickle.load(f)
        f.close()
        self.success = dataDict['success']
        self.false = dataDict['false']
        self.wait = dataDict['wait']
        self.waitPic = dataDict['waitPic']
        self.page = dataDict['page']


    def isWaitNull(self):
        '''
        判断当前Page等待队列是否为空
        如果为空就append链接
        '''
        if not self.wait:
            self.wait.append("https://konachan.net/post?page="+str(self.page)+"&tags=")
            self.page += 1


    def outputPageUrl(self):
        '''
        输出一个page链接
        '''
        self.isWaitNull()
        nowurl = self.wait.pop(0)

        while(nowurl in self.success):
            self.isWaitNull()
            nowurl = self.wait.pop(0)

        self.isWaitNull()
        return [nowurl, 0]


    def outputPicUrl(self):
        '''
        输出一个图片链接
        如果队列为空，则返回-1，让爬虫线程进入等待状态
        '''
        if self.waitPic:
            picUrl = self.waitPic.pop(0)
            return [picUrl, 1]
        else:
            return -1


    def inputUrl(self, urlList):
        '''
        通过外部程序调用，向队列中写入信息
        返回写入的链接数量
        '''
        t = 0  # 计算写入的链接数量
        for each in urlList:
            if each not in self.success:
                t +=1
                if each.endswith(".jpg"):
                    self.waitPic.append(each)
                else:
                    self.wait.append(each)
        return {'inputNum': t}


    def saveExit(self):
        '''
        用来保存当前的程序进度
        保存覆盖当前文件前，会先生成保存前的备份文件，防止出现错误后全部数据的丢失
        '''
        try:
            dataDict = {'success':self.success, 'false':self.false, 'wait':self.wait, 'waitPic':self.waitPic, 'page':self.page}
            f = open("data/quequ.dat", 'rb')
            bakDict = pickle.load(f)
            f.close()

            f = open("data/quequ.dat.last", 'wb')
            pickle.dump(bakDict, f)
            f.close()

            f = open("data/quequ.dat", 'wb')
            pickle.dump(dataDict, f)
            f.close()

            return 0
        except Exception as e:
            log_record.error_record(e, '安全退出保存数据', 'quequ')



