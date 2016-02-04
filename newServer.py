import socket
import threading
import pickle

#################data classes

class Peer(object):
	def __init__(self, uname, pwd, ip, port):
		self.uname = uname
		self.pwd = pwd
		self.ip = ip
		self.port = port

class ModuleHolders(object):
	def __init__(self, moduleName, owner):
		self.moduleName = moduleName
		self.holderList = []
		self.owner = owner

	def addHolders(uname):
		self.holderList.append(uname)

	def removeHolders(uname):
		self.holderList.remove(uname)

##########################server functionality

def fileOperations(classSelector, operationSelector, args):
	if operationSelector == "get":
		if classSelector == "p":
			fname = "peerlist.dat"
		elif classSelector == "m":
			fname = "modulelist.dat"
		with open(fname,"rb") as input:
			try:
				content = pickle.load(input)
			except(EOFError):
				content = []
			sendableContent = pickle.dumps(content)
			return sendableContent

	if operationSelector == "+":
		if classSelector == "p":
			fname = "peerlist.dat"
			accdetails = args[0]
			newpeer = Peer(accdetails[1], accdetails[2], address[0], address[1])
			peers = []
			with open("peerlist.dat","rb+") as input:
				try:
					peers = pickle.load(input)
					for peer in peers:
						if peer.uname == newpeer.uname:
							return 1
				except(EOFError):
					peers = []
			peers.append(newpeer)
			flag = 0
			with open('peerlist.dat','wb') as output:
				pickle.dump(peers, output, pickle.HIGHEST_PROTOCOL)
				return 2

	if operationSelector == "-":
		if classSelector == "p":
			flag =0
			fname  = "peerlist.dat"
			peers = []
			with open(fname, "rb") as input:
				try:
					peers = pickle.load(input)
					for peer in peers:
						if peer.uname == args[1]:
							if peer.pwd == args[2]:
								peers.remove(peer)
								flag = 1
				except(EOFError):
					return 0
			if flag == 1:
				with open(fname,'wb') as output:
					pickle.dump(peers, output, pickle.HIGHEST_PROTOCOL)
				return 1
			else:
				return 0


def responder(aClient, address):
	while True:
		packet = aClient.recv(1024)
		print packet
		data = pickle.loads(packet)
		print data[0]
		if data[0] == 0:
			print "Received request for registration from", address
			fileOpStatus = fileOperations("p", "+", (data, address))
			if fileOpStatus == 1:
				aClient.send("Account already exists")
			elif fileOpStatus == 2:
				aClient.send("Account created")
			else:
				aClient.send("Creation failed")
		elif data[0] == 1:
			print "Received request for peerlist from", address
			aClient.send(fileOperations("p", "get", ()))
			print "Peerlist sent"
		elif data[0] == 2:
			print "Received request for module list from", address
			aClient.send(fileOperations("m", "get", ()))
		elif data[0] == 5:
			print "Received request for deletion from", address
			if fileOperations("p", "-", data) == 1:
				aClient.send("You've successfully deregistered")
			else:
				aClient.send("Account removal failed")


#########################initialization and listening

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostname()
port = 12345
s.bind((host, port))

s.listen(5)
while True:
	inc, address = s.accept()
	print "Got connection from", address
	aClient = inc
	newt = threading.Thread(target = responder, args = (aClient, address))
	newt.setDaemon(True)
	newt.start()