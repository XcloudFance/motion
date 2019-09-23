# -*- coding:utf-8 -*-
#客户端
#encoding:utf-8
import socket
import time
import json
import threading
from base64_verdant import *
client = socket.socket() #定义协议类型,相当于生命socket类型,同时生成socket连接对象
client.connect(('localhost',9999))
js001 = {'id': '001', 'username': '10000', 'password': '123456'}
js002 = {'id': '002',  "email": ""}  # 这里就是注册信息了
js000 = {'id': '000'}
js003 = {'id': '003', 'password': '','checknum': '','email': "",'name': '','born': ""}

message = ""
willsend_message = []#反正用户不能发送空白信息
def t1():
	#{'id': '003', 'password': '123456','checknum': '197760','email': "15906005579@139.com",'name': 'add','born': "2019-01-01"}
	#js002['email']='15906005579@139.com'{'id': '003', 'password': '123456','checknum': '197760','email': "15906005579@139.com",'name': 'add','born': "2019-01-01"}
	#js003['password']='123456'
	#js003['checknum']=''{'id': '002',  "email": "15906005579@139.com"}
	global message,willsend_message
	tmplen=0
	while True:
		#if tmplen == 3: message = js002
		if willsend_message == [] :
			message=js000
		else :
			message = willsend_message.pop()
		time.sleep(0.250)
		sendmessage = b64encode(str(message)).encode("utf-8")
		client.send(sendmessage)
		data = client.recv(1024)
		getmessage = b64decode(data.decode())
		if message!=js000:
			print(message)
		if getmessage!='nothing':
			print("recv:>", getmessage)
		#message=""
		tmplen+=1

	client.close()
def interface():
	global willsend_message
	while True:
		inputText = input(">>>")
		willsend_message .insert(0,inputText)
threading.Thread(target=interface).start()
threading.Thread(target=t1).start()

