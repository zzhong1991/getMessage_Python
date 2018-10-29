# -*- coding:utf-8 -*-

import smtplib,xlsxwriter,os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.application import MIMEApplication

def Email(filename,sender,mypass,receiver,keyword):
    # table_name是我生成文件时(忽略)的命名，这里解释下
    name = filename
    # 第二步发送文件
    sender = sender  # 发件人邮箱账号
    my_pass = mypass  # 发件人授权码
    receiver = receiver  # 收件人邮箱账号，我这边发送给自己
    def mail():
        ret = True
        try:
            msg = MIMEMultipart()
            msg['From'] = formataddr([sender, sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr([receiver, receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = keyword  # 邮件的主题，也可以说是标题
            filepath = name  # 绝对路径
            xlsxpart = MIMEApplication(open(filepath, 'rb').read())
            basename = filename
            xlsxpart.add_header('Content-Disposition', 'attachment',
                                filename=('gbk', '', basename))  # 注意：此处basename要转换为gbk编码，否则中文会有乱码。
            msg.attach(xlsxpart)
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
            server.sendmail(sender, receiver, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            # os.remove(filepath)  # 删除文件
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(e)
            ret = False
        return ret
    ret = mail()
    return ret