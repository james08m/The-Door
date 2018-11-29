#! /usr/bin/env/ python

import socket
import threading
import time

from servo import *
from client import *

BUFFER_SIZE = 50  # Normally is 1024, but we want a fast response time

################
#!#  Server  #!#
################

class Server(threading.Thread):
    def __init__(self):

        # Initialise attributs
        threading.Thread.__init__(self)
        self.alive = True
        self.ip = '192.168.10.200'
        self.port = 5340
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.servo = Servo()

        # Binding socket and start lestening
        self.server.bind((self.ip, self.port))
        self.server.listen(1)

    # Close server safely
    def close(self):
        print "\rClosing server.."
        
        # Make sure servo motor is in idle position
        self.servo.idle()
        
        # Kill clients threads
        for client in self.clients:
            client.close()

        # Wait 2sec to make sure clients thread are closed
        time.sleep(2)
        self.server.close()
        print "Server closed"

    # Server main loop and starting method
    def run(self):
        print "Starting server"
        try:
            client_id = 0
            while self.alive:

                print "Waiting for a connection.."
                soc, addr = self.server.accept()

                print "New connection from : ", addr
                client_thread = Client(client_id, addr, soc, self.servo)
                client_thread.start()
                self.clients.append(client_thread)
                client_id += 1

            self.close()

        except KeyboardInterrupt:
            self.close()

####################
#!# Main Program #!#
####################

if __name__ == "__main__":
    server = Server()
    server.run()
