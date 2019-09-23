#!/usr/bin/python3
#encoding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def mail(sender,password,receiver,text):
	try:
		msg = MIMEText(text, 'plain', 'utf-8')
		msg['From'] = 'motion robot'
		msg['To'] = receiver
		msg['Subject'] = Header('请将本邮件内的验证码输入到您的motion client中', 'utf-8')

		server = smtplib.SMTP_SSL("smtp.139.com", 465)  # 发件人邮箱中的SMTP服务器，一般端口是25
		server.login(sender, password)  # 括号中对应的是发件人邮箱账号、o邮箱密码
		server.sendmail(sender, receiver, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
		server.quit()  # 关闭连接
		return 1
	except Exception:
		return 0

