import Flask
import django
import requests
from flask import jsonify, request
from uuid import uuid4
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

import BlockChain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

path = "/"
blockChain = BlockChain()
cipher = pkcs1_15.PKCS115_SigSchech(RSA.generate(2048))


@app.route(f"{path}/messages/new", methods=['POST'])
def new_message():
    values = request.get_json()

    if (not 'message' in values):
        return 'missing value', 400
    
    index = BlockChain.new_block()
    response = {'message': f'message will be added to Block {index}'}

    return jsonify(response), 201

@app.route(f"{path}/key/new", methods=['POST'])
def use_key():
    values = request.get_json()

    if (not 'key' in values):
        return 'missing_value', 400
    
    response = {'message': f'key updated'}

    return jsonify(response), 201

@app.route(f"{path}/chain", methods=['GET'])
def get_chain(self):
    response = {
        'chain': self.blockChain.chain,
        'length': len(self.blockChain.chain)
    }
    return jsonfiy(response), 200

@app.route(f"{path}/nodes/register", methods=['GET'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if (nodes is None):
        return 'Error: please supply a list of nodes', '400'

    for node in nodes:
        blockChain.register_node(nodes)
    
    response = {
        'message': 'Node(s) have been registered',
        'total_noeds': list(blockChain.nodes),
    }

    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200
