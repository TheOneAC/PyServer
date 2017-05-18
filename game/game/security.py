#!/usr/bin/python
# -*- coding: utf-8 -*-



from M2Crypto import RSA,EVP
from M2Crypto.EVP import Cipher  
from M2Crypto import m2  
from M2Crypto import util  
from configure import enKey,RSAPub, RSAPri
import  hashlib


ENCRYPT_OP = 1 # 加密操作 
DECRYPT_OP = 0 # 解密操作 


class SecurityTools():

	rasPub = RSAPub
	rasPri = RSAPri
	privateKey = enKey 
	iv = '\0' * 16 

  	@classmethod
	def PublicEnRSA(cls, msg):
		ctxt = cls.rasPub.public_encrypt(msg, RSA.pkcs1_padding)
		#ctxt64 = ctxt.encode('base64')
		#print ('密文:%s'% ctxt64)
		return ctxt
	@classmethod
	def SecretDeRSA(cls, msg):
		txt = cls.rasPri.private_decrypt(msg, RSA.pkcs1_padding)
		return txt
	@classmethod
	def SecretSign(cls, msg):
		ctxtPri = cls.rasPri.private_encrypt(msg, RSA.pkcs1_padding)
		#ctxt64_pri = ctxtPri.encode('base64')
		#print ('密文:%s'% ctxt64_pri)
		return ctxtPri

	@classmethod
	def PublicVerify(cls, msg):
		txtPri = cls.rasPub.public_decrypt(msg, RSA.pkcs1_padding)
		#print('明文:%s'% txtPri)
		return txtPri

	@classmethod
	def AESEncrypt(cls, data):  
	  '使用aes_128_ecb算法对数据加密'  
	  cipher = Cipher(alg = 'aes_128_ecb', key = cls.privateKey, iv = cls.iv, op = ENCRYPT_OP)  
	  txt = cipher.update(data)  
	  txt = txt + cipher.final()  
	  del cipher  
	  # 将明文从字节流转为16进制  
	  output = ''  
	  for i in txt:  
	    output += '%02X' % (ord(i))  
	  return output  
 	@classmethod
	def AESDecrypt(cls, data):  
	  '使用aes_128_ecb算法对数据解密'  
	  # 将密文从16进制转为字节流  
	  data = util.h2b(data)  
	  cipher = Cipher(alg = 'aes_128_ecb', key = cls.privateKey, iv = cls.iv, op = DECRYPT_OP)  
	  txt = cipher.update(data)  
	  txt = txt + cipher.final()  
	  del cipher  
	  return txt

	@classmethod
	def EnHash(cls, msg): 
	    hashObj=EVP.MessageDigest("md5") 
	    hashObj.update(msg) 
	    return hashObj.digest()

	@classmethod
	def Encrypt(cls, msg):
		aesMsg = cls.AESEncrypt(msg)
		hashMsg = cls.EnHash(aesMsg)
		#print "sha_msg :" +sha_msg
		signMsg = cls.SecretSign(hashMsg)
		#print "sec_msg :" +sec_msg
		return aesMsg, signMsg








if __name__ == "__main__":
	sec = SecurityTools()
	sec1 = SecurityTools()
	msg = "hello"
	aes_msg, sign_msg = sec.Encrypt(msg)
	pub_msg = sec1.PublicVerify(sign_msg)
	sec_msg = sec1.EnHash(aes_msg)
	if sec_msg == pub_msg:
		print "Yes"
	else:
		print pub_msg, sec_msg
		print "No"
