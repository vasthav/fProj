import pickle
from pprint import pprint

def show(fname):
	print("--------------------------------------------------------------")
	with open(fname, 'rb') as fd:
		while 1:
			try:
				s = pickle.load(fd)
				pprint(s)
			except (EOFError):
				break
	print("--------------------------------------------------------------")

def insfunc(fname, insob):
	with open(fname, 'ab') as fd:
		pickle.dump(insob, fd)


def logout(fname, uname):
	with open(fname, 'ab') as fd:
		insob = (uname, getpass(uname), getip(uname), getport(uname), "0")
		delfunc(fname, uname)
		insfunc(fname, insob)
	
def delfunc(fname, uname):
	with open("temp",'rb+') as ftemp:	
		with open(fname, 'rb+') as fd:
			while 1: 
				try:
					s = pickle.load(fd)
					if s[0] != uname:
						pickle.dump(s, ftemp)
				except (EOFError):
					break

	with open("temp", 'rb+') as ftemp:
		with open(fname, 'wb+') as fd:
			while 1:
				try:
					s = pickle.load(ftemp)
					pickle.dump(s, fd)
				except (EOFError):
					break

	with open("temp", "wb") as ftemp:
		pass

def uname_exits(fname, uname):
	with open(fname, 'rb') as fd:
		while 1:
			try:
				cmd = pickle.load(fd)
				if cmd["uname"] == uname:
					return 1
			except (EOFError):
				return 0
				break


def getpass(fname, uname):
	with open(fname, 'rb') as fd:
		while 1:
			try:
				s = pickle.load(fd)
				if s["uname"] == uname:
					return s["pwd"]
			except (EOFError):
				return None
				break

def getip(fname, uname):
	with open(fname, 'rb') as fd:
		while 1:
			try:
				s = pickle.load(fd)
				if s["uname"] == uname:
					return s[""]
			except (EOFError):
				return None
				break


def getport(fname, uname):
	with open(fname, 'rb') as fd:
		while 1:
			try:
				s = pickle.load(fd)
				if s["uname"] == uname:
					return s["listeningPort"]
			except (EOFError):
				return None
				break


def getnetstat(fname, uname):
	with open(fname, 'rb') as fd:
		while 1:
			try:
				s = pickle.load(fd)
				if s[0] == uname:
					return s[4]
			except (EOFError):
				return None
				break



if __name__ == '__main__':
# 	with open(fname, 'wb+') as fd:
# 		pickle.dump(("jesus", "christ", "127.0.0.1", "12345"), fd)
# 		pickle.dump(("dalai", "lama", "127.0.0.2", "12346"),fd)
# 		pickle.dump(("saviour", "christ", "127.0.0.3", "12347"),fd)

# 	insfunc(fname, ("jesus", "christ", "127.0.0.1", "12345"))
# 	insfunc(fname, ("dalai", "lama", "127.0.0.2", "12346"))
#   insfunc(fname, ("saviour", "christ", "127.0.0.3", "12347"))


	# Edit the filename to work on
	fname = "peerlist"

	show(fname)
	print(getpass(fname, "jesus"))
	print(getip(fname, "jesus"))
	print(getport(fname, "jesus"))
	print(getpass(fname, "vasthav"))
