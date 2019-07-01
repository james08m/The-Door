#! /usr/bin/env/ python

import logging
import socket
import threading

BUFFER_SIZE = 50        # Usually 1024, but we want a fast response time
BAD_QUERY_LIMIT = 5     # Limit of bad queries tolerated

###################################################################
## Class Name: Client
## Parent : threading.Thread
## Input(s): id, address(IP+PORT), socket, servo and logger
## Description: The Client class purpose is to handle every clients
##              interactions with the server. Every time a client
##              connexion is made. The server instantiate a client
##              object, lunch the client thread and store it into a
##              list. Every active client thread is listening on
##              the socket for datas and process it like it should.
##
## Notes: This is where clients command and executed depending of
##        servo motor status.
###################################################################

class Client(threading.Thread):

    # Properly initialize client by initializing
    # the parent thread and by passing all
    # arguments needed to the client
    def __init__(self, id, addr, socket, servo, logger):
        threading.Thread.__init__(self)
        self.id = id
        self.ip = addr[0]
        self.port = addr[1]
        self.alive = True
        self.logger = logger
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
    # This method is the client's
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

                    self.logger.info("{} | CONNECT".format(self.get_info()))
                    self.socket.send("CONNECT ACK")         # Acknowledge to client
                    self.auth = True                        # Set authorization to True

                # Client request to put servo motor in idle position
                elif data == "IDLE":

                    if self.auth:
                        self.logger.info("{} | IDLE".format(self.get_info()))
                        self.socket.send("IDLE ACK")        # Acknowledge to client
                        self.servo.idle()
                    else:
                        self.socket.send("IDLE DENIED")     # Deny client

                # Client request to put servo motor in idle position
                elif data == "PSH":

                    if self.auth:
                        self.logger.info("{} | PSH".format(self.get_info()))
                        self.socket.send("PSH ACK")         # Acknowledge to client
                        self.servo.push()
                    else:
                        self.socket.send("PSH DENIED")      # Deny client

                else:
                    self.logger.warning("{} | QUERY IGNORED".format(self.get_info()))  # After too much bad queries connection is stopped
                    self.badquery += 1
                    self.socket.send("QUERY IGNORED")       # Tell client that query was ignored
                    
                    if(self.badquery == BAD_QUERY_LIMIT):
                        self.socket.send("DISCONNECT")      # Tell client that connection is terminated
                        self.close()
                    
            except socket.error as e:                   # When Socket exception is raised
                print self.logger.error("{} | {}".format(self.get_info(), e))
                
        self.servo.idle()                           # Put back servo motor in idle position for security purposes
        self.socket.close()                         # Close client socket
        self.logger.warning("{} | CLOSED".format(self.get_info()))


