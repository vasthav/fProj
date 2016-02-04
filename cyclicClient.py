import socket
import time
import pickle

#############################data classes

class Peer(object):
	def __init__(self, uname, pwd, ip, port, status):
		self.ip = ip
		self.port = port

s = socket.socket()
host = socket.gethostname()
port = 12345

class ModuleHolders(object):
	def __init__(self, moduleName, owner):
		self.moduleName = moduleName
		self.holderList = []
		self.owner = owner

	def addHolders(uname):
		self.holderList.append(uname)

	def removeHolders(uname):
		self.holderList.remove(uname)

##########################################

s.connect((host, port))

def preparePacket(data):  #serializes data and prepares packet
	sendableContent = pickle.dumps(data)
	return sendableContent

while True:
	uname = None
	pwd = None
	inp = None
	inp = input("Enter 0 for registering, 1 for getting peerlist, 2 for getting modulelist, 5 for deregistering") #temporary menu driver

	if inp == 0: ###########	registering user
		uname = raw_input("What would you like your username to be?")
		pwd = raw_input("Password please")
		s.send(preparePacket((0, uname, pwd)))
		print s.recv(1024)

	elif inp == 1:	###############	requesting peer list
		print "You've requested peerlist"
		s.send(preparePacket((1,)))
		peers = pickle.loads(s.recv(1024))
		if peers == []:
			print "No peers"
		for peer in peers:
			print "Module name is ", peer.uname
			print "Peer IP is", peer.ip
			print "Peer port is", peer.port
			

	elif inp == 2:	#############	requesting module list
		print "You've requested modulelist"
		s.send(preparePacket((2,)))
		modules = pickle.loads(s.recv(1024))
		for module in modules:
			print "Module name is", peer.uname
			print "Module owner is", module.owner
			print "Holders : \n"
			for holder in peer.holderList:
				print holder, "\n"

	elif inp == 5:	####################	deregistration
		print "You're deleting your account"
		uname = raw_input("Re enter your username")
		pwd = raw_input("Re enter your password")
		s.send(preparePacket((5, uname, pwd)))
		print s.recv(1024)