# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午1:38
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : main.py
# @Software : PyCharm
# @IDE      : PyCharm

import quequ_list
import spider
import select


Quequ = quequ_list.quequ()
Spider = spider.spider()
Select = select.select()

if __name__ == '__main__':
    urlMSG = Quequ.outputPageUrl()
    url = urlMSG[0]
    code = urlMSG[1]

    response = Spider.getHTML(url)

    urlList = Select.selectMain(response, code)

    print(urlList)
