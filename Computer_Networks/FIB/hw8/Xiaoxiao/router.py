import json
import logging

from logger_helper import setup_logger

logger = setup_logger('csen233hw8JiangXiaoxiao.log')


class Router:
    def __init__(self, nm):
        self.name = nm  # name of the router
        self.links = {}  # a dictionary of directly connected neighbors with link costs
        self.fib = {}  # Forwarding Information Base as a dictionary

    def addLink(self, l, c):
        self.links[l] = c

    def updateFib(self, destination, next_hop, cost):
        self.fib[destination] = (next_hop, cost)

    def sendData(self, dest, data):
        if dest in self.fib:
            next_hop, cost = self.fib[dest]
            # Packet encapsulation with destination name as header
            packet = {"header": {"destination": dest}, "data": data}
            # Simulate sending the packet to the next router
            return next_hop.recvData(packet)
        else:
            # Log the packet drop event
            logger.info(f"Router {self.name}: No FIB entry for destination {dest}. Dropping packet.")
            return False

    def recvData(self, packet):
        dest = packet["header"]["destination"]
        if dest == self.name:
            # Packet is for this router, so accept and discard the packet
            logger.info(f"Router {self.name}: Packet received. Data: {packet['data']}")
            return True
        else:
            # Packet is for another router, so forward it using FIB
            logger.info(f"Router {self.name}: Forwarding packet. Data: {packet['data']}")
            return self.sendData(dest, packet["data"])

    def __str__(self):
        return self.__repr__()

    # Friendly output of router info in JSON syntax
    def __repr__(self):
        str_repr = '{{"Router": "{}", '.format(self.name)
        if self.links:
            str_repr += '"Links": ' + json.dumps(self.links)
        if self.fib:
            fib_simple = {dest: (next_hop, cost) if isinstance(next_hop, str) else (next_hop.name, cost) for dest, (next_hop, cost) in self.fib.items()}
            str_repr += ', "FIB": ' + json.dumps(fib_simple)
        str_repr += '}'
        return str_repr




