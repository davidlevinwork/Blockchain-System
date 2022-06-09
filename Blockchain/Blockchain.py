import json
import hashlib
import requests
import datetime
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request


###########################
# Creating the Blockchain #
###########################

class Blockchain:

    def __init__(self):
        self.chain = []
        self.nodes = set()
        # This list will contain any new transaction, and once a block is mined, all this transactions of the lists will get into a block.
        # It most be before the create_block function!
        self.transactions = []
        # Each block will have its own proof value & previous_hash (the link with the previous block).
        # The initialize values are for the Genesis block of the blockchain.
        self.create_block(proof=1, previous_hash='0')

    """
    Function role is to create a new block & append it to the blockchain (function will execute after we mine a block).
    """

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        # Init transaction list after creating a block that hold all the transactions information.
        self.transactions = []
        self.chain.append(block)
        return block

    """
    Function role is to return last block of the current chain.
    """

    def get_previous_block(self):
        return self.chain[-1]

    """
    Function role is to define the problem that the miners will need to solve in order to mine a new block.
    The previous proof is an element of the problem that the miners will need to counter in order to find the new proof.
    The problem will be hard to solve but easy to verify.
    """

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # The problem that the miners will have to solve (non symmetrical problem)
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # The accepted proof for mining: 4 leading zeros
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    """
    Function role is to return the hash value of the block.
    """

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    """
    Function role is to validate the chain:
    1) The previous hash of each block is equal to the hash of the previous block
    2) Each block in the blockchain has a correct proof of work
    """

    def is_chain_valid(self, chain):
        block_index = 1
        previous_block = chain[0]
        while block_index < len(chain):
            block = chain[block_index]
            # The first condition is not met
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # The second condition is not met
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    """
    Function role is to create a transaction & add it the list of transactions.
    """

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    """
    Function role is to add the node address to the set of nodes.
    """

    def add_node(self, address):
        parsed_url = urlparse(address)
        # netloc is the url including the port.
        self.nodes.add(parsed_url.netloc)

    """
    Function role is to create the consensus concept.
    """

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        # The chain of the blockchain inside the node on which we are applying this replace_chain method.
        max_length = len(self.chain)
        for node in network:
            # Get the response of the get_chain request of the current node in the nodes network.
            response = requests.get(f'http://{node}/get_chain')
            # Check if the response is OK
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # Conditions for replacing chain
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


#########################
# Mining the Blockchain #
#########################

# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating an address for the node on Port 5000 (port value needs to be identical to the 'app.run' port).
# We need an address for the node, because whenever we mine a new block, there is going to be a transaction from this node to yourself.
# The uuid4 will generate a unique address for this node.
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

"""
Function role is to mine a new block (the given url is .../mine_block).
We are using the GET method because we want to get the new block.
"""


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # Add a new transaction (receiver & amount are defaults values)
    blockchain.add_transaction(sender=node_address, receiver='Admin', amount=1)
    # Creating the new block
    block = blockchain.create_block(proof, previous_hash)
    # Informative message to the user with the block details he just mined
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200


"""
Function role is to display the full chain (the given url is .../get_chain).
We are using the GET method because we want to get the full chain.
"""


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


"""
Function role is to check if the blockchain is valid (the given url is .../is_valid).
We are using the GET method because we want validate the given blockchain.
"""


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200


"""
Function role is to add a new transaction to the blockchain (the given url is .../add_transaction).
We are using the POST method because we want to post the new transaction.
"""


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    # Get the json file posted in Postman
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    # Ensure that the json file contain all the keys
    if not all(key in json for key in transaction_keys):
        response = 'Some elements of the transaction are missing'
        return response, 400
    # Add the new transaction details
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    # 201 because we are in POST request
    return jsonify(response), 201


#################################
# Decentralizing the Blockchain #
#################################

"""
Function role is to connect new nodes (the given url is .../connect_node).
We are using the POST method because we are going to create a new node in the decentralized network.
"""


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    # Get all the addresses of all the nodes that are in the blockchain network
    nodes = json.get('nodes')
    # If there are zero nodes to register
    if nodes is None:
        response = "No node"
        return response, 400
    # Add each of the nodes
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Adonis Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


"""
Function role is to replace the chain by the longest chain if needed (the given url is .../replace_chain).
The function will apply the consensus in case one chain in the decentralized network is not up to date 
(which basically will happen any time a new block is mined on one specific node).
We are using the GET method because we want to check if we need to replace the chain.
"""


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    # Do we need to replace the chain
    is_chain_replaced = blockchain.replace_chain()
    # We did a replace for the chain (inside the replace_chain function)
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    # We didnt replace the chain
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200


#######################
# Run the application #
#######################
app.run(host='0.0.0.0', port=5000)
