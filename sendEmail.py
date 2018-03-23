#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import smtplib, mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

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

    smtp = smtplib.SMTP_SSL()

    # 默认的端口为 465
    smtp.connect(smtpserver, prot)
    smtp.login(username, password)
    smtp.sendmail(From, To, msg.as_string())
    smtp.quit()

if __name__ == "__main__":
    login = {
        "smtpserver": "smtp.qq.com",
        "username": "icgw@qq.com",
        "password": "afqpioyppbytdhbi"
    }

    group = "group.txt"
    mail = {
        "emailType": "html",
        "from": None,
        "to": None,
        "subject": "邮件主题",
        "content": "内容",
        "attachment": "附件路径"
    }

    with open(group) as f:
        for line in f:
            receiver = line.rstrip('\n').split(',')
            name, email, attc = receiver[0].strip(), receiver[1].strip(), receiver[2].strip()
            mail["from"] = login["username"]
            mail["to"]   = email
            mail["content"] = name
            mail["attachment"] = attc

            sendEmail(login, mail)
            print(receiver[1], "发送成功 (Successful sending)")