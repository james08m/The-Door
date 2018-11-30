#! /usr/bin/env/ python

import socket
import threading
import time

from servo import *
from client import *

BUFFER_SIZE     = 50                # Usually 1024, but we want a fast response time
SERVER_IP       = '192.168.10.200'  # IP statically assigned to my Raspberry Pi on the LAN
SERVER_PORT     = 5340

##################################
#!#  Server : threading.Thread #!#
##################################

class Server(threading.Thread):

    # Properly initialize server by initializing
    # the parent thread and by initializing
    # the server socket with the right information
    def __init__(self):

        threading.Thread.__init__(self)
        self.alive = True
        self.ip = SERVER_IP
        self.port = SERVER_PORT
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []                           # Initialize clients List
        self.servo = Servo()

        self.server.bind((self.ip, self.port))      # Bind ip address and port to socket
        self.server.listen(1)                       # Socket start listening

    # Safely close the server
    def close(self):
        print "\rClosing server.."
        self.servo.idle()                           # Put back servor motor in idle position for security reason ;)
        self.servo.close()                          # Properly close the servo motor instance

        for client in self.clients:                 # Kill clients threads
            client.close()

        time.sleep(2)                               # Wait 2sec to make sure clients thread are closed
        self.server.close()
        print "Server closed"

    # Redefinition of the run() method from
    # the parent class "threading.Thread".
    # This method is actually the server's
    # thread life cycle
    def run(self):
        print "Server started"
        print "Waiting for connections.."
        try:
            client_id = 0                           # Next client ID to be assign
            while self.alive:

                soc, addr = self.server.accept()            # Wait for a client connection

                print "New connection from : ", addr
                client_thread = Client(client_id, addr, soc, self.servo)    # Create a new client instance
                client_thread.start()                                       # Immediately start client thread
                self.clients.append(client_thread)                          # Add client instance to the clients List
                client_id += 1

            self.close()

        except KeyboardInterrupt:
            self.close()

########################
#!# Run Main Program #!#
########################

if __name__ == "__main__":
    server = Server()
    server.run()
