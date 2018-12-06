#! /usr/bin/env/ python

import threading
import time

##################################
#!# Cleaner : threading.Thread #!#
##################################

class Cleaner(threading.Thread):

    # Properly initialize server cleaner by initializing
    # the parent thread and by passing the clients list in param
    def __init__(self, client_list):
        threading.Thread.__init__(self)
        self.alive = True
        self.clients = client_list

    # Redefinition of the run() method from
    # the parent class "threading.Thread".
    # This method is actually the server
    # cleaner thread life cycle
    def run(self):
        while self.alive:
            for client in self.clients:          # Go through all clients in List
                if not client.alive:             # If the client thread is not alive
                    self.clients.remove(client)  # Remove client from clients List
            time.sleep(60)  # Wait 1 minute