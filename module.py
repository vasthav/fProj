import argparse
import socket
import pickle
import os
import transfer

def filereader(fname):
	try:
		if os.path.getsize(fname) == 0:
			return {}
		fd = open(fname, "rb")
		content = fd.read()
		data = content
		fd.close()
		return data
	except (IOError, pickle.PicklingError) as e:
		return False


def create_sock(port = None):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# sock.setblocking(0)
	if port:
		sock.bind(("127.0.0.1", port))
	return sock

def solver():
	print("Solve mode")
	modsock = create_sock(54321)
	modsock.listen(5)
	peersock, peer_addr = modsock.accept()
	r = transfer.receiver(peersock)
	peersock.close()
	modsock.close()
	dat = pickle.loads(r)
	print("Job Received: ")
	print(dat)
	result = 0
	for num in dat:
		result = result + num
	print("Result Calculated: ", result)

	msock = create_sock(54321)
	msock.connect((peer_addr[0], peer_addr[1]))
	transfer.sender(msock, pickle.dumps(result))
	msock.close()



def initiator():
	print("Initiating....")
	data = filereader("rand")
	lines = data.splitlines()
	to_send = []
	count = 0
	sub = []
	for line in lines:
		sub.append(int(line))
		count += 1
		if count == 100:
			to_send.append(sub)
			count = 0
			sub = []


	print(to_send)


	modsock = create_sock(54321)
	modsock.listen(5)
	peersock, peer_addr = modsock.accept()
	msg = pickle.loads(peersock.recv(1024))
	if msg == "data":
		transfer.sender(peersock, pickle.dumps(to_send))
	peersock.close()
	modsock.close()

	modsock = create_sock(54321)
	modsock.listen(5)
	peersock, peer_addr = modsock.accept()
	result = pickle.loads(transfer.receiver(peersock))
	print("Result received from peers: ", result)
	final_result = 0
	for ans in result:
		final_result += ans
	
	print("final result", final_result)
	modsock.close()
	peersock.close()


parser = argparse.ArgumentParser()
parser.add_argument("controller")
args = parser.parse_args()
if args.controller == "solve":
	solver()
elif args.controller == "initiate":
	initiator()