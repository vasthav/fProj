import argparse
import socket
import pickle

data = [[1, 2], [3, 4], [5, 6], [7, 8]]

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
	r = peersock.recv(1024)
	peersock.close()
	modsock.close()
	dat = pickle.loads(r)
	print(dat)
	result = dat[0] + dat[1]
	print(result)

	msock = create_sock(54321)
	msock.connect((peer_addr[0], peer_addr[1]))
	msock.send(pickle.dumps(result))
	msock.close()



def initiator():
	print("Initiating....")
	modsock = create_sock(54321)
	modsock.listen(5)
	peersock, peer_addr = modsock.accept()
	msg = pickle.loads(peersock.recv(1024))
	if msg == "data":
		peersock.send(pickle.dumps(data))
	peersock.close()
	modsock.close()

	modsock = create_sock(54321)
	modsock.listen(5)
	peersock, peer_addr = modsock.accept()
	result = pickle.loads(peersock.recv(1024))
	print(result)
	modsock.close()
	peersock.close()


parser = argparse.ArgumentParser()
parser.add_argument("controller")
args = parser.parse_args()
if args.controller == "solve":
	solver()
elif args.controller == "initiate":
	initiator()