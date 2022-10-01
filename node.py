import requests
from flask import Flask, jsonify, request, render_template
from uuid import uuid4
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, SHA1
from Crypto.Signature import pkcs1_15

from BlockChain import BlockChain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

path = ""
blockChain = BlockChain('user')
cipher = pkcs1_15.PKCS115_SigScheme(RSA.generate(2048))

@app.route(f"{path}/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route(f"{path}/key/new", methods=['POST'])
def use_key():
    values = request.get_json()

    if (not 'key' in values):
        return 'missing_value', 400
    
    response = {'message': f'key updated'}

    return jsonify(response), 201

@app.route(f"{path}/chain", methods=['GET'])
def get_chain():
    response = {
        'chain': (blockChain.chain),
        'length': len(blockChain.chain),
    }
    return jsonify(response), 200

@app.route(f"{path}/nodes/register", methods=['PUT'])
def register_nodes():
    values = request.get_json()

    if (values.get('netid') != blockChain.netid()):
        return 'Error: submitting to wrong network', '400'

    nodes = values.get('nodes')
    if (nodes is None):
        return 'Error: please supply a list of nodes', '400'

    for node in nodes:
        blockChain.register_node(node)
    
    response = {
        'message': 'Node(s) have been registered',
        'total_noeds': list(blockChain.nodes),
    }

    return jsonify(response), 201

@app.route(f'{path}/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockChain.resolve_conflicts()

    chain=[]
    for block in blockChain.chain:
        chain.append(block)


    if replaced:
        response = {
            'netid': blockChain.netid,
            'message': 'Our chain was replaced',
            'new_chain': chain
        }
    else:
        response = {
            'netid': blockChain.netid,
            'message': 'Our chain is authoritative',
            'chain': chain
        }

    return jsonify(response), 200

if __name__ == "__main__":
    app.run()