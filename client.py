#! /usr/bin/env/ python

import socket
import threading
import time

from servo import *

BUFFER_SIZE = 50  # Normally is 1024, but we want a fast response time
BAD_QUERY_LIMIT = 5

################
#!#  Client  #!#
################

class Client(threading.Thread):
    def __init__(self, id, addr, socket, servo):
        threading.Thread.__init__(self)
        self.id = id
        self.ip = addr[0]
        self.port = addr[1]
        self.alive = True
        self.socket = socket
        self.servo = servo
        self.badquery = 0

    def close(self):
        self.alive = False
    
    def info(self):
        info = str(self.ip) + ":" + str(self.port) + " id=" + str(self.id)
        return info

    def run(self):
        while self.alive:
            try:
                data = self.socket.recv(BUFFER_SIZE)
                
                if data == "":
                    self.close()
                elif data == "PSH":
                    print self.info() + " | PSH"
                    self.socket.send("ACK")
                    self.servo.push()
                elif data == "IDLE":
                    print self.info() + " | IDLE"
                    self.socket.send("ACK")
                    self.servo.idle()
                elif data == "CONNECT":
                    print self.info() + " | CONNECT"
                    self.socket.send("ACK")
                else:
                    print self.info() + " | BAD QUERY " # After too much bad queries the connection is stopped
                    self.badquery += 1
                    
                    if(self.badquery == BAD_QUERY_LIMIT):
                        self.close()
                    
            except socket.error as e: # When Socket exception is raised
                print e
                
        self.servo.idle()
        self.socket.close()
        print "[!] " + self.info() + " | CLOSED"


