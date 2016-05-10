# peer.py
# python 3.x code 
# continue from initiate_comp / select_operation functions

import os
import socket
import pickle
import select
import getpass
import threading
import time
import transfer
import queue


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


def call_module(modname):
	try:
		fd = open(modname+".py", "r")
		content = fd.read()
		exec(content)
		return True
	except Exception as e:
		print("Module error : \n" + str(e))
		return False


def login(port, tracker_addr):
	sock = create_sock(port)
	uname = input("Please enter your username : ")
	pwd = getpass.getpass(prompt = "Please enter your password : ")
	sock.connect((tracker_addr["ip"], tracker_addr["port"]))
	sock.send(pickle.dumps({"cat" : "login", "uname" : uname, "pwd" : pwd}))
	reply = pickle.loads(sock.recv(1024))
	sock.close()
	if reply == "success":
		print("Logged in successfully.")
		return (1, uname, pwd)
	else:
		print("Log in failed.")
		return (0, None, None)


def signup(port, tracker_addr):
	uname = input("Enter desired username : ")
	pwd = getpass.getpass(prompt="Enter desired password : ")
	sock = create_sock(port)
	sock.connect((tracker_addr["ip"], tracker_addr["port"]))
	sock.send(pickle.dumps({"cat" : "create", "uname" : uname, "pwd" : pwd}))
	reply = pickle.loads(sock.recv(1024))
	sock.close()
	if reply == "success":
		print("Account created successfully.")
	elif reply == "exists":
		print("Username already exists.")
	elif reply == "fail":
		print("Account creation failed.")


def select_operation(main_port, tracker_addr, uname, pwd):
	print("What do you want to do?")
	print("1.\tVolunteer")
	print("2.\tInitiate")
	option = input("Please select option : ")
	if option == "1":
		volunteer(main_port, tracker_addr, uname, pwd)
	elif option == "2":
		initiate(main_port, tracker_addr, uname, pwd)
	else:
		print("Invalid option.")
		select_operation(main_port, tracker_addr, uname)



def volunteer(main_port, tracker_addr, uname, pwd):
	print("You have selected to volunteer.")
	sock = create_sock(main_port)
	sock.listen(4)
	nsock, naddr = sock.accept()

	r = nsock.recv(1024)
	print(pickle.loads(r))

	s = nsock.send(pickle.dumps("yes"))
	print("s: ", s)
	nsock.close()
	sock.close()

	sock = create_sock(main_port)
	sock.listen(4)
	nsock, naddr = sock.accept()
	r = nsock.recv(1024)
	print(pickle.loads(r))

	nsock.send(pickle.dumps({"content": True, "result":10}))
	nsock.close()
	sock.close()
	

# def initiate_sender(main_port, tracker_addr, uname, pwd, peerlist):
# 	print("Sending requests....")
# 	sock = create_sock()
# 	while peerlist:
# 		pk, pv = peerlist.popitem()
# 		sock.connect((pv[0], pv[1]))
# 		sock.sender(pickle.dumps({"cat": "request"}))


def peer_ready(peer):
	sock = create_sock()
	sock.connect((peer["ip"], peer["port"]))
	sock.send(pickle.dumps({"cat" : "request"}))
	
	r = sock.recv(1024)
	sock.close()
	
	response = pickle.loads(r)

	if response == "yes":
		print(response, "is the response")
		return True
	else:
		print(response, "is the response")
		return False

		

def initiate2(main_port, tracker_addr, uname, pwd, modpath):
	seg_job = [[1, 2], [3, 4], [5, 6], [7, 8]]
	job_status = [False, False, False, False]
	job_remaining = 4

	results = [None for x in range(0, len(seg_job))]
	assigned = []

	q = queue.Queue()
	
	while True:
		threads = [None for x in range(0, len(seg_job))]
		sock = create_sock(main_port)
		sock.connect((tracker_addr["ip"], tracker_addr["port"]))
		sock.send(pickle.dumps({"cat" : "get", "item" : "peerlist"}))
		peerlist = pickle.loads(sock.recv(1024))
		sock.close()
		
		if job_remaining == 0:
			break

		for i in range(0, len(seg_job)):
			if job_status[i] == False:
				peer_found = False
				# if uname in peerlist:
				try:
					del peerlist[uname]
				except:
					pass
				for peer in peerlist:
					if peer not in assigned:
						if peer_ready(peerlist[peer]) == True:
							threads[i] = threading.Thread(target = solve_job, args = (peerlist[peer], seg_job[i], q), daemon = True)
							threads[i].start()
							peer_found = True
							assigned.append(peer)

				if not peer_found:
					break

		#Wait for threads to complete
		for i in range(0, len(seg_job)):
			if threads[i] is not None:
				threads[i].join()
				result = q.get()
				print(result[0])
				if result[0] == True:
					job_remaining = job_remaining - 1
					results[i] = result[1]

		#If there are no threads to wait for, it means that no jobs were sent successfully.
		#Wait for a random amount of time so that someone may come online.
		for i in range(0, len(seg_job)):
			if threads[i] is not None:
				pass
		time.sleep(20)




def solve_job (host, job, q):
	print((host["ip"], host["port"]))
	sock = create_sock()
	sock.connect((host["ip"], host["port"]))

	# checking if the peer is online -  redundant
	# sock.send(pickle.dumps({"cat" : "request"}))
	# r = sock.recv(1024)
	# response = pickle.loads(r)

	# sending job
	sock.send(pickle.dumps(job))
	r = sock.recv(1024)
	response = pickle.loads(r)
	if response["content"] == False:
		ret = [False, None]
	else:
		ret = [True, response["result"]]
	# sock.send(pickle.dumps(job))
	# r = sock.recv(1024)
	# result = pickle.loads(r)
	
	q.put(ret)
	return ret







def initiate(main_port, tracker_addr, uname, pwd):
	sock = create_sock(main_port)
	sock.connect((tracker_addr["ip"], tracker_addr["port"]))
	sock.send(pickle.dumps({"cat" : "get", "item" : "peerlist"}))
	r = sock.recv(1024)
	peerlist = pickle.loads(r)
	sock.close()
	print(peerlist)
	modpath = input("Enter path of module : ")
	if os.path.isfile(modpath) == True:
		command = "python3 " + modpath + " initiate"
		os.system(command)
	else:
		initiate(main_port, tracker_addr, uname, pwd)
	sock = create_sock()
	sock.connect
	initiate2(main_port, tracker_addr, uname, pwd, modpath)
	# sock = create_sock(main_port)
	# sock.setblocking(0)
	# sendsock = create_sock()
	# readlist = [ sock ]
	# writelist = [ sendsock ]
	# dict_of_addr = {}
	# sock.listen(10)
	# print("after listening")
	# while True:
	# 	print("Entering loop")
	# 	readlist, writelist, exceptlist = select.select(readlist, writelist, [], 0.7)
	# 	for rsock in readlist:
	# 		if rsock is sock:
	# 			try:
	# 				print("Listening for incoming....")
	# 				newsock, newaddr = rsock.accept()
	# 				newsock.setblocking(0)
	# 				readlist.append(newsock)
	# 				dict_of_addr[newsock] = newaddr
	# 			except BlockingIOError:
	# 				pass
	# 		else:
	# 			msg = rsock.recv(1024)
	# 			if msg:
	# 				print(pickle.loads(msg))
	# 				readlist.remove(sock)
	# 				del dict_of_addr[sock]
	# 			else:
	# 				if sock in readlist:
	# 					readlist.remove(sock)
	# 				elif sock in writelist:
	# 					writelist.remove(sock)
	# 	for wsock in writelist:
	# 		print("Entering send section")
	# 		if peerlist:
	# 			pk, pv = peerlist.popitem()
	# 			if pk != uname:
	# 				try:
	# 					wsock.connect((pv["ip"], pv["port"]))
	# 					wsock.send(pickle.dumps({"cat" : "request"}))
	# 					#wsock.close()
	# 				except BlockingIOError:
	# 					pass
	#threading.Thread(target = initiate_sender, args = (main_port, tracker_addr, uname, pwd, peerlist), daemon = True).start()
	#time.sleep(10)


def setup():
	main_port = int(input("Enter port no you want to listen to : "))
	tracker_ip = input("Enter IP address of tracker : ")
	tracker_port = int(input("Enter port no of tracker : "))
	filewriter("settings", {"port" : main_port, "tracker_addr" : {"ip" : tracker_ip, "port" : tracker_port}})


def initialize():
	content = filereader("settings")
	if content == {}:
		setup()
		return initialize()
	elif content == False:
		setup()
		return initialize()
	else:
		return (content["port"], content["tracker_addr"])

def create_sock(port = None):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# sock.setblocking(0)
	if port:
		sock.bind(("0.0.0.0", port))
	return sock


def main_op():
	try:
		main_port, tracker_addr = initialize()
		print("1.\tLogin")
		print("2.\tSign Up")
		print("3.\tSetup")
		option = input("Please select option : ")
		if option == "1":
			login_flag, uname, pwd = login(main_port, tracker_addr) 
			if login_flag == 1:
				# sock = create_sock()
				select_operation(main_port, tracker_addr, uname, pwd)
			else:
				main_op()
		elif option == "2":
			signup(main_port, tracker_addr)
			# sock = create_sock()
			main_op()
		elif option == "3":
			setup()
			main_op()
		else:
			print("Invalid option.")
			main_op()
	except KeyboardInterrupt:
		print("\nExiting....")


if __name__ == "__main__":
	main_op()
	
