"""
This is the Tracker code 
---------------------
"""

#!/usr/bin/env python

import select
import socket
import sys
import threading
import pickle
import util
import os
from pprint import pprint
import transfer

# Server class which deals with peer and server them
class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 12345
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    # function to open the socket for listening to various peers
    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error as message:
            if self.server:
                self.server.close()
            print("Could not open socket: ", message)
            sys.exit(1)

    # server class handler function
    def run(self):
        self.open_socket()
        input = [self.server,sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    c = peer(self.server.accept())
                    c.start()
                    self.threads.append(c)

        self.server.close()
        for c in self.threads:
            c.join()


# peer class for handling different peer requests
class peer(threading.Thread):
    # def __init__(self, (peer,address)):
    def __init__(self, aval):
        threading.Thread.__init__(self)
        self.peer = aval[0] #peer
        self.address = aval[1] #address
        self.size = 1024
        self.uname = None
        print("Got connetion form : ", self.address[0],":", self.address[1])

    # function for peer authentication
    def authenticate(self, cmd, n):
        if n == 0:
            if util.uname_exits("peerlist", cmd["uname"]) == 1:
                if cmd["pwd"] == util.getpass("peerlist", cmd["uname"]):
                    self.uname = cmd["uname"]
                    return 1
            else: 
                return 0

        if n == 1:
            if util.uname_exits("peerlist", cmd["uname"]) == 0:
                d = {"uname":cmd["uname"], "pwd":cmd["pwd"], "ip": self.address[0], "port":cmd["port"], "status":"active"}
                util.insfunc("peerlist", d)
                self.uname = cmd["uname"]
                return 1
            else:
                return 2
        # return uname  
        
    # function to handle peer requests
    def command_handler(self):
        # cmd = pickle.loads(self.peer.recv(self.size))
        cmd = pickle.loads(transfer.receiver(self.peer))
        print("request recieved: ")
        pprint(cmd)

        # if login request
        if cmd["type"] == "login":
            rval = self.authenticate(cmd, 0)
            print("rval : .. ", rval)
            if rval == 1:
                print("Login successful.")
                d = {"type":"rlogin", "content":"yes"}
                ackdata = pickle.dumps(d)
                transfer.sender(self.peer, ackdata)
                reply = pickle.loads(transfer.receiver(self.peer))
                pprint(reply)
                print(self.uname, "has modulelist: ")
                pprint(reply["modlist"])
                util.modupdate(reply, self.uname, "modulelist")
                

            else:
                print("Login failed.")
                d = {"type":"rlogin", "content":"no"}
                ackdata = pickle.dumps(d)
                transfer.sender(self.peer, ackdata)
            return 1

        # if signup request
        elif cmd["type"] == "signup":
            rval = self.authenticate(cmd, 1)
            print("authenticated : ", rval)
            if rval == 1:
                print("Account created successful.")
                d = {"type":"rsignup", "content":"yes"}
                ackdata = pickle.dumps(d)
                transfer.sender(self.peer, ackdata)
                reply = pickle.loads(transfer.receiver(self.peer))
                pprint(reply)
                print(self.uname, "has modulelist: ")
                pprint(reply["modlist"])
                util.modupdate(reply, self.uname, "modulelist")

            elif rval == 2:
                print("Username already exists.")
                d = {"type":"rsignup", "content":"exists"}
                ackdata = pickle.dumps(d)
                transfer.sender(self.peer, ackdata)

            elif rval == 0:
                print("Account creation failed.")
                d = {"type":"rsignup", "content":"no"}
                ackdata = pickle.dumps(d)
                transfer.sender(self.peer, ackdata)

            return 1

        # if file download requested
        elif cmd["type"] == "get":
            # if peerlist if requested
            if cmd["content"] == "peerlist":
                print("sending peerlist file...")
                util.makepeerlist("peerlist")
                transfer.send_file(self.peer, "demopeerlist")
                print("Done!")

            # if module list is requested
            elif cmd["content"] == "modlist":
                print("sending modulelist file...")
                transfer.send_file(self.peer, "modulelist")
                print("Done!")
            return 1

        # if the peer wants to close the connection
        elif cmd["type"] == "quit":
            print("peer closed connection")
            return 0


    # peer class handler
    def run(self):
        running = 1
        while running:
            running = self.command_handler()
            # data = self.peer.recv(self.size)


if __name__ == "__main__":
    print("Server UP and running...")
    s = Server()
    s.run() 