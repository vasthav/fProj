# function arguments are module list from peer, peer's username and file name of tracker's module list file.
# assumes that module list is received from peer as [ modName1, modName2 ]
# module list is stored as { "modName1" : [ "peerName1", "peerName2" ], "modName2" : [ "peerName3", "peerName4" ] }

def modListManipulator(peerModList, peerName, trackerModListFileName):
	trackerModList = pickle.loads(readFile(trackerModListFileName))
	for moduleName in peerModList:
		if moduleName in trackerModList:
			trackerModList[moduleName].append(peerName)
		else:
			trackerModList[moduleName] = [ peerName ]

	writeFile(trackerModListFileName, pickle.dumps(trackerModList))
