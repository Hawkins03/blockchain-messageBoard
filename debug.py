import json
import Crypto
import requests
from time import time
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from base64 import b64decode, b64encode
import BlockChain

message = "Hello World"
key = RSA.generate(2048)
cipher = pkcs1_15.PKCS115_SigScheme(key)
signature_output = b64encode(cipher.sign(SHA256.new(message.encode('utf-8')))).decode('ascii')

str_pubKey = key.public_key().export_key().decode('utf-8')
pubkey = RSA.import_key(str_pubKey)
cipher2 = pkcs1_15.PKCS115_SigScheme(pubkey)
try:
    hash_sig = cipher2.verify(SHA256.new(message.encode('utf-8')), b64decode(signature_output.encode('ascii')))
    print("successfull!")
except ValueError:
    print("ERROR! signature does not match!")
print(hash_sig == None)


blockChain1 = BlockChain.BlockChain()
blockChain2 = BlockChain.BlockChain()

blockChain1.new_block("Hallo Friend!!")
blockChain2.new_block("Hello Fellow Friend!")

print(f"{blockChain2.validChain(blockChain1.chain)}")
print(f"{blockChain1.validChain(blockChain2.chain)}")