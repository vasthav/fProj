# function arguments are module list from peer, peer's username and file name of tracker's module list file.
# assumes that module list is received from peer as [ modName1, modName2 ]
# module list is stored as { "modName1" : [ "peerName1", "peerName2" ], "modName2" : [ "peerName3", "peerName4" ] }

import pickle
from pprint import pprint

def show(fname):
	print("---------------------------------------------------------------------------")
	with open(fname, 'rb') as fd:
		while 1:
			try:
				s = pickle.load(fd)
				pprint(s)
			except (EOFError):
				break
	print("---------------------------------------------------------------------------")

def insfunc(fname, insob):
	with open(fname, 'ab') as fd:
		pickle.dump(insob, fd)

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

def modupdate(msg, uname, fname):
	mlist = msg["modlist"]
	with open("temp",'rb+') as ftemp:	
		with open(fname, 'rb+') as fd:
			while 1: 
				try:
					data = pickle.load(fd)
					if data["modname"] in mlist:
						data["peers"].add(uname)
						mlist.remove(data["modname"])
					pprint(data)
					pickle.dump(data, ftemp)
				except (EOFError):
					break

			if len(mlist) > 0:
				for mod in mlist:
					data = {"modname":mod, "peers":{uname}}
					pickle.dump(data, ftemp)
					pprint(data)

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