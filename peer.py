import os
import pickle
import socket
import getpass
import transfer
import sys

def readFile(fileName):
	with open(fileName, "rb") as inFile:
		return inFile.read()

def writeFile(fileName, writeData):
	with open(fileName, "wb") as output:
		output.write(writeData)

def setup():
	print("Welcome to peer setup.")
	trackerIP = input("Please enter your preferred tracker address : ")
	trackerPort = input("Please enter its port no : ")
	peerPort = input("Please enter port you wish the peer to listen on : ")
	settings = {"trackerIP" : trackerIP, "trackerPort" : int(trackerPort), "peerPort" : int(peerPort)}
	writeFile("settings.dat", pickle.dumps(settings))


def peerFunctionality(settings):
	trackerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	trackerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print("Attempting to connect to tracker........")
	try:
		trackerSock.connect((settings["trackerIP"], settings["trackerPort"]))
		while(1):
			select = input("\n\nEnter : \n\n\t1 For login\n\t2 For signup\n\t3 Exit\n\nYour option : ")
			if select == "1":
				uname = input("Please enter your username : ")
				pwd = getpass.getpass("Please enter your password : ")
				print("Logging in.....")
				transfer.sender(trackerSock, pickle.dumps({"category" : "login", "uname" : uname, "pwd" : pwd}))
				reply = pickle.loads(transfer.receiver(trackerSock))
				if reply["category"] == "message" and reply["content"] == "auth success":
					print("Login successful.")
					listofmodules = pickle.loads(readFile("modulelist.dat"))
					transfer.sender(trackerSock, pickle.dumps({"category" : "modulelist", "content" : listofmodules}))
					break
				else:
					print("Login failed.")
					if reply["category"] == "message" and reply["content"] == "auth no acc":
						print("Please check your username. No account exists under given name.")
					if reply["category"] == "message" and reply["content"] == "auth wrong pwd":
						print("Incorrect password. Please try again.")
			elif select == "2":
				while(1):
					"""uname = input("Enter desired username : ")
					pwd = getpass.getpass("Enter desired password : ")
					rpwd = getpass.getpass("Re enter password : ") 
					"""
				print("Creating account")
				break
			elif select == "3":
				sys.exit(0)
			else:
				print("Invalid option....")

		while(1):
			select = input("\n\nTemp Menu\n\n\t1 Get peer list\n\t2 Get module list\n\t3 Exit\n\nYour option : ")
			if select == "1":
				transfer.sender(trackerSock, pickle.dumps({"category" : "message", "content" : "get peerlist"}))
				print("Request sent.")
				peerlist = pickle.loads(transfer.receiver(trackerSock))
				print("Peer list received....")
			elif select == "2":
				transfer.sender(trackerSock, pickle.dumps({"category" : "message", "content" : "get modulelist"}))
				modulelist = pickle.loads(transfer.receiver(trackerSock))
				print("Module list received....")
			elif select == "3":
				break
			else:
				print("Invalid option.")
	except (ConnectionError, socket.error):
		print("Connection problems. Please try later.")
	

def initialize():
	if os.path.isfile("settings.dat") and os.path.getsize("settings.dat") > 0:
		try:
			settings = pickle.loads(readFile("settings.dat"))
		except pickle.UnpicklingError:
			print("Settings seems to be corrupted.....")
			setup()
		print("Peer set to get info from "+settings["trackerIP"]+" and listen on port "+str(settings["peerPort"]))
		peerFunctionality(settings)
	else:
		setup()



if __name__ == "__main__":
	try:
		initialize()
	except KeyboardInterrupt:
		print("\n\nExiting.....")