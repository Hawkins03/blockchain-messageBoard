import os
import socket
import django
import Crypto
from Crypto import PublicKey, RSA
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64decode, b64encode

import BlockChain
def generate(self):
        key = RSA.generate(2048)
        f = open(directory + 'key.pem', 'w')
        f.write(key.exportKey('PEM'))
        self.cipher = PKCS1_v1_5.new(key)

def importKey(self, key_str):
    if (not (isinstance(key_str, str))):
        return False
    keyDER = b64decode(key_str)
    self.cipher = PKCS1_v1_5.new(pubDER)
    return True

def importPubKey(self, file):
    if (not (isinstance(file, str))):
        return False
    self.pubKey = RSA.importKey(open(file).read())
    return True