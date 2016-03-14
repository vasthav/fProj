# function arguments are module list from peer, peer's username and file name of tracker's module list file.
# assumes that module list is received from peer as [ modName1, modName2 ]
# module list is stored as { "modName1" : [ "peerName1", "peerName2" ], "modName2" : [ "peerName3", "peerName4" ] }

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

def modListManipulator(peerModList, peerName, trackerModListFileName):
	trackerModList = pickle.loads(readFile(trackerModListFileName))
	for moduleName in peerModList:
		if moduleName in trackerModList:
			trackerModList[moduleName].append(peerName)
		else:
			trackerModList[moduleName] = [ peerName ]

	writeFile(trackerModListFileName, pickle.dumps(trackerModList))
