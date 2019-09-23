#encoding:utf-8
from flask import Flask,render_template,request,url_for,redirect
from flask import request
import socket
import json
js001 = {'id': '001', 'username': '10000', 'password': '123456'}
js002 = {'id': '002',  "email": ""}  # 这里就是注册信息了
js000 = {'id': '000'}
js003 = {'id': '003', 'password': '','checknum': '','email': "",'name': '','born': ""}
correct = {'id':'004'}
cor2= {'id':'006','user':''}
error = {'id':'005'}
client = socket.socket()
client.connect(('localhost',9999))
app = Flask(__name__,static_url_path='',template_folder='templates')
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
def ping():

	return ""


@app.route('/signin',methods=['POST','GET'])
def login():
	ping()
	print(request.method)
	if request.method=='POST':
		username = request.form.get('username')
		password = request.form.get('password')
		print (username,password)
		js001['username']=username
		js001['password']=password

		client.send(str(js001).encode('utf-8'))
		data = json.loads(client.recv(128).decode())
		print (data)
		if data['id']=='001':
			return json.dumps(correct)
		if data['id']=='002':
			return json.dumps(error)
	return ""
@app.route('/signup',methods=['POST'])
def signup():
	ping()
	username = request.form.get('username')
	password = request.form.get('password')
	email = request.form.get('email')
	code= request.form.get('code')
	born = request.form.get('born')
	print(born)
	js003['name']=username
	js003['password']=password
	js003['checknum'] = code
	js003['born'] = born
	js003['email'] = email
	client.send(str(js003).encode('utf-8'))
	data = json.loads(client.recv(128).decode())
	if data['id'] == '006':#这是正确的结果
		print(data['user'])
		cor2['user'] = data['user']
		return json.dumps(cor2)
		#return json.dumps(correct)
	if data['id'] == '003':
		return json.dumps(error)
@app.route('/')
def index():
	return render_template('login.html')
@app.route('/code',methods=['POST'])
def code():
	ping()
	mail = request.form.get('email')
	js002['email'] = mail
	client.send(str(js002).encode('utf-8'))
	data = json.loads(client.recv(128).decode())
	print(data)
	if data['id'] == '002':#这是正确的结果
		return json.dumps(error)
	if data['id'] == '003':
		return json.dumps(correct)
@app.route('/registercorrect',methods=['GET'])
def c():
	js={'id':request.args.get('id')}
	return render_template('complete.html', js=js)

app.run(host='127.0.0.1',port=6566)