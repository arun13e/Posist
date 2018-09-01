#!/usr/bin/python -u
import datetime
import random
from hashlib import md5

from Crypto.Cipher import AES
import base64, os

document = {}

nodeCount = 0
genesisReferenceNode = False

#AES code from https://gist.github.com/syedrakib/d71c463fc61852b8d366



class Node:
	timestamp = ''
	data = {}
	nodeNumber = 1
	nodeId = ''
	referenceNodeId = ''
	childReferenceNodeId = []
	genesisReferenceNodeId = ''
	hashValue = ''

	def encrypt(self):
		global generate_secret_key_for_AES_cipher
		global encrypt_message
		padding_character = "{"
		secret_key = generate_secret_key_for_AES_cipher()
		self.data = encrypt_message(self.data, secret_key, padding_character)
		return secret_key

	def decrypt(self, key):
		global decrypt_message
		padding_character = "{"
		decrypted_msg = decrypt_message(self.data, secret_key, padding_character)
		return decrypt_message

	def __init__(self, value, ownerId, ownerName, parentNode= None):
		global genesisReferenceNode
		global nodeCount
		self.nodeId = random.getrandbits(32)
		if( genesisReferenceNode == False ):
			self.referenceNodeId = None #genesisNode
			genesisReferenceNode = self.nodeId

		self.timestamp = datetime.datetime.now()
		self.genesisReferenceNodeId =  genesisReferenceNode
		
		self.referenceNodeId = parentNode
		self.childReferenceNodeId = []

		# for nodes in document[parentNode].childReferenceNodeId:
		# 	pass #check values

		if(parentNode is not None):
			print("Creating Genesis node...")
			document[parentNode].childReferenceNodeId.append({self.nodeId : self})
		# self.hashValue = ''

		self.data = str(ownerId) + ';' +  str(value) + ';' + str(ownerName) + ';' + md5(str(value) + str(ownerId) + str(ownerName)).hexdigest()

		# print("Data is: " + self.data)
		print("===================")
		print("Record created")
		print self
		print("Secret key is" + self.encrypt())

		# print("Encrypted data is: " + self.data)

		nodeCount = nodeCount + 1
		self.nodeNumber = nodeCount

		document[self.nodeId] = self
		print("Number of nodes: " + str(nodeCount))

		print("===================")


	def __str__(self):
		return str("NodeID: " + str(self.nodeId) + " \n1Children : [" + ', '.join([str(x) for x in self.childReferenceNodeId])  + "]") 

def generate_secret_key_for_AES_cipher():
	
	AES_key_length = 16 
	secret_key = os.urandom(AES_key_length)
	encoded_secret_key = base64.b64encode(secret_key)
	return encoded_secret_key

def encrypt_message(private_msg, encoded_secret_key, padding_character):
	
	secret_key = base64.b64decode(encoded_secret_key)
	cipher = AES.new(secret_key)
	padded_private_msg = private_msg + (padding_character * ((16-len(private_msg)) % 16))
	encrypted_msg = cipher.encrypt(padded_private_msg)
	encoded_encrypted_msg = base64.b64encode(encrypted_msg)
	return encoded_encrypted_msg

def decrypt_message(encoded_encrypted_msg, encoded_secret_key, padding_character):
	secret_key = base64.b64decode(encoded_secret_key)
	encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	cipher = AES.new(secret_key)
	decrypted_msg = cipher.decrypt(encrypted_msg)
	unpadded_private_msg = decrypted_msg.rstrip(padding_character)
	return unpadded_private_msg

def createNode():
	ownerName = raw_input("Enter Your name: ")
	ownerId = raw_input("Enter Your ID: ")
	value = raw_input("Enter Value: ")

	if( genesisReferenceNode == False ):
		node = Node(value, ownerId, ownerName)
	else:
		parentNode = raw_input("Enter parent Node ID: ")
		node = Node(value, ownerId, ownerName, parentNode)

def main():
	input = 1
	while input != 0:
		print '''
		
		****************************
		@ Add new record
		@ View record
		@ Exit
		'''
		input = raw_input()

		if input == '1':
			createNode()
		



    
if __name__ == "__main__":
    main()
