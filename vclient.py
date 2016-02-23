#!/usr/bin/env python

import socket
import sys
import os
import re
import getpass
import pickle
import getpass
import fmanager
from pprint import pprint
#trying to connect server
try:
	host = 'localhost'
	port = 12345
	size = 1024
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
except socket.error as message:
	if s:
		s.close()
	print ("Could not open socket: ", message)

def prepare_packet(data):  
	sendable_content = pickle.dumps(data)
	return sendable_content

def  extract_packet(data):
	raw_data = pickle.loads(data)
	return raw_data

def close_connection():
	s.send(prepare_packet(('100')))
	s.close()
	sys.exit(0)

def recv_file(fname):
	# with open(fname,"wb") as fd:
	# 	insob = s.recv(1024)
	# 	while insob:
	# 		pickle.dump(insob, fd)
	# 		insob = s.recv(1024)
	# print("file recieved.")
	size = extract_packet(s.recv(1024))
	peers = pickle.load(s.recv(size))
	pprint(peers)
	# while size >= 0:
	# 	peers = pickle.load(s.recv(1024))
	# 	pprint(peers)
	# 	size = size - 1024

def authenticate():
	print("""		Menu
		0 Login
		1 Sign Up
		Enter your option: """)
	inp = input()
	if inp == '':
		print("Invalid option")
		close_connection()
	if inp == "0":
		for i in range(4):
			if i == 3:
				print("Authentication Failure, Closing connection")
				close_connection()

			username = input("Username: ")
			password = getpass.getpass(prompt= "Password: ")

			packet = prepare_packet([0, username, password])
			s.send(packet)
			res = s.recv(1024)
			# print(res)
			password=None
			if res == b'1':
				print("Successfully logged in.")
				break
			elif res == b'0':  
				print("Password or Username doesn't match. Try again.")
			print("starting again")



	if inp == "1":
		for i in range(4):
			if i == 3:
				print("Authentication Failure, Closing connection")
				close_connection()

			username = input("Enter a Username : ")
			print(username)

			password = getpass.getpass(prompt= "New Password: ")
			packet = prepare_packet([1, username, password])
			s.send(packet)
			res = s.recv(1024)
			# print(res)
			if res == b'1':
				print("Successfully account Created and logged in.")
				break
			elif res == b'2':
				print("User already exits, Try a different username.")

def command_handler():
	print("""		Menu
		0 Logout
		1 Get IP address
		2 Get Port 
		3 Get Connection Status
		4 Get NodeList
		5 Exit
		Enter your option: """)
	inp = input()
	pprint(inp)
	if inp == '0':
		s.send(prepare_packet("100"))
		return 0
	elif inp == '4':
		s.send(prepare_packet("4"))
		print("File request sent.")
		recv_file("inputfile")
		fmanager.show("inputfile")

if __name__ == '__main__':
	running = 1
	while 1:
		authenticate()
		print("Authentication Done!")
		while running:
			rval = command_handler()
			if rval == 0:
				break
	close_connection()			