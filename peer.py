#python 3.x code
#continue from initiate / select_operation functions

import socket
import pickle
import os


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
	pwd = input("Please enter your password : ")
	sock.connect((tracker_addr["ip"], tracker_addr["port"]))
	sock.send(pickle.dumps({"cat" : "login", "uname" : uname, "pwd" : pwd}))
	reply = pickle.loads(sock.recv(1024))
	sock.close()
	if reply == "success":
		print("Logged in successfully.")
		return (1, uname, pwd)



def signup(sock, tracker_addr):
	uname = input("Enter desired username : ")
	pwd = input("Enter desired password : ")
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



def select_operation(main_sock, tracker_addr, uname, pwd):
	print("What do you want to do?")
	print("1.\tVolunteer")
	print("2.\tInitiate")
	option = input("Please select option : ")
	if option == "1":
		volunteer(main_sock, tracker_addr, uname)
	elif option == "2":
		initiate(uname, pwd)
	else:
		print("Invalid option.")
		select_operation(main_sock, tracker_addr, uname)




def initiate(main_sock, tracker_addr, uname):
	main_sock.connect((tracker_addr["ip"], tracker_addr["port"]))




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


def volunteer():
	print("You have opted to volunteer")



def main_op():
	try:
		main_port, tracker_addr = initialize()
		main_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		main_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print("1.\tLogin")
		print("2.\tSign Up")
		print("3.\tSetup")
		option = input("Please select option : ")
		if option == "1":
			login_flag, uname, pwd = login(main_sock, tracker_addr) 
			if login_flag == 1:
				select_operation(main_sock, tracker_addr, uname, pwd)
			else:
				main_op()
		elif option == "2":
			signup(main_sock, tracker_addr)
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
	
