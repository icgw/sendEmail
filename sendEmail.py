#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import smtplib, mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# 使用 ssl 加密连接时的端口 465 或 994
def sendEmail(login = None, mail = None, port = 465):
    smtpserver = login["smtpserver"]
    username   = login["username"]
    password   = login["password"]

    EmailType  = mail["emailType"]
    From       = mail["from"]
    To         = mail["to"]
    Subject    = mail["subject"]
    Content    = mail["content"]
    Attachment = mail["attachment"]

    msg = MIMEMultipart()
    msg["Subject"] = Subject
    msg["From"]    = From
    msg["To"]      = To

    text = MIMEText(Content, EmailType, "utf-8")
    msg.attach(text)
    part = MIMEApplication(open(Attachment, "rb").read())
    part.add_header("Content-Disposition", "attachment", filename = Attachment.split("/")[-1])
    msg.attach(part)

    try:
        smtp = smtplib.SMTP_SSL()

        # 默认的端口为 465
        smtp.connect(smtpserver, port)
        smtp.login(username, password)
        smtp.sendmail(From, To, msg.as_string())
        print(To + "\t 邮件发送成功 (Sent successfully)")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    smtp.quit()

if __name__ == "__main__":
    login = {}

    # 在这里设置 SMTP 服务器地址
    login["smtpserver"] = "mail.cstnet.cn"
    login["username"]   = input("请输入登陆邮箱地址：")
    login["password"]   = input("请输入密码：")

    group     = "group.txt"
    content   = "content.txt"
    attachDir = "./attachment/"
    
    text = open(content).read()
    mail = {
        "emailType": "html",
        "from": None,
        "to": None,
        
        # 在这里设置统一的邮件主题
        "subject": "关于核对完善国科大院士指导教师信息的通知",
        "content": None,
        "attachment": None
    }

    with open(group) as f:
        for line in f:
            receiver = line.rstrip('\n').split(',')
            name, email, attc = receiver[0].strip(), receiver[1].strip(), receiver[2].strip()
            mail["from"] = login["username"]
            mail["to"]   = email
            cnt = text.replace("$name$", name)
            cnt = cnt.replace("$email$", "icgw@outlook.com")
            mail["content"] = cnt
            mail["attachment"] = attachDir + attc
            
            # 这里默认的端口 465，可以在第三个参数上自定义
            sendEmail(login, mail)