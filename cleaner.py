#! /usr/bin/env/ python

import logging
import threading
import time

###################################################################
## Class Name: Cleaner
## Parent : threading.Thread
## Input(s): clients_list, logger
## Description: The Cleaner class purpose is to clean the server of
##              all unused clients of the server clients list.
##              since a server can be run for a long amount of time
##              we want to make sure the memory is used properly
##              to prevent any buffer overflow and server crashed.
##              It also make it much easier to monitor how much
##              client are connected and reduce the memory weight
##              for the Raspberry PI
##
## Notes:
###################################################################


class Cleaner(threading.Thread):

    # Properly initialize server cleaner by initializing
    # the parent thread and by passing the clients list in param
    def __init__(self, client_list, logger):
        threading.Thread.__init__(self)
        self.alive = True
        self.logger = logger
        self.clients = client_list

    # Redefinition of the run() method from
    # the parent class "threading.Thread".
    # This method is the server
    # cleaner thread life cycle
    def run(self):
        self.logger.info("Cleaner started")
        while self.alive:
            time.sleep(10)  # Wait 10sec and clean again

            if self.alive:      # Make sure cleaner wasn't closed while sleep
                self.remove()   # Remove closed client from List
                self.display()  # Display alive clients info

    def close(self):
        self.logger.info("Closing cleaner..")
        self.alive = False

    def remove(self):
        to_remove = []                       # Create list where client to be removed will be store

        for client in self.clients:          # Go through all clients' in List
            if not client.alive:             # If the client thread is not alive
                to_remove.append(client)     # Add client to the "to be removed" list

        for client in to_remove:             # Remove not alive clients found
            self.logger.info("Removing {}".format(client.get_info()))
            self.clients.remove(client)      # Remove clients from clients' List

    def kill(self):                          # This method is called when server is closed to kill the remaining clients
        for client in self.clients:
            client.close()

    def display(self):                       # Display the remaining clients and their information
        for client in self.clients:
            print client.get_info()