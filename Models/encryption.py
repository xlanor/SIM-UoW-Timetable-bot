#! /usr/bin/env python3
# -*- coding: utf-8 -*-
##
# Hera encryption mod
# Thanks to stackoverflow
# Modified to place into a singular class
##
import base64, hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES


class Encrypt:
    def __init__(self, password: str, application_key: str):
        BS = 16
        self.__pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        self.__unpad = lambda s: s[0 : -s[-1]]
        self.__pw = password
        self.__encryption_key = application_key
        self.__key = hashlib.sha256(self.__encryption_key.encode("utf-8")).digest()

    def encrypt(self):
        raw = self.__pad(self.__pw).encode("utf-8")
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self):
        enc = base64.b64decode(self.__pw)
        iv = enc[:16]
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        return self.__unpad(cipher.decrypt(enc[16:])).decode("utf-8")
