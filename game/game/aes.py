#!/usr/bin/python
# -*- coding: utf-8 -*-


from Crypto.Cipher import AES
from configure import enKey, RSA_PRIVATE_KEY,RSA_PUBLIC_KEY
import math
import base64

from Crypto import Random
from Crypto.Hash import MD5
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
    
def SecretSign(message):
    key = RSA.importKey(RSA_PRIVATE_KEY)
    h = MD5.new(message)
    signer = Signature_pkcs1_v1_5.new(key)
    signature = signer.sign(h)
    return base64.b64encode(signature)
    #return signature


def PublicVerify(message, signature):
    key = RSA.importKey(RSA_PUBLIC_KEY)
    h = MD5.new(message)
    verifier = Signature_pkcs1_v1_5.new(key)
    if verifier.verify(h, base64.b64decode(signature)):
        return True
    return False

def Parse_hex(hex_key):
    l = int(math.ceil(len(hex_key)/2))
    iv = ''
    for i in range(0,l):
        s = hex_key[(i*2):((i+1)*2)]
        iv = iv+chr(int(s,16))
    return iv

def AESEncrypt(password):
    encryptor = AES.new(enKey, AES.MODE_CBC,Parse_hex(enKey))
    plain_text = password * 16
    ciphertext = encryptor.encrypt(plain_text)
    encry_base64 = ciphertext.encode('base64').replace('\n','')
    return encry_base64


def AESDecrypt(encrypted_msg):
    decryptor = AES.new(enKey, AES.MODE_CBC,Parse_hex(enKey))
    plain = decryptor.decrypt(encrypted_msg.decode('base64'))
    data = plain[0:len(plain)/16]
    return data





if __name__ == "__main__":
    message = "hello"
    message = AESEncrypt(message)
    message = AESDecrypt(message)
    print message

    message = "fdsafsd"
    msg =  SecretSign(message);
    print PublicVerify(message, msg)


