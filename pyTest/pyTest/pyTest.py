#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import json
import math
import base64

import M2Crypto
from M2Crypto import *
from M2Crypto.EVP import Cipher  
from M2Crypto import m2  
from M2Crypto import util 

def AESEncrypt(plain):
    #encryptor = AES.new(cls.aesKey, AES.MODE_ECB, cls.__ParseHex(cls.aesKey))
    ##if fs is a multiple of 16
    #x = len(plain) % 16
    #if x != 0:
    #    plain = plain + '0'*(16 - x) #It shoud be 16-x not
    #ciphertext = encryptor.encrypt(plain)
    #encry_base64 = ciphertext.encode('base64').replace("\n", '')
    #return encry_base64

    cipher = Cipher(alg = 'aes_128_ecb', key = "68b329da9893e340", iv = "68b329da9893e340", op = 1, padding = 0)
    x = len(plain) % 16
    if x != 0:
        plain = plain + '\0' * (16 - x)
    txt = cipher.update(plain)
    txt = txt + cipher.final()
    del cipher
    return txt


print base64.b64encode(AESEncrypt("hello"));