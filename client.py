import os
import pickle
import socket

def initialize():
	print("Client is starting up.....")
	if ((os.path.isfile("settings") == True) and (os.stat("settings").st_size != 0)):
		with open("settings", "rb") as input:
			settings = pickle.load(input)
			clientOperation(settings)
			input.close()
	else:
		setup()

def setup():
	serverIP = input("Please enter server IP address : ")
	clientPort = input("Please enter client port no : ")
	settings = Settings(socket.gethostbyaddr(serverIP)[0], clientPort)
	with open("settings", "wb") as output:
		pickle.dump(settings, output, pickle.HIGHEST_PROTOCOL)
		output.close()

class Settings:
	def __init__(self, serverHost, clientPort):
		self.host = serverHost
		self.clientPort = int(clientPort)
		print("Set to connect to "+self.host+" from port "+str(self.clientPort)+"\nPlease restart client to apply changes.")

def clientOperation(settings):
	serverHandleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverHandleSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	peerHandleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	peerHandleSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	peerHandleSocket.bind((socket.gethostname(), settings.clientPort))
	
	try:
		print("Connecting to "+settings.host+" from "+socket.gethostname()+" on port "+str(settings.clientPort))
		serverHandleSocket.connect((settings.host, 12345))
		if login(serverHandleSocket, settings) == 1:
			while True:
				mode = input("Please enter 1 for performing computation or 2 for volunteering in a computation. ")
				if mode == '1':
					perform(settings)
				elif mode == '2':
					responder(peerHandleSocket)
				else:
					print("Invalid option. ")
		else:
			print("Login failed.")

	except ConnectionError:
		print("Failed to connect to server")

def login(serverHandleSocket, settings):
	uname = input("Enter your username : ")
	pwd = input("Enter your password : ")
	loginDetails = {"uname" : uname, "pwd" : pwd, "listeningPort" : settings.clientPort}
	loginPacket = pickle.dumps(loginDetails)
	serverHandleSocket.send(loginPacket)
	serverack = serverHandleSocket.recv(1024)
	ackdata = pickle.loads(serverack)
	if (ackdata["uname"] == uname) and (ackdata["status"] == "ok"):
		return 1
	else:
		return 0

def perform(settings):
	print("Performing computation")

def responder(peerHandleSocket):
	print("Listening on socket")

if __name__ == "__main__":
	initialize()