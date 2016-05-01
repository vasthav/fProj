import socket
import pickle
import os

def login(settings):
	uname = input("Enter username : ")
	pwd = input("Enter password : ")
	sock = get_sock(settings["main_port"])
	sock.connect((settings["tracker_ip"], settings["tracker_port"]))
	sock.send(pickle.dumps({"cat" : "login", "uname" : uname, "pwd" : pwd}))
	if pickle.loads(sock.recv(1024)) == "success":
		print("Logged in successfully.")
		return (True, uname, pwd)
	else:
		return (False, None, None)



def signup(settings):
	uname = input("Enter username : ")
	pwd = input("Enter password : ")
	sock = get_sock(settings["main_port"])
	sock.connect((settings["tracker_ip"], settings["tracker_port"]))
	sock.send(pickle.dumps({"cat" : "create", "uname" : uname, "pwd" : pwd}))
	response = pickle.loads(sock.recv(1024))
	if response == "success":
		print("Account created successfully.")
	elif response == "fail":
		print("Account creation failed.")
	elif response == "exists":
		print("Username already exists.")



def setup():
	peer_port = input("Enter port no to listen on : ")
	tr_ip = input("Enter ip of tracker : ")
	tr_port = input("Enter port of tracker : ")
	fd = open("settings", "wb")
	fd.write(pickle.dumps({"main_port" : int(peer_port), "tracker_ip" : tr_ip, "tracker_port" : int(tr_port)}))
	fd.close()



def load_settings():
	try:
		fd = open("settings", "rb")
		contents = fd.read()
		return pickle.loads(contents)
	except:
		setup()
		return load_settings()



def get_sock(port_no):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	if port_no:
		sock.bind(("0.0.0.0", port_no))
	return sock



def initiate_comp(settings, uname, pwd):
	# desc = input("Enter description for your computation.")
	# modname = input("Enter name of module required.")
	# sock = get_sock(None)
	# sock.connect((settings["tracker_ip"], settings["tracker_port"]))
	# sock.send(pickle.dumps({"cat" : "get", "item" : "peerlist"}))
	# peerlist = pickle.loads(sock.recv(1024))
	# print(peerlist)
	# online_list_socks = []
	# accept_list = []
	# for peer in peerlist:
	# 	if peer["status"] == "online":
	# 		sock = get_sock(None)
	# 		sock.connect((peer["ip"], peer["port"]))
	# 		online_list_socks.append(sock)
	# while online_list_socks:
	# 	readlist, writelist, exceptlist = select.select(online_list_socks, [], [], 0.7)
	# 	for sock in readlist:
	# 		msg = pickle.loads(sock.recv(1024))
	# 		if msg["response"] == "accept":
	# 			accept_list.append(sock)
	# 			online_list_socks.remove(sock)
	# 		else:
	# 			online_list_socks.remove(sock)
	# 			sock.close()
	# 	for sock in writelist:
	# 		sock.send(pickle.dumps({"cat" : "volunteer_request", "description" : desc, "module" : modname}))
	pass
	


def volunteer_comp(settings, uname, pwd):
	pass


def select_op(settings, uname, pwd):
	while True:
		print("What do you want to do?")
		print("1.\tInitiate Computation")
		print("2.\tVolunteer in a Computation")
		print("3.\tGo Back")
		opt = input("Please select an option : ")
		if opt == "1":
			initiate_comp(settings, uname, pwd)
		elif opt == "2":
			volunteer_comp(settings, uname, pwd)
		elif opt == "3":
			break
		else:
			print("Invalid option.")



if __name__ == "__main__":
	try:
		settings = load_settings()
		sock = get_sock(settings["main_port"])
		while True:
			print("1.\tLogin")
			print("2.\tSignup")
			print("3.\tChange Settings")
			opt = input("Please choose appropriate option : ")
			if opt == "1":
				login_flag, uname, pwd = login(settings)
				if login_flag == True:
					select_op(settings, uname, pwd)
				else:
					print("Login failed.")
			elif opt == "2":
				signup(settings)
			elif opt == "3":
				setup()
			else:
				print("Incorrect Option")
	except KeyboardInterrupt:
		print("Exiting.")