
#encoding:utf-8
import base64
def b64decode(text):
	base64_verdant = ""
	try:
		str_decrypt = text
		base64_decrypt = base64.b64decode(str_decrypt.encode('utf-8'))
		#print("BASE64解密串（UTF-8）:\n", str(base64_decrypt, 'utf-8'))
		return  str(base64_decrypt, 'utf-8')
	except Exception as e:
		print("BASE64解密串（UTF-8）异常:", e)
		#print("BASE64解密串（默认字符集）:\n", str(base64_decrypt))
		base64_decrypt = ""
def b64encode(text):
	str_encrypt = text
	base64_encrypt = base64.b64encode(str_encrypt.encode('utf-8'))
	#print("BASE64加密串:\n" + str(base64_encrypt, 'utf-8'))
	return  str(base64_encrypt, 'utf-8')
if __name__ == '__main__':
	b64 = base64_verdant()
	print(b64.b64encode('233'))
	print(type(b64.b64decode('MjMz')))