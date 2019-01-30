#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Jude
import smtplib
import string
from email.mime.text import MIMEText
from email.utils import formatdate
from email.header import Header
from abyss import logger as LOG

smtpHost = 'smtp.exmail.qq.com'
sslPort = '465'
fromMail = 'abyss@jinuo.me'
username = 'abyss@jinuo.me'
password = 'dsad4@IPPs998'

encoding = 'utf-8'


def send_email(to, pipe, project_name, project_version, message, result):
    if to:
        LOG.big_log_start("Report email")
        result_str = "成功" if result else "失败"
        subject = "[{result}] {pipe}".format(result=result_str,
                                             pipe=pipe)

        body = "项目：{project_name} {project_version}  \n更新内容：{message}".format(project_name=project_name
                                                                              , project_version=project_version
                                                                              , message=message)

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
    return True
