# Blockchain Message Board
## How does a Blockchain work?
First we have to understand a few things:
1. A hash: Pretty much a "signature" of a bit of text. Each bit of text has it's own hash, and vice versa.
  a. A signed hash: if a hash starts with 4 leading 0's (this is manipulated by a number called a nonce)
2. Pub/priv key encryption: Each public / private key can encrypt a message sent by the other. In this case, we're encrypting using the private key so that others can validate the message using our public key. (Never give out your private key)
3. What is a block: A block is a Object / data type and for each block, it has 4 things.
  a. data - whatever we're sending (and encrypting using our private key)
  b. previous hash - the hash of the previous block in the sequence
  c. hash - the hash of this block (data, previous block, and nonce)
  d. nonce - the "number used only once." It's job is to ensure that the hash starts with 4 leading 0's.
(note, each user will have an array of public keys linked to a network address)

## How does this work?
Given an array of nodes, each has a copy of the "blockchain." If there is a new hash posted, then each node checks it against its own chain. If the new nodes are signed and the hashes of the previous node match the hashes it has, it accepts it as valid. Next when you read it, you can only decrypt it with the public key if the sender decrypted it with their private key.

## What do I want to do with it?
I intend to mainly use this for my own research and just mess around with the idea of how one would create a blockchain network, and thus, create an anonomous message board using blockchain technology.

## How do I intnend to do this?
### Per node
A node will have 2 threads. One will listen for updates to the blockchain, and the other will send out updates. Note, to join the network, the new node will message an existing node with its public key, and that node will send out its node_struct, and each existing node will update their hash-maps, and the accepting node will send its hashmap of nodes in return.
A blockchain update can come in two forms. 1. a status update (where the node shares a new / change to it's status or a new member joining) or 2. a normal message.

### Per block
Each block as above will have data (either a message or a new / updated node struct) - encrypted using its public key
A timestamp (this will be a messaging app, it would make sense to have a time for each message)
A nonce (to modify the hash)
a previous hash (to link it to the blockchain)
and a signed hash of all of the previous information (signed = four leading 0's)

## member struct:
pretty much a member struct is just a way to transfer a new hashmap entry linking the network address of a node to its public key. It's not massive.

(Note, I don't have enough practical knowledge to debate the ethics of this technology, I simply know enough to know that it's a bit of a sore subject)
