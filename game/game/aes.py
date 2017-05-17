#!/usr/bin/python
# -*- coding: utf-8 -*-


from Crypto.Cipher import AES
from configure import EN_KEY, RSA_PRIVATE_KEY,RSA_PUBLIC_KEY
import  math
import base64

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

def EnRSA(message):
	message =  Encrypt(message)
	key = RSA_PUBLIC_KEY
	rsakey = RSA.importKey(key)
	cipher = Cipher_pkcs1_v1_5.new(rsakey)
	cipher_text = base64.b64encode(cipher.encrypt(message))

	rsakey = RSA.importKey(key)
	signer = Signature_pkcs1_v1_5.new(rsakey)
	digest = SHA.new()
	digest.update(message)
	sign = signer.sign(digest)
	signature = base64.b64encode(sign)

	return signature


def DeRSA(message):
	key =  RSA_PRIVATE_KEY
	rsakey = RSA.importKey(key)
	cipher = Cipher_pkcs1_v1_5.new(rsakey)
	text = cipher.decrypt(base64.b64decode(message), Random.new().read)
	
	erifier = Signature_pkcs1_v1_5.new(rsakey)
	digest = SHA.new()
	# Assumes the data is base64 encoded to begin with
	digest.update(message)
	is_verify = signer.verify(digest, base64.b64decode(signature))

	is_verify = Decrypt(is_verify)
	return is_verify


def Parse_hex(hex_key):
    l = int(math.ceil(len(hex_key)/2))
    iv = ''
    for i in range(0,l):
        s = hex_key[(i*2):((i+1)*2)]
        iv = iv+chr(int(s,16))
    return iv

def Encrypt(password):
    encryptor = AES.new(EN_KEY, AES.MODE_CBC,Parse_hex(EN_KEY))
    plain_text = password * 16
    ciphertext = encryptor.encrypt(plain_text)
    encry_base64 = ciphertext.encode('base64').replace('\n','')
    return encry_base64


def Decrypt(encrypted_msg):
    decryptor = AES.new(EN_KEY, AES.MODE_CBC,Parse_hex(EN_KEY))
    plain = decryptor.decrypt(encrypted_msg.decode('base64'))
    data = plain[0:len(plain)/16]
    return data



if __name__ == "__main__":
	message = "hello"
	message = Encrypt(message)
	message = Decrypt(message)
	print message


