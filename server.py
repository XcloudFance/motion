#encoding:utf-8
import socketserver
import threading
import time
import json
import pymysql
import demjson
from base64_verdant import *
from smtpmail import *
import random
from maketoken import *
err1={"id":"002"}#返回错误信息
cor1={'id':'003'}#返回正确信息
cor2={'id':'001','token':''}#这个是登录成功的专门返回值
js000={'id':'000'}
#signup = {'id':'004','username':''}
userlist = {}
usertokenlist={}
emailusrname="15906005579@139.com"
emailpassword="906005579"
checknumlist = {}
mysql = pymysql.connect(host='192.168.1.100', user='root', password='sc111', db='motion')
cursor = mysql.cursor()
class MyTCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		while True:
			sendmessage = ""
			getmessage=""
			self.data = self.request.recv(1024).strip()
			if self.client_address not in userlist:
				userlist[self.client_address]=js000
			print("{} wrote:".format(self.client_address))
			getmessage = b64decode(self.data.decode('utf-8'))
			print(getmessage)
			getjson = demjson.decode(getmessage)
			if getjson["id"] == '001':#sign in
				#It said we should get sign in message
				user = getjson["username"]
				password = getjson["password"]
				print('select * from motion where id='+user+';')#打印出mysql命令
				cursor.execute('select * from user where id='+user+';')#执行mysql
				data = list(cursor.fetchone())#列举出mysql里面的搜索结果第一条(一般也没有很多条)

				if data[2]!=password:sendmessage=b64encode(json.dumps(err1)).encode('utf-8')#self.request.send(json.dumps(err1).encode('utf-8'))
				else: sendmessage = b64encode(json.dumps(cor1)).encode('utf-8')#self.request.send(json.dumps(cor1).encode('utf-8'))
				print(data)
				self.request.send(sendmessage)#这步索性为总体发送
				continue
			if getjson["id"] == '002':
				num = ""
				for i in range(6):
					ch = chr(random.randrange(ord('0'), ord('9') + 1))
					num += ch
				checknumlist[getjson['email']] = num
				if mail(emailusrname,emailpassword,getjson["email"],'欢迎使用Motion!\n验证码为:'+num) == 0:
					sendmessage=b64encode(json.dumps(err1)).encode('utf-8')
				else:
					sendmessage=b64encode(json.dumps(cor1)).encode('utf-8')
				self.request.send(sendmessage)
				# 这步索性为总体发送，一般错误为邮箱出错,但是错误也应该是在server的邮箱问题，此步修改server密码为错误也可以间接关闭用户注册通道
			if getjson['id'] == '003':

				if getjson['checknum'] == checknumlist[getjson['email']]:
					cursor.execute('select COUNT(*) from user')#获取行数，也就是有几个人已经注册
					index=int(cursor.fetchone()[0])#获取出来的元组里面第一个就是index，(2,)元组的规定是如果只有一个元素那么必须加逗号
					str1 = 'insert into user(id,name,born,password,friendlist) values ('
					index = str(10000+index)
					str2 = '10000");'
					sendmessage = b64encode(json.dumps(cor1)).encode('utf-8')
					print((str1 + index + ',"' + getjson['name'] + '","' + getjson['born'] + '","' + getjson[
						'password'] + '","' + str2))
					cursor.execute((str1 + index + ',"' + getjson['name'] + '","' + getjson['born'] + '","' + getjson[
						'password'] + '","' + str2))
					cursor.connection.commit()
				else:
					sendmessage = b64encode(json.dumps(err1)).encode('utf-8')#连验证码都敢输错？
				self.request.send(sendmessage)  # 这步索性为总体发送

			self.request.send(b64encode(userlist[self.client_address]).encode('utf-8'))
			userlist[self.client_address]="nothing"
def test1():
	while True:
		time.sleep(0.250)
		if userlist!={}:
			userlist[list(userlist.keys())[0]] = "233"
if __name__ == "__main__":

	#t1 = threading.Thread(target=test1)
	#t1.start()
	HOST, PORT = "localhost", 9999
	server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()
	cursor.close()
	mysql.close()


# server  = socketserver.ForkingTCPServer((HOST, PORT), MyTCPHandler)