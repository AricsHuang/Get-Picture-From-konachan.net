# _*_coding:utf-8_*_
# @Time     : 2020/5/2 下午4:09
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : error_record.py
# @Software : PyCharm
# @IDE      : PyCharm

'''
用于记录程序产生的错误
'''

import datetime
import time

def record(error, type, module):
    '''
    :param error: 错误代码
    :param type: 错误类型 或 错误描述
    :param module: 发生错误的模块
    :return: 返回值暂时保留
    '''
    try:
        t = time.strftime('%H:%M:%S',time.localtime(time.time()))
        date = datetime.date.today()
        f = open("log/error_"+str(date)+".dat", "a")
        f.write(str(t)+'\t'+str(type)+'  '+str(error)+'\t'+str(module)+'\n')
        f.close()
        return 0
    except Exception as e:
        pass