#! /usr/bin/env/ python

import logging
import socket
import threading

BUFFER_SIZE = 50        # Usually 1024, but we want a fast response time
BAD_QUERY_LIMIT = 5     # Limit of bad queries tolerated

##################################
#!#  Client : threading.Thread #!#
##################################

class Client(threading.Thread):

    # Properly initialize client by initializing
    # the parent thread and by passing all
    # arguments needed to the client
    def __init__(self, id, addr, socket, servo):
        threading.Thread.__init__(self)
        self.id = id
        self.ip = addr[0]
        self.port = addr[1]
        self.alive = True
        self.auth = True
        self.socket = socket
        self.servo = servo
        self.badquery = 0

    # Overloading operator <
    def __lt__(self, other):
        return self.id < other.id

    # Overloading operator <=
    def __le__(self, other):
        return self.id <= other.id

    # Overloading operator ==
    def __eq__(self, other):
        return self.id == other.id

    # Overloading operator !=
    def __ne__(self, other):
        return self.id != other.id

    # Overloading operator >
    def __gt__(self, other):
        return self.id > other.id

    # Overloading operator >=
    def __ge__(self, other):
        return self.id >= other.id

    # Overloading __str__ buildin python Object
    # This method is called when when printing client 
    def __str__(self):
        return str(self.id)
        
    # Terminate the thread instance
    def close(self):
        self.alive = False

    # Return a string of informations about the client.
    # Give the client IP address, port and id on the server
    def get_info(self):
        info = str(self.ip) + ":" + str(self.port) + " id=" + str(self.id)
        return info

    # Redefinition of the run() method from
    # the parent class "threading.Thread".
    # This method is actually the client's
    # thread life cycle
    def run(self):
        while self.alive:
            try:

                data = self.socket.recv(BUFFER_SIZE)    # Receiving client data from socket

                # Empty data terminate the client thread. Usually received when client close the connection
                if data == "":
                    self.close()

                # Client request access to servo motor
                elif data == "CONNECT":

                    print "[w] " + self.get_info() + " | CONNECT"
                    self.socket.send("CONNECT ACK")         # Acknowledge to client
                    self.auth = True                        # Set authorization to True

                # Client request to put servo motor in idle position
                elif data == "IDLE":

                    if self.auth:
                        print "[w] " + self.get_info() + " | IDLE"
                        self.socket.send("IDLE ACK")        # Acknowledge to client
                        self.servo.idle()
                    else:
                        self.socket.send("IDLE DENIED")     # Deny client

                # Client request to put servo motor in idle position
                elif data == "PSH":

                    if self.auth:
                        print "[w] " + self.get_info() + " | PSH"
                        self.socket.send("PSH ACK")         # Acknowledge to client
                        self.servo.push()
                    else:
                        self.socket.send("PSH DENIED")      # Deny client

                else:
                    print "[w] " + self.get_info() + " | QUERY IGNORED"  # After too much bad queries connection is stopped
                    self.badquery += 1
                    self.socket.send("QUERY IGNORED")       # Tell client that query was ignored
                    
                    if(self.badquery == BAD_QUERY_LIMIT):
                        self.socket.send("DISCONNECT")      # Tell client that connection is terminated
                        self.close()
                    
            except socket.error as e:                   # When Socket exception is raised
                print "[e] " + self.get_info() + " | " + e
                
        self.servo.idle()                           # Put back servor motor in idle position for security reason ;)
        self.socket.close()                         # Close client socket
        print "[w] " + self.get_info() + " | CLOSED"


