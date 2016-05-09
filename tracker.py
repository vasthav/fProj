# tracker.py
# python3.x code

import os
import socket
import select
import pickle
import time


def filewriter(fname, content):
	to_write = pickle.dumps(content)
	try:
		fd = open(fname, "wb")
		fd.write(to_write)
		fd.close()
		return True
	except IOError:
		return False


def filereader(fname):
	try:
		if os.path.getsize(fname) == 0:
			return {}
		fd = open(fname, "rb")
		content = fd.read()
		data = pickle.loads(content)
		fd.close()
		return data
	except (IOError, pickle.PicklingError) as e:
		return False


def login(uname, pwd, addr):
	peerlist = filereader("peerlist")
	if uname in peerlist:
		print("Username exists")
		if peerlist[uname]["pwd"] == pwd:
			print("Password correct")
			if ((time.time() - peerlist[uname]["last_seen"]) <= 60) and (peerlist[uname]["ip"] != addr[0] and peerlist[uname]["port"] != addr[1]):
				print("Just logged in from elsewhere.")
				return False
			else:
				peerlist[uname]["last_seen"] = time.time()
				peerlist[uname]["status"] = "online"
				peerlist[uname]["ip"] = addr[0]
				peerlist[uname]["port"] = addr[1]
				if filewriter("peerlist", peerlist):
					return True
				else:
					return False
		else:
			return False
	else:
		return False


def create(uname, pwd, addr):
	peerlist = filereader("peerlist")
	if uname in peerlist:
		return "exists"
	else:
		peerlist[uname] = {"pwd" : pwd, "ip" : addr[0], "port" : addr[1], "last_seen" : time.time(), "status" : "online"}
		if filewriter("peerlist", peerlist) == True:
			return "success"
		else:
			return "fail"


def keepalive(uname, pwd):
	peerlist = filereader("peerlist")
	if uname in peerlist:
		if peerlist[uname]["pwd"] == pwd:
			peerlist[uname]["last_seen"] = time.time()
			peerlist[uname]["status"] = "online"


def getpeerlist(sock):
	print("Sending peerlist")
	payload = filereader("peerlist")
	sendable_payload = {}
	if payload != False:
		for uname in payload:
			sendable_payload[uname] = {"ip" : payload[uname]["ip"], "port" : payload[uname]["port"], "last_seen" : payload[uname]["last_seen"], "status" : payload[uname]["status"]}
		sock.send(pickle.dumps(sendable_payload))


def getmodulelist(sock):
	print("Sending modulelist")
	payload = filereader("modulelist")
	if payload != False:
		sock.send(pickle.dumps(payload))


def update_peerlist(uname, pwd, status):
	peerlist = filereader("peerlist")
	if uname in peerlist:
		if peerlist[uname]["pwd"] == pwd:
			peerlist[uname]["status"] = status
			filewriter("peerlist", peerlist)


def update_modulelist(uname, pwd, list_of_modules):
	peerlist = filereader("peerlist")
	if uname in peerlist:
		if peerlist[uname]["pwd"] == pwd:
			modulelist = filereader("modulelist")
			modulelist[uname] = list_of_modules
			filewriter("modulelist", modulelist)


def process(msg, sock, addr):
	content = pickle.loads(msg)
	print(content)
	if content["cat"] == "login":
		if login(content["uname"], content["pwd"], addr) == True:
			sock.send(pickle.dumps("success"))
		else:
			sock.send(pickle.dumps("fail"))
	elif content["cat"] == "create":
		creator_response = create(content["uname"], content["pwd"], addr)
		if creator_response == "exists":
			sock.send(pickle.dumps("exists"))
		elif creator_response == "success":
			sock.send(pickle.dumps("success"))
		elif creator_response == "fail":
			sock.send(pickle.dumps("fail"))
	elif content["cat"] == "keepalive":
		keepalive(content["uname"], content["pwd"])
	elif content["cat"] == "get":
		if content["item"] == "peerlist":
			getpeerlist(sock)
		elif content["item"] == "modulelist":
			getmodulelist(sock)
	elif content["cat"] == "update":
		if content["item"] == "peerlist":
			update_peerlist(content["uname"], content["pwd"], content["status"])
		elif content["item"] == "modulelist":
			update_modulelist(content["uname"], content["pwd"], content["list"])


def listupdater(interval):
	peerlist = filereader("peerlist")
	for uname in peerlist:
		if (time.time() - peerlist[uname]["last_seen"]) >= interval:
			peerlist[uname]["status"] = "offline"
	filewriter("peerlist", peerlist)


if __name__ == "__main__":
	try:
		if os.path.isfile("peerlist") == False:
			if filewriter("peerlist", {}) == False:
				print("Unable to create support files, aborting.")
		if os.path.isfile("modulelist") == False:
			if filewriter("modulelist", {}) == False:
				print("Unable to create support files, aborting.")
		main_port = int(input("Enter port no to listen on : "))
		main_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		main_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		main_sock.setblocking(0)
		main_sock.bind(("0.0.0.0", main_port))
		dict_of_addr = {}
		main_sock.listen(5)
		list_of_socks = [ main_sock ]
		while list_of_socks:
			msg = None
			readlist, writelist, exceptlist = select.select(list_of_socks, [], [], 0.7)
			for sock in readlist:
				listupdater(60)
				if sock is main_sock:
					try:
						newsock, newaddr = sock.accept()
						newsock.setblocking(0)
						readlist.append(newsock)
						dict_of_addr[newsock] = newaddr
					except BlockingIOError:
						pass
				else:
					msg = sock.recv(1024)
					if msg:
						process(msg, sock, dict_of_addr[sock])
						readlist.remove(sock)
						del dict_of_addr[sock]
					else:
						if sock in readlist:
							readlist.remove(sock)
						elif sock in writelist:
							writelist.remove(sock)


	except KeyboardInterrupt:
		print("Exiting")

