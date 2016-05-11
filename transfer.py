import struct

# def sender(sock, msg):
#     # Prefix each message with a 4-byte length (network byte order)
#     msg = struct.pack('>I', len(msg)) + msg
#     sock.sendall(msg)

# def receiver(sock):
#     # Read message length and unpack it into an integer
#     raw_msglen = recvall(sock, 4)
#     if not raw_msglen:
#         return None
#     msglen = struct.unpack('>I', raw_msglen)[0]
#     # Read the message data
#     return recvall(sock, msglen)

# def recvall(sock, n):
#     # Helper function to recv n bytes or return None if EOF is hit
#     data = ''
#     while len(data) < n:
#         packet = sock.recv(n - len(data))
#         if not packet:
#             return None
#         data += packet
#     return data

# module for transferring files - sizes upto 4GB
# call sender and receiver only
# recvall is an internal function to mirror sendall

import struct

# func to send file
def send_file(sock, fileName):
    with open(fileName, "rb") as inFile:
        data =  inFile.read()
        sender(sock, data)

# func to recv file
def recv_file(sock, fileName):
    with open(fileName, "wb+") as output:
        writeData = receiver(sock)
        output.write(writeData)

# data sender
def sender(sock, data):
    fileSize = len(data)
    #print("File size is "+str(fileSize))
    sock.sendall(struct.pack('!I', fileSize))
    sock.sendall(data)

# deta reciever
def receiver(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    #print(str(length))
    return recvall(sock, length)

# sendall mirror func
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf = buf + newbuf
        count = count - len(newbuf)
    return buf
