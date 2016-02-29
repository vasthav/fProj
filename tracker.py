#!/usr/bin/env python

import select
import socket
import sys
import threading
import pickle
import fmanager
import os
from pprint import pprint

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 12345
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

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

                # elif s == sys.stdin:
                #     # handle standard input
                #     junk = sys.stdin.readline()
                #     running = 0
        # close all threads
        self.server.close()
        for c in self.threads:
            c.join()

class peer(threading.Thread):
    # def __init__(self, (peer,address)):
    def __init__(self, aval):
        threading.Thread.__init__(self)
        self.peer = aval[0] #peer
        self.address = aval[1] #address
        self.size = 1024
        print("Got connetion form : ", self.address[0],":", self.address[1])

    def authenticate(self, cmd, n):
        if n == 0:
            if fmanager.uname_exits("peerlist", cmd["uname"]) == 1:
                if cmd["pwd"] == fmanager.getpass("peerlist", cmd["uname"]):
                    return 1
            else: 
                return 0

        if n == 1:
            if fmanager.uname_exits("peerlist", cmd["uname"]) == 0:
                val = cmd
                dat = val.pop("category")
                pprint(dat)
                fmanager.insfunc("peerlist", dat)
                return 1
            else:
                return 0
        # return uname  
        
    def sendfile(self, fname):
        try:
            f = open(fname,'rb')
            while True:
                # print("sending file...")
                l = f.read(1024)
                while (l):
                    self.peer.send(l)
                    # print('Sent ', l)
                    l = f.read(1024)
                if not l:
                    print("completed")
                    self.peer.send(pickle.dumps("CLOSEEOF"))
                    f.close()
                    break
        except IOError:
            print("file doent exits.")
            


    def command_handler(self):
        cmd = pickle.loads(self.peer.recv(self.size))
        pprint(cmd)
        if cmd["category"] == "login":
            rval = self.authenticate(cmd, 0)
            if rval == 1:
                print("Login successful.")
                d = {"uname":cmd["uname"], "status":"ok"}
                ackdata = pickle.dumps(d)
                self.peer.send(ackdata)
            else:
                print("Login failed.")
                d = {"uname":cmd["uname"], "status":"notok"}
                ackdata = pickle.dumps(d)
                self.peer.send(ackdata)
                # self.peer.close()

        elif cmd["category"] == "create":
            rval = self.authenticate(cmd, 1)
            if rval == 1:
                print("Account created successful.")
                d = {"uname":cmd["uname"], "status":"ok"}
                ackdata = pickle.dumps(d)
                self.peer.send(ackdata)
            else:
                print("Account creation failed.")
                d = {"uname":cmd["uname"], "status":"notok"}
                ackdata = pickle.dumps(d)
                self.peer.send(ackdata)
                # self.peer.close()

        elif cmd["category"] == "message":
            if cmd["content"] == "getpeerlist":
                print("sending file...")
                self.sendfile("peerlist")

        elif cmd["category"] == "message":
            if cmd["content"] == "getmodlist":
                print("sending file...")
                self.sendfile("modlist")



    def run(self):
        running = 1
        while running:
            self.command_handler()
            # data = self.peer.recv(self.size)


if __name__ == "__main__":
    print("Server UP and running...")
    s = Server()
    s.run() 