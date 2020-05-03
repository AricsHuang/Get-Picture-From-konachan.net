# _*_coding:utf-8_*_
# @Time     : 2020/5/3 上午10:19
# @Author   : Arics
# @Email    : 739386753@qq.com
# @File     : monitor.py
# @Software : PyCharm
# @IDE      : PyCharm

from email.mime.text import MIMEText
import smtplib
import datetime
import log_record

class monitor():
    def __init__(self, _quequ, _spider, _select):
        self.sendMailNum = 0                                        # 发送邮件的数量
        self._qu = _quequ                                           # 队列对象
        self._sp = _spider                                          # 爬虫对象
        self._se = _select                                          # 选择器对象

        date = datetime.date.today()
        f = open("log/error/error_" + str(date) + ".dat", "a")
        f.close()
        f = open("log/error/error_" + str(date) + ".dat", "r")
        errors = f.readlines()
        f.close()

        self.begin_ErrorNum = len(errors)                           # 初始错误数量
        self.begin_quequSuccessNum = len(self._qu.success)          # 初始成功队列数量
        self.begin_quequFalseNum = len(self._qu.false)              # 初始失败队列数量
        self.begin_PictureNum = _select.pictureNum                  # 初始选择器图片数量
        self.AllList = []


    def sendMail(self, mailMSG, theme):
        '''
        这是一个邮件发送程序
        通过qq邮箱（也可以通过别的）
        '''
        msg = MIMEText(mailMSG)
        msg['Subject'] = theme                      # 邮件主题
        msg['From'] = 'konachan.net 【爬虫回报】'     # 发件人
        msg['To'] = 'admin'                         # 收信人
        from_addr = "发件邮箱地址"              # 发件地址
        password = "你的邮箱授权码"               # 邮箱授权码
        smtp_server = 'smtp.qq.com'                 # 发件服务器
        to_addr_list = ['收件邮箱地址', '收件邮箱地址']         # 收件地址，可以填写多个

        for to_addr in to_addr_list:
            exit_flag = 0
            for i in range(3):
                try:
                    server = smtplib.SMTP_SSL(smtp_server, 465, timeout=2)
                    server.login(from_addr, password)

                    server.sendmail(from_addr, [to_addr], msg.as_string())
                    server.quit()
                    exit_flag = 1
                    log_record.log_record("[Mail][Message]", "Send-Mail", "发送邮件成功 >>> "+str(i+1)+'/3')
                except Exception as e:
                    log_record.error_record(e, '发送邮件发生错误 >>> '+str(i+1)+'/3', 'Send-Mail')
                if exit_flag == 1:
                    break

    def writeMail(self, quequ_success_add, quequ_success_now, quequ_false_add, quequ_false_now, Error_v, Picture_v, Picture_totalNum):
        '''
        这个函数对邮件进行编写
        '''
        nowTime = datetime.date.today()
        f = open("data/Mail.txt", 'w')
        f.write("目前已发送邮件:				" + str(self.sendMailNum) + "\n")
        f.write("回报统计时间:				" + str(nowTime) + "\n")
        f.write("=====================================\n")
        f.write("\n")
        f.write("================QUEQU================\n")
        f.write("成功队列数量:			" + str(quequ_success_now) + '(+' + str(quequ_success_add) + ')\n')
        f.write("失败队列数量:			" + str(quequ_false_now) + '(+' + str(quequ_false_add) + ')\n')
        f.write("=====================================\n")
        f.write("\n")
        f.write("================SPIDER===============\n")
        f.write("近十分钟的错误速度:			" + str(Error_v) + '/min\n')
        f.write("=====================================\n")
        f.write("\n")
        f.write("================SELECT===============\n")
        f.write("图片保存速度:			" + str(Picture_v) + '/min\n')
        f.write("图片总计:				" + str(Picture_totalNum) + '\n')
        f.write("=====================================")

    def monitorMain(self, sendflag):
        '''
        用以监控数据的变化
        '''
        date = datetime.date.today()

        quequ_success_now = len(self._qu.success)
        quequ_success_add = quequ_success_now-self.begin_quequSuccessNum

        quequ_false_now = len(self._qu.false)
        quequ_false_add = quequ_false_now-self.begin_quequFalseNum

        f = open("log/error/error_" + str(date) + ".dat", "r")
        errors = f.readlines()
        f.close()

        '''目前的错误数量'''
        now_ErrorNum = len(errors)
        '''近十分钟内错误产生速度'''
        Error_v = (now_ErrorNum-self.begin_ErrorNum)/10

        now_PictureNum = self._se.pictureNum
        Picture_v = (now_PictureNum-self.begin_PictureNum)/10

        '''调用函数写邮件'''
        self.writeMail(quequ_success_add, quequ_success_now, quequ_false_add, quequ_false_now, Error_v, Picture_v, now_PictureNum)

        with open('data/Mail.txt', 'r') as f:
            msg = f.read()

        '''发送邮件的条件'''
        if Error_v >= 5:
        # if True:
            self.sendMail(msg, '错误数量超预期')
            self.sendMailNum += 1

        if sendflag == 1:
            aimsList = self.AllList.pop(0)
            self.begin_ErrorNum = aimsList[0]
            self.begin_quequSuccessNum = aimsList[1]
            self.begin_quequFalseNum = aimsList[2]
            self.begin_PictureNum = aimsList[3]
        else:
            pass

        tempList = [now_ErrorNum, quequ_success_now, quequ_false_now, now_PictureNum]
        self.AllList.append(tempList)
