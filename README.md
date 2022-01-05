# pychatbot

The official chitta chatbot python package

This library 

A serverless cloud template with starter whatsapp chatbot flows. The library 

# Installation

Run $ pip3 install py-algorand-sdk to install the package.

Alternatively, choose a distribution file, and run $ pip3 install [file name].

SDK Development
Install dependencies

pip install -r requirements.txt
Run tests

make docker-test
Format code:

black .
Quick start
Here's a simple example you can run without a node.

from algosdk import account, encoding

# generate an account
private_key, address = account.generate_account()
print("Private key:", private_key)
print("Address:", address)

# check if the address is valid
if encoding.is_valid_address(address):
    print("The address is valid!")
else:
    print("The address is invalid.")
Node setup
Follow the instructions in Algorand's developer resources to install a node on your computer.

Running examples/example.py
Before running example.py, start kmd on a private network or testnet node:

$ ./goal kmd start -d [data directory]
Next, create a wallet and an account:

$ ./goal wallet new [wallet name] -d [data directory]
$ ./goal account new -d [data directory] -w [wallet name]
Visit the Algorand dispenser and enter the account address to fund your account.

Next, in tokens.py, either update the tokens and addresses, or provide a path to the data directory.

You're now ready to run example.py!

Documentation
Documentation for the Python SDK is available at py-algorand-sdk.readthedocs.io.

License
py-algorand-sdk is licensed under a MIT license. See the LICENSE file for details.
