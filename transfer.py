# module for transferring files - sizes upto 4GB
# call sender and receiver only
# recvall is an internal function to mirror sendall
import struct

def send_file(sock, fileName):
	with open(fileName, "rb") as inFile:
		data =  inFile.read()
		sender(sock, data)

def recv_file(sock, fileName):
	with open(fileName, "wb+") as output:
		writeData = receiver(sock)
		output.write(writeData)

def sender(sock, data):
	fileSize = len(data)
	#print("File size is "+str(fileSize))
	sock.sendall(struct.pack('!I', fileSize))
	sock.sendall(data)

def receiver(sock):
	lengthbuf = recvall(sock, 4)
	length, = struct.unpack('!I', lengthbuf)
	#print(str(length))
	return recvall(sock, length)

def recvall(sock, count):
	buf = b''
	while count:
		newbuf = sock.recv(count)
		if not newbuf:
			return None
		buf = buf + newbuf
		count = count - len(newbuf)
	return buf
