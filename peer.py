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


def login(sock, tracker_addr):
	uname = input("Please enter your username : ")
	pwd = getpass.getpass(prompt = "Please enter your password : ")
	sock.connect((tracker_addr["ip"], tracker_addr["port"]))
	sock.send(pickle.dumps({"cat" : "login", "uname" : uname, "pwd" : pwd}))
	reply = pickle.loads(sock.recv(1024))
	sock.close()
	if reply == "success":
		print("Logged in successfully.")
		return (1, uname, pwd)


def signup(sock, tracker_addr):
	uname = input("Enter desired username : ")
	pwd = getpass.getpass(prompt="Enter desired password : ")
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


def select_operation(tracker_addr, uname, pwd):
	print("What do you want to do?")
	print("1.\tVolunteer")
	print("2.\tInitiate")
	option = input("Please select option : ")
	if option == "1":
		volunteer(tracker_addr, uname, pwd)
	elif option == "2":
		initiate_comp(tracker_addr, uname, pwd)
	else:
		print("Invalid option.")
		select_operation(tracker_addr, uname)



def initiate_comp(sock, tracker_addr, uname):
	main_sock.connect((tracker_addr["ip"], tracker_addr["port"]))
	pass


def volunteer(tracker_addr, uname):
	print("You have opted to volunteer")
	msg = None
	main_sock = create_sock()
	main_sock.setblocking(0)
	main_sock.bind(("0.0.0.0", main_port))
	dict_of_addr = {}
	main_sock.listen(5)

	list_of_socks = [ main_sock ]
	while list_of_socks:
		readlist, writelist, exceptlist = select.select(list_of_socks, [], [], 0.7)
		for sock in readlist:
			if sock is main_sock:
				try:
					newsock, newaddr = sock.accept()
					newsock.setblocking(0)
					list_of_socks.append(newsock)
					dict_of_addr[newsock] = newaddr
				except BlockingIOError:
					pass
			else:
				msg = sock.recv(1024):
				if not msg:
					if sock in readlist:
						readlist.remove(sock)
					elif sock in writelist:
						writelist.remove(sock)
				else:
					print("calling process")
					vprocess(msg, sock, main_sock, tracker_addr, uname, pwd)
					# sock.send(pickle.dumps(result))
					list_of_socks.remove(sock)


def getmodule(modname, main_sock, tracker_addr):
	main_sock.send(pickle.dumps({"cat":"get", "item":"modulelist"}))
	content = pickle.loads(main_sock.recv(1024))
	for i in content:
		if modname == i["modname"]:
			# send request
			pass

def vprocess(msg, sock, main_sock, tracker_addr, uname, pwd):
	content = pickle.loads(msg)
	print(content)
	
	if content["cat"] == "getmodule":
		if os.path.isfile("./modules/"+content["modname"]+".py"):
			data = filereader("./modules/"+content["modname"]+".py")
			mains_sock.send(pickle.dumps(data))
			print("Requested Module Sent: ", content["modname"]+".py")
		else:
			print("Requested module does not exists")
			sock.send(pickle.dumps("Module Unavailable"))
		return "Module_Sent"

	elif content["cat"] == "request":
		choice = input("Do you want to volunteer? (Yes / No) ")
		if choice == "Yes" or choice == "yes" or choice == "y" or choice == "Y":
			print("Thank you for participating in the Project.")
			main_sock.send(pickle.dumps({"cat":"update", "item":"peerlist", "uname":uname, "pwd",pwd, "status": "busy"}))
			# recieve_job(job)
			# if not os.path.isfile("./modules/"+content["modname"]+".py"):
			# 	getmodule(modname, main_sock, tracker_addr)
			# result = module(job)
			# return result


def setup():
	main_port = input("Enter port no you want to listen to : ")
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

def create_sock():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# sock.setblocking(0)
	return sock


def main_op():
	try:
		sock = create_sock()
		main_port, tracker_addr = initialize()
		print("1.\tLogin")
		print("2.\tSign Up")
		print("3.\tSetup")
		option = input("Please select option : ")
		if option == "1":
			login_flag, uname, pwd = login(sock, tracker_addr) 
			if login_flag == 1:
				# sock = create_sock()
				select_operation(tracker_addr, uname, pwd)
			else:
				main_op()
		elif option == "2":
			signup(sock, tracker_addr)
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
	
