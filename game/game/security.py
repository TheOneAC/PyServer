#!/usr/bin/python
# -*- coding: utf-8 -*-


import M2Crypto
from M2Crypto import *
from M2Crypto.EVP import Cipher  
from M2Crypto import m2  
from M2Crypto import util  
import configure 
#from configure import RSAPub, RSAPri
import  hashlib
import json
import base64
from base64 import b64encode, b64decode

from Crypto.Cipher import AES

ENC = 1 # 加密操作 
DEC = 0 # 解密操作 


class SecurityTools():

	rsaPub = configure.RSAPub
	rsaPri = configure.RSAPri
	aesKey = configure.enKey 
	iv ='' #'\0' * 16


  	@classmethod
	def PublicEnRSA(cls, msg):
		ctxt = cls.rsaPub.public_encrypt(msg, RSA.pkcs1_padding)
		#ctxt64 = ctxt.encode('base64')
		#print ('密文:%s'% ctxt64)
		return ctxt
	@classmethod
	def SecretDeRSA(cls, msg):
		txt = cls.rsaPri.private_decrypt(msg, RSA.pkcs1_padding)
		return txt

	@classmethod
	def SecretSign(cls, msg):

		m = EVP.MessageDigest("md5")
		m.update(msg)
		digest = m.final()
		#key_str = file('secret/private','rb').read()
		#key = RSA.load_key_string(key_str, util.no_passphrase_callback)
		key = cls.rsaPri
		result = key.sign(digest,"md5")
		return result
	@classmethod
	def PublicVerify(cls, msg,sign):
		
		m = EVP.MessageDigest("md5")
		m.update(msg)
		digest = m.final()
		#cert_str = file('secret/public','rb').read()
		#mb = BIO.MemoryBuffer(cert_str)
		#cert = RSA.load_key_bio(mb)
		cert = cls.rsaPub
		result = cert.verify(digest, sign, "md5")
		return result

	@classmethod
	def MsgSecretSign(cls, msg):
		ctxtPri = cls.rsaPri.private_encrypt(msg, RSA.pkcs1_padding)
		#ctxt64_pri = ctxtPri.encode('base64')
		#print ('密文:%s'% ctxt64_pri)
		return ctxtPri

	@classmethod
	def MsgPublicVerify(cls, msg):
		txtPri = cls.rsaPub.public_decrypt(msg, RSA.pkcs1_padding)
		#print('明文:%s'% txtPri)
		return txtPri

	@classmethod
	def AesEncrypt(cls, password):
		key = cls.aesKey
		mode = AES.MODE_CBC
		encryptor = AES.new(key, mode,key)
		plain_text = password * 16
		ciphertext = encryptor.encrypt(plain_text)
		#print ciphertext
		encry_base64 = ciphertext.encode('base64').replace('\n','')
		return encry_base64

	@classmethod
	def AesDecrypt(cls, encrypted_msg):
		key = cls.aesKey
		mode = AES.MODE_CBC
		decryptor = AES.new(key, mode,key)
		plain = decryptor.decrypt(encrypted_msg.decode('base64'))
		return plain[0:len(plain)/16]

	@classmethod
	def TestEncryption(cls, msg):
		#text = input_passwd()
		encrypted_msg = cls.AesEncrypt(msg)
		print encrypted_msg

		plain_msg = cls.AesDecrypt(encrypted_msg)
		print plain_msg



	
	@classmethod
	def AESEncrypt(cls, data):  
	  '使用aes_128_ecb算法对数据加密'  
	  cipher = Cipher(alg = 'aes_256_ecb', key = cls.aesKey, iv = cls.iv, op = ENC)  
	  txt = cipher.update(data)  
	  txt = txt + cipher.final()  
	  del cipher  
	  # 将明文从字节流转为16进制  
	  #output = ''  
	  #for i in txt:  
	  #  output += '%02X' % (ord(i))  
	  #return output  
	  return b64encode(txt)
 	@classmethod
	def AESDecrypt(cls, data):  
	  '使用aes_128_ecb算法对数据解密'  
	  # 将密文从16进制转为字节流  
	  #data = util.h2b(data) 
	  data = b64decode(data)
	  cipher = Cipher(alg = 'aes_256_ecb', key = cls.aesKey, iv = cls.iv, op = DEC)  
	  txt = cipher.update(data)  
	  txt = txt + cipher.final()  
	  del cipher  
	  return txt
	'''
	@classmethod
	def AES_build_cipher(cls, key, iv, op=ENC):
		return M2Crypto.EVP.Cipher(alg='aes_128_cbc', key=key, iv=iv, op=op)
	@classmethod
	def AESEncrypt(cls, msg):
		#Decode the key and iv
		#key = b64decode(key)
		key = cls.aesKey
		iv = cls.iv
		# Return the encryption function
		#def encrypt(data):
		cipher = cls.AES_build_cipher(key, iv, DEC)
		v = cipher.update(msg)
		v = v + cipher.final()
		del cipher
		v = b64encode(v)
			#return v
		
		#print "AES encryption successful\n"
		#return encrypt(msg)
		return v
	@classmethod
	def AESDecrypt(cls, key,msg, iv=None):
		#Decode the key and iv
		key = b64decode(key)
		if iv is None:
			iv = '\0' * 16
		else:
			iv = b64decode(iv)
		# Return the decryption function
		def decrypt(data):
			data = b64decode(data)
			cipher = cls.AES_build_cipher(key, iv, DEC)
			v = cipher.update(data)
			v = v + cipher.final()
			del cipher
			return v
		#print "AES dencryption successful\n"
		return decrypt(msg)
	''' 
       
        



	@classmethod
	def EnHash(cls, msg): 
	    hashObj=EVP.MessageDigest("md5") 
	    hashObj.update(msg) 
	    return hashObj.digest()
	
	@classmethod
	def Encrypt(cls, msg):
		aesMsg = cls.AesEncrypt(msg)
		#hashMsg = cls.EnHash(aesMsg)
		#print "sha_msg :" +sha_msg
		signMsg = cls.SecretSign(aesMsg)
		#print "sec_msg :" +sec_msg
		return aesMsg, signMsg
	@classmethod
	def LoginEncrypt(cls, userName, password):
		message = {"userName": userName, "password":base64.b64encode(cls.EnHash(password + configure.salt))}
		return cls.AESEncrypt(json.dumps(message))

	





	







if __name__ == "__main__":
	sec = SecurityTools()
	sec1 = SecurityTools()
	msg = "hello"
	aes_msg, sign_msg = sec.Encrypt(msg)
	print aes_msg
	pub_msg = sec1.PublicVerify(aes_msg,sign_msg)
	#sec_msg = sec1.EnHash(aes_msg)
	if pub_msg:
		print "Yes"
	else:
		print pub_msg
		print "No"
	en = sec1.AESEncrypt(msg*16)
	print b64encode(en)
	de = sec1.AESDecrypt(en)
	print de
	sec1.TestEncryption("hello")
