#!/usr/bin/env python

import socket
import threading
import pickle
import sys
from pprint import pprint

# trying to create a socket
try:
	host = 'localhost' #socket.gethostname()
	port = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(5)
except socket.error, (value, message):
	if s:
		server.close()
	print ("Could not open the socket: ", message)
	sys.exit(1)

# responder function for client handling
def responder(aClient, address):
	running = 1
	while running:
		packet = aClient.recv(1024)
		data = pickle.loads(packet)


if __name__ == '__main__':
	while True:
		inc, address = s.accept()
		print("Got connection from", address)
		aClient = inc
		newt = threading.Thread(target = responder, args = (aClient, address))
		newt.setDaemon(True)
		newt.start()