#! /usr/bin/env/ python

from servo import *
from client import *
from cleaner import *

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
        self.cleaner = Cleaner(self.clients)        # Initialize server client cleaner
        self.servo = Servo()

        self.server.bind((self.ip, self.port))      # Bind ip address and port to socket

    # Safely close the server
    def close(self):
        print "\r[i] Closing server.."
        self.servo.idle()                           # Put back servo motor in idle position for security reason ;)
        self.servo.close()                          # Properly close the servo motor instance

        self.cleaner.close()                        # Stop server cleaner thread
        self.cleaner.join()                         # Wait that the cleaner thread end
        self.cleaner.kill()                         # Kill remaining clients threads
        print "[i] Cleaner closed."

        self.server.close()
        print "[i] Server closed."

    # Redefinition of the run() method from
    # the parent class "threading.Thread".
    # This method is actually the server's
    # thread life cycle
    def run(self):
        print "[i] Starting server.."

        self.server.listen(1)  # Start listening
        self.cleaner.start()   # Start client cleaner thread
        time.sleep(0.5)        # Wait half a second to le thread print message

        print "[i] Server started."
        print "[i] Waiting for connections.."
        try:
            while self.alive:

                soc, addr = self.server.accept()            # Wait for a client connection

                print "[i] New connection from : ", addr
                client_id = len(self.clients)
                client_thread = Client(client_id, addr, soc, self.servo)    # Create a new client instance
                self.clients.append(client_thread)                          # Add client instance to the clients List
                self.clients[client_id].start()                             # Immediately start client thread

            self.close()

        except KeyboardInterrupt:
            self.close()
