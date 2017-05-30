#!/usr/bin/python
# -*- coding: utf-8 -*-
import configure
import hashlib
import json
import math
import base64

import M2Crypto
from M2Crypto import *
from M2Crypto.EVP import Cipher  
from M2Crypto import m2  
from M2Crypto import util 

ENC = 1 # 加密操作
DEC = 0 # 解密操作

class SecurityTools():

    #辅助类的类成员
    rsaPub = RSA.load_pub_key(configure.publicKey)
    rsaPri = RSA.load_key(configure.privateKey)
    aesKey = configure.enKey  #aes

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
    def Sign(cls, msg):
        m = EVP.MessageDigest("md5")
        m.update(msg)
        digest = m.final()
        key = cls.rsaPri
        result = key.sign(digest,"md5")
        return result
        
    @classmethod
    def Verify(cls, msg, sign):
        m = EVP.MessageDigest("md5")
        m.update(msg)
        digest = m.final()
        cert = cls.rsaPub
        result = cert.verify(digest, sign, "md5")
        return result

    @classmethod
    def __ParseHex(cls, hex_key):
        l = int(math.ceil(len(hex_key)/2))
        iv = ''
        for i in range(0,l):
            s = hex_key[(i*2):((i+1)*2)]
            iv = iv+chr(int(s,16))
        return iv

    @classmethod
    def AESEncrypt(cls, plain):
        #encryptor = AES.new(cls.aesKey, AES.MODE_ECB, cls.__ParseHex(cls.aesKey))
        ##if fs is a multiple of 16
        #x = len(plain) % 16
        #if x != 0:
        #    plain = plain + '0'*(16 - x) #It shoud be 16-x not
        #ciphertext = encryptor.encrypt(plain)
        #encry_base64 = ciphertext.encode('base64').replace("\n", '')
        #return encry_base64
        cipher = Cipher(alg = 'aes_128_ecb', key = cls.aesKey, iv = cls.aesKey, op = ENC, padding = 0)  
        x = len(plain) % 16
        if x != 0:
            plain = plain + '0'*(16 - x)
        txt = cipher.update(plain)
        txt = txt + cipher.final()
        del cipher  
        return base64.b64encode(txt)

    @classmethod
    def AESDecrypt(cls, encrypted_msg):
        #decryptor = AES.new(aesKey, AES.MODE_ECB, cls.__ParseHex(cls.aesKey))
        #plain = decryptor.decrypt(encrypted_msg.decode('base64'))
        #data = plain[0:len(plain)/16]
        #return data
        pass
    
    @classmethod
    def Encrypt(cls, msg):
        aesMsg = cls.AESEncrypt(msg)
        #hashMsg = cls.EnHash(aesMsg)
        #print "sha_msg :" +sha_msg
        signMsg = cls.Sign(aesMsg)
        #print "sec_msg :" +sec_msg
        return base64.b64encode(aesMsg), base64.b64encode(signMsg)

    





    







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
    en = sec1.AESEncrypt(msg * 16)
    print b64encode(en)
    de = sec1.AESDecrypt(en)
    print de
    sec1.TestEncryption("hello")
