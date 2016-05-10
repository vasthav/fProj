import socket
import threading
import pickle
import time
import os

file_lock = threading.Lock()

def filewriter(fname, msg):
	to_write = pickle.dumps(msg)
	file_lock.acquire()
	try:
		fd = open(fname, "wb")
		fd.write(to_write)
		fd.close()
		return True
	except IOError:
		return False
	finally:
		file_lock.release()


def filereader(fname):
	try:
		if os.path.getsize(fname) == 0:
			return {}
		fd = open(fname, "rb")
		msg = fd.read()
		data = pickle.loads(msg)
		fd.close()
		return data
	except (IOError, pickle.PicklingError) as e:
		return False


def login(uname, pwd, addr):
	peerlist = filereader("peerlist")
	if uname in peerlist:
		if peerlist[uname]["pwd"] == pwd:
			peerlist[uname]["last_seen"] = time.time()
			peerlist[uname]["status"] = "online"
			peerlist[uname]["ip"] = addr[0]
			peerlist[uname]["port"] = addr[1]
			if filewriter("peerlist", peerlist):
				return 1
			else:
				return 5
		else:
			return 3
	else:
		return 2


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

def signup(uname, pwd, addr):
	peerlist = filereader("peerlist")
	if uname not in peerlist:
		peerlist[uname] = {"pwd" : pwd, "ip" : addr[0], "port" : addr[1], "last_seen" : time.time(), "status" : "online"}
		if filewriter("peerlist", peerlist):
			return 1
		else:
			return 3
	else:
		return 2


def handler(sock, addr):
	msg = pickle.loads(sock.recv(1024))
	print(msg)
	if msg["cat"] == "login":
		response = login(msg["uname"], msg["pwd"], addr)
		if response == 1:
			sock.send(pickle.dumps("success"))
		elif response == 2:
			sock.send(pickle.dumps("uname"))
		elif response == 3:
			sock.send(pickle.dumps("pwd"))
		else:
			sock.send(pickle.dumps("fail"))
	elif msg["cat"] == "create":
		response = signup(msg["uname"], msg["pwd"], addr)
		if response == 1:
			sock.send(pickle.dumps("success"))
		elif response == 2:
			sock.send(pickle.dumps("uname"))
		else:
			sock.send(pickle.dumps("fail"))
	elif msg["cat"] == "get":
		if msg["item"] == "peerlist":
			getpeerlist(sock)
		elif msg["item"] == "modulelist":
			getmodulelist(sock)
	elif msg["cat"] == "update":
		if msg["item"] == "peerlist":
			update_peerlist(msg["uname"], msg["pwd"], msg["status"])
		elif msg["item"] == "modulelist":
			update_modulelist(msg["uname"], msg["pwd"], msg["list"])



if __name__ == "__main__":
	try:
		if os.path.isfile("peerlist") == False:
			if filewriter("peerlist", {}) == False:
				print("Unable to create support files, aborting.")
		if os.path.isfile("modulelist") == False:
			if filewriter("modulelist", {}) == False:
				print("Unable to create support files, aborting.")
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(("0.0.0.0", 5465))
		sock.listen(10)
		while True:
			csock, caddr = sock.accept()
			t = threading.Thread(target = handler, args = (csock, caddr), daemon = True)
			t.start()
	except KeyboardInterrupt:
		print("\nExiting...")