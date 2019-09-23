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
cor3={'id':'006','user':''}#注册成功后会返回id
js000={'id':'000'}#无意义
err2={'id':'004'}#timestamp产生的错误，因为timestamp过期
js007 = {'id':'007','name':'','sex':'','born':''}
emailusrname="username"
emailpassword="password"
checknumlist = {}
mysql = pymysql.connect(host='ip',port=63791, user='root', password='Password', db='motion')
cursor = mysql.cursor()
timelimit = 24 #24小时
def candy(text):#一个语法糖，目的是将要发送的json转换成utf-8字符串
	return json.dumps(text).encode('utf-8')
class MyTCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		while True:
			sendmessage = ""
			getmessage=""
			self.data = self.request.recv(1024).strip()
			mysql.ping(reconnect=True)
			print("{} wrote:".format(self.client_address))
			getmessage = self.data.decode('utf-8')
			print(getmessage)
			getjson = demjson.decode(getmessage)
			#这个js000是针对测试服务器是否可以连接的
			if getjson['id'] == '000':
				self.request.send(candy(js000))

			if getjson["id"] == '001':#sign in
				#It said we should get sign in message
				user = getjson["username"]
				password = getjson["password"]
				print('select id,name,password from motion where id='+user+';')#打印出mysql命令
				cursor.execute('select * from user where id='+user+';')#执行mysql

				data = cursor.fetchone()#列举出mysql里面的搜索结果第一条(一般也没有很多条)
				print(data)
				if data == None:
					sendmessage = json.dumps(err1).encode('utf-8')
					self.request.send(sendmessage)
					continue
				else:
					data=list(data)
				if data[2]!=password:
					sendmessage=json.dumps(err1).encode('utf-8')#self.request.send(json.dumps(err1).encode('utf-8'))
				else:
					cor2['token'] = mktoken()
					timestamp = gettimestamp()
					cursor.execute('update user set token = "'+cor2['token']+'", timestamp = "'+timestamp+'" where id = '+getjson['username'])
					cursor.connection.commit()
					sendmessage = json.dumps(cor2).encode('utf-8')#self.request.send(json.dumps(cor1).encode('utf-8'))
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
					sendmessage=json.dumps(err1).encode('utf-8')
				else:
					sendmessage=json.dumps(cor1).encode('utf-8')
				self.request.send(sendmessage)
				# 这步索性为总体发送，一般错误为邮箱出错,但是错误也应该是在server的邮箱问题
				#此步修改server密码为错误也可以间接关闭用户注册通道

			if getjson['id'] == '003':

				if getjson['checknum'] == checknumlist[getjson['email']]:
					cursor.execute('select COUNT(*) from user')#获取行数，也就是有几个人已经注册
					index=int(cursor.fetchone()[0])#获取出来的元组里面第一个就是index，(2,)元组的规定是如果只有一个元素那么必须加逗号
					str1 = 'insert into user(id,name,born,password,email,friendlist,sex) values ('
					index = str(10000+index)
					print(index)
					str2 = '10000",0);'
					cor3['user'] = index
					sendmessage = json.dumps(cor3).encode('utf-8')
					print(getjson['password'])
					cursor.execute(str1 + index + ',"' + getjson['name'] + '","' + getjson['born'] + '","' + getjson[
						'password'] + '","' +getjson['email'] +'","'+str2)
					cursor.connection.commit()
					checknumlist[getjson['email']] = '' #防止有人恶意批量注册
				else:
					sendmessage = candy(err1)#连验证码都敢输错？

				self.request.send(sendmessage)  # 这步索性为总体发送

			if getjson['id'] == '004':#这里004为验证token的timestamp有没有过期
				cursor.execute('select token,timestamp from user where id = '+getjson['username'])
				data = cursor.fetchone()
				minus = gettimestamp() - data[1] #算出时间戳的差值
				minus = int(minus / 60 / 60)#直接转换成hour
				if data[1] != getjson['token']:
					self.request.send(candy(err1))
				elif(minus>timelimit):
					self.request.send(candy(err2))
				else:
					self.request.send(candy(cor1))
			#查询分多种
			#第一种为005,005则是单纯获取一个人的name或者性别，年龄等等单纯的内容
			#第二种为006，就是批量获取此人信息

			if getjson['id'] == '005':#这里为请求一些必要的内容，例如name，为了保证数据安全性将会特判来限制可查询内容
				ret = {'id':'005','ret':''}
				if getjson['content'] == 'name':
					cursor.execute('select name from user where id = '+getjson['username'])
					ret['ret'] = cursor.fetchone()[0]
				if getjson['content'] == 'sex':
					cursor.execute('select sex from user where id = ' + getjson['username'])
					ret['ret'] = cursor.fetchone()[0]
				if getjson['content'] == 'born':
					cursor.execute('select born from user where id = ' + getjson['username'])
					ret['ret'] = cursor.fetchone()[0]
				self.request.send(candy(ret))
			#这是一个庞大的项目:授权登录
			if getjson['id'] == '006':
				ret = js007
			if getjson['id'] == '007': #判断token是否过期
				token = getjson['token']

			if getjson['id'] == '198':
				print('授权接入！')
				appid = getjson['appid']



			#self.request.send(js000.encode('utf-8'))
if __name__ == "__main__":
	HOST, PORT = "localhost", 9999
	print('Get to ',HOST,PORT)
	server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()
	cursor.close()
	mysql.close()
