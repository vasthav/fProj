import socket
import pickle
import os

def login():

def signup():

def setup():

def load_settings(): 

def get_sock():

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
				login()
			elif opt == "2":
				signup()
			elif opt == "3":
				setup()
			else:
				print("Incorrect Option")
	except KeyboardInterrupt:
		print("Exiting.")