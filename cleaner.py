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
        print "Cleaner started."
        while self.alive:
            time.sleep(30)  # Wait 30sec

            if self.alive:      # Make sure cleaner wasn't closed while sleep
                self.remove()   # Remove closed client from List
                self.display()  # Display alive clients info

    def close(self):
        self.alive = False
        print "Cleaner closed"

    def remove(self):
        to_remove = []
        for client in self.clients:          # Go through all clients in List
            if not client.alive:             # If the client thread is not alive
                print "Removing client : ", client.get_info()
                to_remove.append(client)

        for client in to_remove:
            self.clients.remove(client)  # Remove client from clients List

    def kill(self):
        for client in self.clients:
            client.close()

    def display(self):
        for client in self.clients:
            print client.get_info()