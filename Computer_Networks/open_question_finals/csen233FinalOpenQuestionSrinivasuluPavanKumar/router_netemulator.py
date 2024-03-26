# Maintainer: Srinivasulu, Pavan Kumar
# Email: psrinivasulu@scu.edu

import json
from log import MyLogger


# ---------------------------Router--------------------------
class Router():
    def __init__(self, nm, network):
        self.name = nm
        self.links = {}
        self.fib = {}
        self.network = network
        self.fib_iteration = 0
        self.logger = MyLogger.setup_user1_logger()  # Initialize logger from MyLogger class

    def startRoutingUpdate(self):
        return self.sendFibToNeighbors()

    def linkCostUpdations(self, l, new_cost):
        if l in self.links:
            self.links[l] = new_cost
            if l in self.fib:
                self.fib[l] = (new_cost, l)
            return True
        return False

    def addLink(self, l, c):
        self.links[l] = c
        self.fib[l] = (c, l)

    def recvData(self, packet):
        header = packet.get('header', {})
        if header.get('packet_type') == 'ROUTING' and header.get('destination') == 'FLOOD':
            self.logger.info(f"Router {self.name} successfully received data from {header.get('sender')} ---> {packet['data']}")
            return self.updateFib(packet['data'], header.get('sender'))
        return False

    def updateFib(self, new_routes, sender):
        fib_updated = False
        for dest, (cost, next_hop) in new_routes.items():
            if dest == self.name:
                continue
            if dest not in self.fib or cost + self.links[sender] < self.fib[dest][0]:
                self.logger.info(
                    f"Router {self.name} updating Forwarding table for destination {dest} via {sender} with cost {cost + self.links[sender]}")
                self.fib[dest] = (cost + self.links[sender], sender)
                fib_updated = True
        if fib_updated:
            self.fib_iteration += 1
            self.sendFibToNeighbors()
        return fib_updated

    def sendFibToNeighbors(self):
        packet = {
            'header': {
                'packet_type': 'ROUTING',
                'destination': 'FLOOD',
                'sender': self.name,
                'iteration': self.fib_iteration
            },
            'data': self.fib
        }
        for neighbor in self.links:
            if neighbor in self.network.routers:
                self.network.routers[neighbor].recvData(packet)
        self.logger.info(f"Router {self.name} sent Forwarding table to neighbors --> {self.fib}")


# ---------------------------Net Emulator--------------------------
class NetworkEmulator():
    def __init__(self):
        self.routers = {}
        self.router_updated = True
        self.logger = MyLogger.setup_user1_logger()  # Initialize logger from MyLogger class

    def displayFIBTables(self, stage):
        self.logger.info(f"\n{stage} FIB Tables:")
        for router in self.routers.values():
            self.logger.info(f"Router --> {router.name}: {router.fib}")

    def initializeRouteUpdation(self):
        while self.router_updated:
            self.router_updated = False
            for router in self.routers.values():
                if router.startRoutingUpdate():
                    self.router_updated = True

    def rtInit(self, fname):
        try:
            with open(fname, 'r') as f:
                net = json.load(f)
        except Exception as e:
            self.logger.error(f'Error: {e}')
            return None

        for rtr in net['Network']:
            r = Router(rtr['Router'], self)
            for l, c in rtr['Links'].items():
                r.addLink(l, c)
            self.routers[r.name] = r

    def linkDown(self, router_name, link_name, new_cost):
        router = self.routers.get(router_name)
        if router and router.linkCostUpdations(link_name, new_cost):
            self.router_updated = True  # Trigger the routing update process again
            self.logger.info(f"Link {link_name} from Router {router_name} cost updated to {new_cost}.")
        else:
            self.logger.error(f"Failed to update cost for link {link_name} from Router {router_name}.")
