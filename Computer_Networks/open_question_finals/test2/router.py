from log import MyLogger
class Router():
    def __init__(self, nm, network):
        self.name = nm
        self.links = {}
        self.fib = {}
        self.network = network
        self.fib_iteration = 0
        self.logger = MyLogger.setup_user1_logger()  # Initialize logger from MyLogger class

    def addLink(self, l, c):
        self.links[l] = c
        self.fib[l] = (c, l)

    def recvData(self, packet):
        header = packet.get('header', {})
        if header.get('packet_type') == 'ROUTING' and header.get('destination') == 'FLOOD':
            self.logger.info(f"Router {self.name} received data from {header.get('sender')}: {packet['data']}")
            return self.updateFib(packet['data'], header.get('sender'))
        return False

    def updateFib(self, new_routes, sender):
        fib_updated = False
        for dest, (cost, next_hop) in new_routes.items():
            if dest == self.name:
                continue
            if dest not in self.fib or cost + self.links[sender] < self.fib[dest][0]:
                self.logger.info(f"Router {self.name} updating FIB for destination {dest} via {sender} with cost {cost + self.links[sender]}")
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
        self.logger.info(f"Router {self.name} sent FIB to neighbors: {self.fib}")

    def startRoutingUpdate(self):
        return self.sendFibToNeighbors()

    def linkCostUpdations(self, l, new_cost):
        if l in self.links:
            self.links[l] = new_cost
            if l in self.fib:
                self.fib[l] = (new_cost, l)
            return True
        return False