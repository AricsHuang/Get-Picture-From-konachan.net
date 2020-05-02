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


Quequ = quequ_list.quequ()
Spider = spiderModule.spider()
Select = selectModule.select()

flag = []

def getPage(flag, ThreadName):
    while(not flag):
        urlMSG = Quequ.outputPageUrl()
        url = urlMSG[0]
        code = urlMSG[1]

        response = Spider.getHTML(url)

        print("[Page][Message]", ThreadName, '|', url)
        if response == -1:
            print("[Page][Warming]", ThreadName, '|', "Get html error!")
        else:
            print("[Page][Message]", ThreadName, '|', "Get a page-html.")
            urlList = Select.selectMain(response, code)

        print("[Page][Message]", ThreadName, '|', "Get a urlList.")
        inputRerutn = Quequ.inputUrl(urlList)
        inputNum = inputRerutn['inputNum']
        print("[Page][Message]", ThreadName, '|', "Input these url. >>", str(inputNum)+'/'+str(len(urlList)))

def getPicture(flag, ThreadName):
    time.sleep(10)
    while(not flag):
        urlMSG = Quequ.outputPicUrl()
        if urlMSG == -1:
            time.sleep(30)
            print("[Page][Message]", ThreadName, '|', "The Picture-url is empty.")
        else:
            url = urlMSG[0]
            code = urlMSG[1]
            print("[Page][Message]", ThreadName, '|', url)

            response = Spider.getHTML(url)

            if response == -1:
                print("[Page][Warming]", ThreadName, '|', "Get Picture error!")
            else:
                result = Select.selectMain(response, code)
                print("[Page][Message]", ThreadName, '|', "Get a Picture successful.")

def saveExit():
    Quequ.saveExit()
    Select.saveExit()
    Spider.saveExit()

if __name__ == '__main__':
    Thread_Page_1 = Thread(name="Page-1", target=getPage, args=(flag, "Page-1"))
    Thread_Picture_1 = Thread(name="Picture-1", target=getPicture, args=(flag, "Picture-1"))
    Thread_saveExit = Thread(name="saveExit", target=saveExit)

    ThreadList = [Thread_Picture_1, Thread_Page_1]

    for each in ThreadList:
        each.start()

    input_flag = input()
    flag.append(1)

    print("[Program][Message]", '|', "Wait All Thread exit.")

    for each in ThreadList:
        each.join()

    Thread_saveExit.start()
    Thread_saveExit.join()
    print("[Program][Message]", '|', "Save data successful.")

    print("Exit successful.")



