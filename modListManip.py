# function arguments are module list from peer, peer's username and file name of tracker's module list file.

def modListManipulator(peerModList, peerName, trackerModListFileName):
	trackerModList = pickle.loads(readFile(trackerModListFileName))
	for moduleName in peerModList:
		if moduleName in trackerModList:
			trackerModList[moduleName].append(peerName)
		else:
			trackerModList[moduleName] = [ peerName ]

	writeFile(trackerModListFileName, pickle.dumps(trackerModList))
