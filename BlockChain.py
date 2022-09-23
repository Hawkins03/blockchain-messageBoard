import os
import socket
import json
import Crypto
from time import time
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

'''
note, quite a bit of this class took inspiration from https://github.com/dvf/blockchain/
(This class does use most of the protocols, however it encodes messages instead of transactions, and signs the hashes with a private key to ensure the specified user sent it)
'''

class BlockChain:
    def __init__(self, key = RSA.generate(2048)):
        """
        :param privKey: <Crypto.Pubkey.RSA> the keypair you're using to sign / encrypt data.

        """

        self.cipher = pkcs1_15.PKCS115_SigScheme.new(key)
        if (not cipher.can_sign()):
            return ValueError("key must be a private key / able to sign messages")

        self.pubkey = key.public_key()
        self.chain = []
        self.nodes = set()

        self.new_block(previous_hash='1', proof=100)

    def new_block(self, message, proof, prev_hash = self.hash(self.chain[-1])):
        block = {
            'pubkey': self.pubkey,
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'message': b64encode(message),
            'proof': proof,
            'prev_hash': prev_hash,
        }
        self.chain.append(block)

        return block
    
    def new_block(self, message):
        if (self.chain.length == 0):
            return
        
        prev_hash = self.hash(self.chain[-1])
        proof = proof_of_work(self.cipher[-1])

        block = {
            'pubkey': self.pubkey,
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'message': b64encode(message),
            'proof': proof,
            'prev_hash': prev_hash,
            'signature': cipher.sign(SHA256.new(message))
        }

        self.chain.append(block)
        return block

    @property
    def lastBlock(self):
        return self.chain[-1]

    def hash(self, block):
        """
        get the hash of a block
        :param block: <dict> the block to collect a hash for
        :return: <:class: SHA256Hash> the hash of the message
        """
        block_str = json.dumps(block, sort_keys=True)
        return SHA256.new(block_str)

    def proof_of_work(self, lastBlock):
        """
        returns a proof of work (an intger that when hashed with the hash of the last block and proof from the hashed block is signed)

        :param lastBlock: <dict> the previous node in the BlockChain
        :return: <int> the new valid proof of work
        """

        lastProof = lastBlock['proof']
        lastHash = self.hash(lastBlock)

        proof = 0
        while (not self.validProof(lastProof, proof, lastHash)):
            proof+=1

        return proof
    
    @staticmethod
    def validProof(lastProof, proof, lastHash):
        '''
        :param lastproof: <int> the proof of work from the previous block
        :param proof: <int> the proof we're trying this time
        :param lastHash: <str> the hash of the previous block
        :return: <bool> true if the guess hash is signed (4 leading 0's)
        '''
        guess = f'{lastProof}{proof}{lastHash}'.encode()
        guessHash = SHA1.new(guess).hexdigest()
        return guessHash[:4] == "0000"

    def register_node(self, address, pubkey):
        """
        add a new node to send and recive things from
        :param address: <str> a valid address to another node (i.e. https://10.0.0.1:8000/user1)
        :param pubkey: a valid public key to use to decrypt the message inside (validation purposes)
        """
        parsedUrl = urlparse(address)
        if (parsedUrl.netloc):
            # regular website thingey
            self.nodes.add(parsedUrl.netloc)
        elif (parsedUrl.path):
            # for an ip address w/ path
            self.nodes.add(parsedUrl.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        validates a new blockchain in 2 ways:
        for each block (beyond the first)
            it first checks that the hash matches
        """


        # counting backwards because it's more likely that a problem will be with anything new
        for i in range(len(chain), 1, -1):
            last_block = chain[i - 1]
            block = chain[i]
            print(f'{last_block}')
            print(f'{block}')
            print('\n-=-=-=-=-=-=-\n')

            # checking hash
            try:
                ver = pkcs1_15.PKCS115_SigScheme(block['pubkey'])
                last_block_hash = ver.verify(self.hash(last_block))
            except: 
                return False
            if (block['prevHash'] != last_block_hash):
                return False

            # checking the proofs are valid
            if (not self.validProof(last_block['proof'], block['proof'], last_block_hash)):
                return False

            last_block = block
        
        return True