import json
import Crypto
import requests
import flask
from time import time
from base64 import b64decode, b64encode
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, SHA1
from Crypto.Signature import pkcs1_15

'''
note, quite a bit of this class took inspiration from https://github.com/dvf/blockchain/
(This class does use most of the protocols, however it encodes messages instead of transactions, and signs the hashes with a private key to ensure the specified user sent it)
'''

class BlockChain:
    def __init__(self, username, net_passwd = 'Stuff and Things', netid = 1, key = RSA.generate(2048),):
        """
        :param privKey: <Crypto.Pubkey.RSA> the keypair you're using to sign / encrypt data.
        :param netid: <int> the network id you're using. (note, this will change to be a random number I'll generate somehow later)
        
        Link username to public key hash. (key hash = user_id)
        If a username matches a previous username, then have to 
        """

        self.cipher = pkcs1_15.PKCS115_SigScheme(key)
        if (not self.cipher.can_sign()):
            return ValueError("key must be a private key / able to sign messages")

        self.pubkey = key.public_key()
        self.chain = []
        self.nodes = set()
        self.netid = netid
        self.user_id = SHA1.new(b64encode(self.pubkey.export_key())).hexdigest()
        self.username = username

        self.new_block("", proof=100, prev_hash='1')
    
    def lastBlock(self):
        return self.chain[-1]

    def netid(self):
        return self.netid

    def key(self, key):
        self.cipher = pkcs1_15.PKCS115_SigScheme(key)
        self.pubkey = key.pubkey
        self.user_id = SHA1.new(pubkey.export_key()).hexdigest()

    def register_node(self, address, username, pubkey, signature):
        """
        add a new node to send and recive things from
        :param address: <str> a valid address to another node (i.e. https://10.0.0.1:8000/user1)
        :param pubkey: a valid public key to use to decrypt the message inside (validation purposes)
        """
        parsedUrl = urlparse(address)
        message_hash = SHA256.new(self.passwd).encode('utf-8') 
        try:
            pubCipher = pkcs1_15.PKCS115_SigScheme(pubkey)
            pubCipher.verify(message_hash, signature)
        except ValueError:
            return False
        if (parsedUrl.netloc):
            # regular website thingey
            self.nodes.add({'address': parsedUrl.netloc, 'user': username, 'pubkey':pubkey})
        elif (parsedUrl.path):
            # for an ip address w/ path
            self.nodes.add({'address': parsedUrl.path, 'user': username, 'pubkey':pubkey})
        else:
            raise ValueError('Invalid URL')
        return

    def new_block(self, message, proof = None, prev_hash = None):
        """
        creates a new block and adds it to the chain (as well as gives it to you)

        :param message: <str> the specific data the block holds
        :param proof: <int> the number that allows the hash to be signed
        :param prev_hash: <hash> the hash of the previous block in the chain
        :return: <dict> the block to be added to the chain (note, it is added to the chain by the function as well)
        """
        if (not proof):
            proof = self.proof_of_work(self.chain[-1])
        if (not prev_hash):
            prev_hash = self.hash(self.chain[-1])
        block = {
            'user-id': self.user_id,
            'pubkey': self.pubkey.export_key('OpenSSH').decode('UTF-8'), 
            'index': len(self.chain) + 1, #int
            'timestamp': time(), #float
            'message': message, #str
           'proof': proof, #int
            'prev_hash': prev_hash, #str
            'signature': self.cipher.sign(self.hash(message.encode('utf-8')))
        }
        block['signature']=b64encode(block['signature']).decode('ascii')
        #block['pubkey'] = b64encode(block['pubkey']).decode('ascii')
        self.chain.append(block)

        #push to all nodes : f"https://{node}/update"
        return block

    def pull_data(self, node):
        """
        :param node: <str> the node to request data from
        :return: <bool> True if data was overwritten, false if otherwise
        note, this will be called if an update gets pushed to {self}/update
        """

        response = requests.get(f"https://{node}/chain")

        if (response.status_code == 200):
            if (((response.json()['length'] > len(self.chain)))):
                if (valid_chain(response.json()['chain'])):
                    self.chain = response.json()[chain]
                    return True
        
        return False

    def resolve_conflicts(self):
        """
        resolves conflicts between the current blockchain and those owned by others

        :return: <bool> True if the chain was replaced
        """

        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        #find largest node
        for node in neighbors:
            address = node['address']
            response = request.get(f"https://{address}/chain")

            if (response.status_code == 200):
                length = response.json()['length']
                chain = response.json()['chain']

                if (length > max_length):
                    max_length = length
                    new_chain = chain

        #Replace chain if a newer chain was discovered and it works out
        if ((new_chain) and (valid_chain(new_chain))):
            self.chain = new_chain
            return True

        return False

    def validChain(self, chain):
        """
        validates a new blockchain in 2 ways:
        for each block (beyond the first)
            it first checks that the hash matches

        :param chain: <list> new blockchian to be checked
        """
        # counting backwards because it's more likely that a problem will be with anything new
        for i in range(len(chain) - 1, 1, -1):
            last_block = chain[i - 1]
            block = chain[i]
            print(f'{last_block}')
            print(f'{block}')
            print('\n-=-=-=-=-=-=-\n')

            # checking hash
            if (not validBLock(block, last_block)):
                return False
        return True

    def validBlock(self, block, prevBlock):
        # checking that the validated message signature matches the hash of the message
        try:
            pubCipher = pkcs1_15.PKCS115_SigScheme(RSA.import_key(block['pubkey']))
            pubCipher.verify(self.hash(block['message']), block['signature'])
        except:
            return False

        #checking that the previous hash matches
        last_block_hash = ver.verify(self.hash(last_block))
        if (block['prevHash'] != last_block_hash):
            return False

        # checking the proofs are valid
        if (not self.validProof(last_block['proof'], block['proof'], last_block_hash)):
            return False
    
    @staticmethod
    def validProof(lastProof, proof, lastHash):
        '''
        :param lastproof: <int> the proof of work from the previous block
        :param proof: <int> the proof we're trying this time
        :param lastHash: <str> the hash of the previous block
        :return: <bool> true if the guess hash is signed (4 leading 0's)
        '''
        guess = f'{lastProof}{proof}{lastHash}'.encode()
        guessHash = SHA256.new(guess).hexdigest()
        return guessHash[:4] == "0000"

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
    
    def hash(self, block):
        """
        get the hash of a block
        :param block: <dict> the block to collect a hash for
        :return: <:class: SHA256Hash> the hash of the message
        """
        return SHA256.new(f"{block}".encode('utf-8'))