import socket
import time
import pickle

##########################data classes

class Peer(object):
	def __init__(self, uname, pwd, ip, port, status):
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

##########################################

s = socket.socket()
host = socket.gethostname()
port = 12345
s.connect((host, port))

def preparePacket(data):  #serializes data and prepares packet
	sendableContent = pickle.dumps(data)
	return sendableContent

while True:
	uname = None
	pwd = None
	inp = None
	inp = raw_input("\t\t\tMenu\n\n\t\t0 for registering\n\t\t1 for getting peerlist\n\t\t2 for getting modulelist\n\t\t5 for deregistering\n\nEnter your option :\t") #temporary menu driver

	if inp == '0': ###########	registering user
		uname = raw_input("What would you like your username to be?\t")
		pwd = raw_input("Password please\t")
		s.send(preparePacket((0, uname, pwd)))
		print s.recv(1024)

	elif inp == '1':	###############	requesting peer list
		print "\nYou've requested peerlist\n"
		s.send(preparePacket((1,)))
		peers = pickle.loads(s.recv(1024))
		if peers == []:
			print "====================================="
			print "No peers\n====================================="
		else:
			for peer in peers:
				print "------------------------------"
				print "Peer name is ", peer.uname
				print "Peer IP is", peer.ip
				print "Peer port is", peer.port
			

	elif inp == '2':	#############	requesting module list
		print "\nYou've requested modulelist\n"
		s.send(preparePacket((2,)))
		modules = pickle.loads(s.recv(1024))
		if modules == []:
			print "====================================="
			print "No modules listed\n====================================="
		else:
			for module in modules:
				print "------------------------------"
				print "Module name is", module.moduleName
				print "Module owner is", module.owner
				print "Holders : \n"
				for holder in peer.holderList:
					print holder, "\n"

	elif inp == '5':	####################	deregistration
		print "You're deleting your account\n"
		uname = raw_input("Re enter your username\t")
		pwd = raw_input("Re enter your password\t")
		s.send(preparePacket((5, uname, pwd)))
		print s.recv(1024)

	else:
		print "-------------------------------"
		print "Invalid option.\n-------------------------------"