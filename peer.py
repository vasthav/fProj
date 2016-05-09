# peer.py
# python 3.x code 
# continue from initiate_comp / select_operation functions

import os
import socket
import pickle
import select
import getpass


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
	print(pickle.loads(nsock.recv(1024)))
	sock.close()


def initiate(main_port, tracker_addr, uname, pwd):
	sock = create_sock(main_port)
	sock.connect((tracker_addr["ip"], tracker_addr["port"]))
	sock.send(pickle.dumps({"cat" : "get", "item" : "peerlist"}))
	peerlist = pickle.loads(sock.recv(1024))
	sock.close()
	print(peerlist)
	modpath = input("Enter path of module : ")
	if os.path.isfile(modpath) == True:
		command = "python3 " + modpath + " initiate"
		os.system(command)
	else:
		initiate(main_port, tracker_addr, uname, pwd)
	sock = create_sock(main_port)
	# sock.setblocking(0)
	# readlist = [ sock ]
	# sendsock = create_sock()
	# writelist = [ sendsock ]
	# dict_of_addr = {}
	# while True:
	# 	msg = None
	# 	readlist, writelist, exceptlist = select.select(readlist, writelist, [], 0.7)
	# 	for r_sock in readlist:
	# 		if r_sock is sock:
	# 			try:
	# 				newsock, newaddr = r_sock.accept()
	# 				newsock.setblocking(0)
	# 				readlist.append(newsock)
	# 				dict_of_addr[newsock] = newaddr
	# 			except (BlockingIOError, OSError):
	# 				pass
	# 		else:
	# 			msg = sock.recv(1024)
	# 			if msg:
	# 				process(msg, sock, dict_of_addr[sock])
	# 				readlist.remove(sock)
	# 				del dict_of_addr[sock]
	# 			else:
	# 				if sock in readlist:
	# 					readlist.remove(sock)
	# 				elif sock in writelist:
	# 					writelist.remove(sock)

	# 	print(readlist)
	# 	print(writelist)
	# 	for w_sock in writelist:
	# 		pk, pv = peerlist.popitem()
	# 		w_sock.connect((pv["ip"], pv["port"]))
	# 		w_sock.send(pickle.dumps({"cat" : "request"}))


	


	




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
	
