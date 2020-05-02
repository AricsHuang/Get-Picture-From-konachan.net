# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午3:26
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : mkData.py
# @Software : PyCharm
# @IDE      : PyCharm

import pickle

def askAgain():
    flag = input("[Warming]新建的文件将会覆盖原来的文件，请确认已经做好备份！！！(yes/no):\n>>>")
    while(True):
        if flag == 'yes':
            return 1
        elif flag == 'no':
            return 0
        else:
            print("[Warming]输入不合法，请重新输入：\n>>> ")
        flag = input()

def mkQuequData():
    dataDict = {'success':[], 'false':[], 'wait':[], 'waitPic':[], 'page':1}
    f = open("data/quequ.dat", 'wb')
    pickle.dump(dataDict, f)
    f.close()

def mkSelectData():
    dataDict = {'selectNum': 0, 'pictureNum': 0}
    f = open("data/select.dat", "wb")
    pickle.dump(dataDict, f)
    f.close()

def mkSpiderData():
    dataDict = {'successNum': 0, 'falseNum': 0}
    f = open("data/spider.dat", "wb")
    pickle.dump(dataDict, f)
    f.close()

if __name__ == '__main__':
    print("1. 创建空的合法队列记录")
    print("2. 创建空的合法选择器记录")
    print("3. 创建空的合法爬虫记录")
    print("==============================")
    code = input('请输入操作编号，输入 exit 退出：\n>>> ')
    while(code != 'exit'):
        flag = askAgain()
        if flag == 1:
            pass
            if code == '1':
                mkQuequData()
                print("[Message]已经成功创建初始化 data/quequ.dat ，原文件已覆盖")
            elif code == '2':
                mkSelectData()
                print("[Message]已经成功创建初始化 data/select.dat ，原文件已覆盖")
            elif code == '3':
                mkSpiderData()
                print("[Message]已经成功创建初始化 data/spider.dat ，原文件已覆盖")
            else:
                print("[Warming]找不到当前编号的操作.")
        elif flag == 0:
            print("[Message]已取消当前操作.")

        print("1. 创建空的合法队列文件")
        print("2. 创建空的合法选择器记录")
        print("3. 创建空的合法爬虫记录")
        print("==============================")
        code = input('请输入操作编号，输入 exit 退出：\n>>> ')

    print("[Message]当前程序已退出，Have a good time.Bye！")