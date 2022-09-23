import json
import Crypto
import requests
from time import time
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import BlockChain

print("Start!")

blockChain1 = BlockChain.BlockChain()
blockChain2 = BlockChain.BlockChain()



blockChain1.new_block("Block 1!")

print(f"{blockChain2.validChain(blockChain1.getChain())}")