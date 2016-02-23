#!/usr/bin/env python

import socket
import threading
import pickle
import sys
import os
import fmanager
from pprint import pprint

# trying to create a socket
try:
	host = 'localhost' #socket.gethostname()
	port = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(5)
except socket.error as message:
	if s:
		server.close()
	print ("Could not open the socket: ", message)
	sys.exit(1)

# serializes data and prepares packet
def prepare_packet(data):  
	sendable_content = pickle.dumps(data)
	return sendable_content

def extract_packet(data):
	raw_data = pickle.loads(data)
	return raw_data

# responder function for client handling
def responder(aClient, address):
	# rval = authenticate(aClient, address)
	# if rval == 0:
	# 	aClient.close()
	# 	return
	running = 1
	while running:
		packet = aClient.recv(1024)
		data = pickle.loads(packet)
		pprint(data)
		print(data[0])
		if data == '100':
			# fmanager.logout(fname, )
			aClient.close()
			break

		if data[0] == 0 or data[0] == 1:
			authenticate(aClient, address, data)

		if data[0] == "4":
			sendfile(aClient, address, "peerlist")
			print("file sent.")
	# fmanager.logout()
	# aClient.close()

def authenticate(aClient, address, data):
	if data[0] == 0:
		if fmanager.uname_exits("peerlist", data[1]) == 1:
			if data[2] == fmanager.getpass("peerlist", data[1]):
				aClient.send(b'1')
		else: 
			aClient.send(b'0')

	if data[0] == 1:
		if fmanager.uname_exits("peerlist", data[1]) == 0:
			fmanager.insfunc("peerlist", (data[1], data[2], address[0], address[1], "1"))
			aClient.send(b'1')
		else:
			aClient.send(b'2')
	# return uname	

def sendfile(aClient, address, fname):
	# with open(fname,"rb") as input:	
	# 	i =0
	# 	while True:
	# 		print(i)
	# 		i = i+1
	# 		try:
	# 			content = pickle.load(input)
	# 		except(EOFError):
	# 			content = ()
	# 		sendableContent = prepare_packet(())
	# 		aClient.send(sendableContent)
	size = os.path.getsize(fname)
	aClient.send(prepare_packet(size))
	with open(fname,"rb") as input:
		try:
			content = pickle.load(input)
		except(EOFError):
			content = []
		sendableContent = pickle.dumps(content)
		aClient.send(sendableContent)


if __name__ == '__main__':
	while True:
		inc, address = s.accept()
		print("Got connection from", address)
		aClient = inc
		newt = threading.Thread(target = responder, args = (aClient, address))
		newt.setDaemon(True)
		newt.start()