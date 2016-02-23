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
                    c = Client(self.server.accept())
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

class Client(threading.Thread):
    # def __init__(self, (client,address)):
    def __init__(self, aval):
        threading.Thread.__init__(self)
        self.client = aval[0] #client
        self.address = aval[1] #address
        self.size = 1024

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
        f = open(fname,'rb')
        while True:
            l = f.read(1024)
            while (l):
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(1024)
            if not l:
                f.close()
                self.sock.close()
                break


    def command_handler(self):
        cmd = pickle.loads(self.client.recv(self.size))
        if cmd["category"] == "login":
            rval = self.authenticate(cmd, 0)
            if rval == 1:
                print("Login successful.")
                d = {"uname":cmd["uname"], "status":"ok"}
                ackdata = pickle.dumps(d)
                self.client.send(ackdata)
            else:
                print("Login failed.")
                d = {"uname":cmd["uname"], "status":"notok"}
                ackdata = pickle.dumps(d)
                self.client.send(ackdata)
                # self.client.close()

        elif cmd["category"] == "create":
            rval = self.authenticate(cmd, 1)
            if rval == 1:
                print("Account created successful.")
                d = {"uname":cmd["uname"], "status":"ok"}
                ackdata = pickle.dumps(d)
                self.client.send(ackdata)
            else:
                print("Account creation failed.")
                d = {"uname":cmd["uname"], "status":"notok"}
                ackdata = pickle.dumps(d)
                self.client.send(ackdata)
                # self.client.close()

        elif cmd["category"] == "message":
            if cmd["content"] == "peerlist":
                pass #sendfile("peerlist")

        elif cmd["category"] == "message":
            if cmd["content"] == "modlist":
                pass #sendfile("modlist")



    def run(self):
        running = 1
        while running:
            self.command_handler()
            # data = self.client.recv(self.size)


if __name__ == "__main__":
    s = Server()
    s.run() 