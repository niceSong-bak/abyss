#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Jude
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.header import Header
from abyss import logger as LOG

smtpHost = 'smtp.exmail.qq.com'
sslPort = '465'
fromMail = 'ci@jinuo.me'
username = 'ci@jinuo.me'
password = 'x1Nbm6wx'

encoding = 'utf-8'


def send_email(to, project_name, project_version, message, result):
    if to:
        LOG.big_log_start("Start send email")
        if result:
            subject = '[编译成功] ' + project_name + ' ' + project_version
        else:
            subject = '[编译失败] ' + project_name + ' ' + project_version

        body = '更新内容: ' + message

        mail = MIMEText(body.encode(encoding), 'plain', encoding)
        mail['Subject'] = Header(subject, encoding)
        mail['From'] = fromMail
        mail['To'] = ', '.join(to)
        mail['Date'] = formatdate()

        smtp = smtplib.SMTP_SSL(smtpHost, sslPort)
        smtp.ehlo()
        smtp.login(username, password)

        # 发送邮件
        smtp.sendmail(fromMail, to, mail.as_string())
        smtp.close()
        LOG.big_log_end("Email Send Successful")
    else:
        LOG.big_log_end("No address to send email")
    return True
