#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:zhuchenxi
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.header import Header

smtpHost = 'smtp.exmail.qq.com'
sslPort = '465'
fromMail = 'ci@jinuo.me'
username = 'ci@jinuo.me'
password = 'x1Nbm6wx'

encoding = 'utf-8'


def notify(to, project_name, project_version):
    if to:
        try:
            subject = project_name + ' ' + project_version + ' 编译完毕'
            body = project_name + ' ' + project_version + ' 在正式环境编译完毕, 已上传到镜像仓库'

            mail = MIMEText(body.encode(encoding), 'plain', encoding)
            mail['Subject'] = Header(subject, encoding)
            mail['From'] = fromMail
            mail['To'] = to
            mail['Date'] = formatdate()

            smtp = smtplib.SMTP_SSL(smtpHost, sslPort)
            smtp.ehlo()
            smtp.login(username, password)

            # 发送邮件
            smtp.sendmail(fromMail, to, mail.as_string())
            smtp.close()
            return True
        except Exception as e:
            return False
    return False
