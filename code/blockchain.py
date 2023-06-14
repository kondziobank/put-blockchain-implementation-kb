from time import time
import pwinput
import hashlib
import json
import random

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or hashlib.sha256(json.dumps(self.chain[-1], sort_keys=True).encode()).hexdigest(),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.chain[-1]['index'] + 1
    
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = hashlib.sha256(json.dumps(self.chain[i - 1], sort_keys=True).encode()).hexdigest()
            
            # Check if the hash of the current block is correct
            if current_block['previous_hash'] == previous_block:
                return True       
            # Check if the proof of work is valid
            if hashlib.sha256(str(current_block['proof']).encode()).hexdigest()[:4] == '0000':
                return True
        return False

    def import_data_from_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.current_transactions = data['current_transactions']
            self.chain = data['chain']

    def export_to_file(self, filename):
        data = {
            'current_transactions': self.current_transactions,
            'chain': self.chain
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

# Program start
blockchain = Blockchain()

# variables and data structures
loginsAndPasswords = {}

# parse txt file with logins and passwords
with open("loginData.txt", 'r') as credentials:
    oneLine = credentials.readlines()
for i in oneLine:
    if('\n') in i:
        i = i[:-1]
    j = i.split('-')
    loginsAndPasswords[j[0]] = j[1]

# infinite loop of program
while(True):
    login = attemptL = input("Login: ")
    attemptP = pwinput.pwinput("Password: ")
    
    # login attepmts
    try:
        loginsAndPasswords[attemptL]
    except:
        print("Wrong data")
        continue
    if (hashlib.sha256(attemptP.encode("utf-8")).hexdigest() != loginsAndPasswords[attemptL]):
        print("Wrong data")
    else:
        filename = "chain.json"
        blockchain.import_data_from_file(filename)

        # instructions
        while(True):
            print("\n")
            print("1 - add a new block")
            print("2 - add a new transaction")
            print("3 - check validity of blockchain")
            print("4 - see blockchain")
            print("5 - save blockchain")
            
            try:
                userInteraction = int(input())
            except:
                print("Wrong data")
                continue

            # new block
            if(userInteraction == 1):
                proof = random.randint(10000, 100000)  # Placeholder for the actual proof of work
                last_block_out = hashlib.sha256(json.dumps(blockchain.chain[-1], sort_keys=True).encode()).hexdigest()
                previous_hash = last_block_out
                blockchain.new_block(proof, previous_hash)
                print("\n")
                print("New block added!")

            # new transaction
            elif(userInteraction == 2):
                print("Sender: {}".format(login))
                receiver = input("Type receiver: ")
                amount = input("How much transfer: ")
                blockchain.new_transaction(login, receiver, amount)
                print("\n")
                print("Completed!")

            # validity
            elif(userInteraction == 3):
                print("\n")
                print("Validity", blockchain.is_valid())
                
            # show in terminal
            elif(userInteraction == 4):
                for block in blockchain.chain:
                    print(json.dumps(block, indent=2))
                    print('-' * 50)
            
            # save to file    
            elif(userInteraction == 5):
                filename = "chain.json"
                blockchain.export_to_file(filename)

                print("Blockchain exported to file:", filename)

            else:
                print("Wrong key, type again")