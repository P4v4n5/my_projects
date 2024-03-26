#Name: Srinivasulu, Pavan Kumar
#Email: psrinivasulu@scu.edu

import json
import logging
from log import MyLogger  # Importing MyLogger class from log.py

class Router:
    def __init__(self, name):
        self.name = name  # name of the router
        self.links = {}  # routers connecting with each other and their costs
        self.fib = {}  # Forwarding Information Base
        self.network = None
        self.logger = MyLogger.setup_user1_logger()

    def addLink(self, l, c):
        self.links[l] = c

    def update_fun_fib(self, destination, next_hop, total_cost):
        self.fib[destination] = (next_hop, total_cost)

    def send_data(self, dest, data):
        
        if dest in self.fib:
            next_hop_name, cost = self.fib[dest]
            self.logger.info(f"Router %s: Sending packet to %s via %s with cost: %s", self.name, dest, next_hop_name, cost)
            if next_hop_name == dest:
                self.network.get_node_by_name(dest).receive_data(self.name, dest, data)
            else:
                self.network.get_node_by_name(next_hop_name).send_data(dest, data)
        else:
            self.logger.info(f"Source router ---> %s | Target router ---> %s. There is no FIB entry for %s. Hence, the packet got dropped.", self.name, dest, dest)

    def receive_data(self, src, dest, data):
        self.logger.info(f"Router %s: Packet received from %s. Data: %s", dest, src, data)

    def __repr__(self):
        str = '{{"Router": "{}", "Links": {}}}'.format(self.name, json.dumps(self.links))
        return str
