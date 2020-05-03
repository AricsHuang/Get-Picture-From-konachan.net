# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午1:38
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : main.py
# @Software : PyCharm
# @IDE      : PyCharm

import quequ_list
import spiderModule
import selectModule
from threading import Thread
import time
import log_record
import monitor

######
## 又拍云账号信息
######
bucketName = "你的数据桶名称"
operatorName = "你的操作员名称"
password = "你的操作员密码"

######
## 邮件设置
######
sendTime = 60    # 邮件发送时间间隔（s）


Quequ = quequ_list.quequ()
Select = selectModule.select(bucketName, operatorName, password)
Spider = spiderModule.spider(Quequ)
Monitor = monitor.monitor(Quequ, Spider, Select)

flag = []

def getPage(flag, ThreadName):
    '''
    这是获取page页面的线程函数
    '''
    while(not flag):
        urlMSG = Quequ.outputPageUrl()
        url = urlMSG[0]
        code = urlMSG[1]

        response = Spider.getHTML(url)

        log_record.log_record("[Page][Message]", ThreadName, url)
        if response == -1:
            log_record.log_record("[Page][Warming]", ThreadName, "Get html error!")
        else:
            log_record.log_record("[Page][Message]", ThreadName, "Get a page-html.")
            urlList = Select.selectMain(response, code)
            log_record.log_record("[Page][Message]", ThreadName, "Get a urlList.")
            inputRerutn = Quequ.inputUrl(urlList)
            inputNum = inputRerutn['inputNum']
            log_record.log_record("[Page][Message]", ThreadName, "Input these url. >> " + str(inputNum)+'/'+str(len(urlList)))

def getPicture(flag, ThreadName):
    '''
    这是获取和保存图片的线程函数
    '''
    time.sleep(10)
    while(not flag):
        urlMSG = Quequ.outputPicUrl()
        if urlMSG == -1:
            time.sleep(30)
            log_record.log_record("[Picture][Message]", ThreadName, "The Picture-url is empty.")
        else:
            url = urlMSG[0]
            code = urlMSG[1]
            log_record.log_record("[Picture][Message]", ThreadName, url)

            response = Spider.getHTML(url)

            if response == -1:
                log_record.log_record("[Picture][Message]", ThreadName, "Get Picture error!")
            else:
                result = Select.selectMain(response, code)
                log_record.log_record("[Picture][Message]", ThreadName, "Get a Picture successful.")

def moni(sendTime, flag):
    i = 0
    while(not flag):
        if i == 10:
            Monitor.monitorMain(1)
        else:
            Monitor.monitorMain(0)
        i += 1
        time.sleep(sendTime)

def saveExit():
    '''
    这个函数在退出的时候被进程调用
    用以保存爬虫的进度
    '''
    Quequ.saveExit()
    Select.saveExit()
    Spider.saveExit()

if __name__ == '__main__':
    Thread_Page_1 = Thread(name="Page-1", target=getPage, args=(flag, "Page-1"))
    Thread_Picture_1 = Thread(name="Picture-1", target=getPicture, args=(flag, "Picture-1"))
    Thread_Monitor = Thread(name="Monitor", target=moni, args=(sendTime, flag))
    Thread_saveExit = Thread(name="saveExit", target=saveExit)

    ThreadList = [Thread_Picture_1, Thread_Page_1, Thread_Monitor]

    for each in ThreadList:
        each.start()

    input_flag = input()
    flag.append(1)

    log_record.log_record("[Program][Message]", "Program", "Wait All Thread exit.")

    for each in ThreadList:
        each.join()

    Thread_saveExit.start()
    Thread_saveExit.join()
    log_record.log_record("[Program][Message]", "Program", "Save data successful.")

    log_record.log_record("[Program][Message]", "Program", "Exit successful.")
