import json
from log import MyLogger

class NetworkEmulator:
    class Router:
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
                print(f"Router {self.name} received data from {header.get('sender')}: {packet['data']}")
                return self.updateFib(packet['data'], header.get('sender'))
            return False

        def updateFib(self, new_routes, sender):
            fib_updated = False
            for dest, (cost, next_hop) in new_routes.items():
                if dest == self.name:
                    continue
                if dest not in self.fib or cost + self.links[sender] < self.fib[dest][0]:
                    print(f"Router {self.name} updating FIB for destination {dest} via {sender} with cost {cost + self.links[sender]}")
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
            print(f"Router {self.name} sent FIB to neighbors: {self.fib}")

        def startRoutingUpdate(self):
            return self.sendFibToNeighbors()

        def linkCostUpdations(self, l, new_cost):
            if l in self.links:
                self.links[l] = new_cost
                if l in self.fib:
                    self.fib[l] = (new_cost, l)
                return True
            return False

    def __init__(self):
        self.routers = {}
        self.router_updated = True
        self.logger = MyLogger.setup_user1_logger()  # Initialize logger from MyLogger class

    def rtInit(self, fname):
        try:
            with open(fname, 'r') as f:
                net = json.load(f)
        except Exception as e:
            print(f'Error: {e}')
            return None

        for rtr in net['Network']:
            r = self.Router(rtr['Router'], self)
            for l, c in rtr['Links'].items():
                r.addLink(l, c)
            self.routers[r.name] = r

    def displayFIBTables(self, stage):
        print(f"\n{stage} FIB Tables:")
        for router in self.routers.values():
            print(f"Router {router.name}: {router.fib}")

    def initializeRouteUpdation(self):
        while self.router_updated:
            self.router_updated = False
            for router in self.routers.values():
                if router.startRoutingUpdate():
                    self.router_updated = True

    def linkDown(self, router_name, link_name, new_cost):
        router = self.routers.get(router_name)
        if router:
            if router.linkCostUpdations(link_name, new_cost):
                self.router_updated = True  # Trigger the routing update process again
                print(f"Link {link_name} from Router {router_name} cost updated to {new_cost}.")
            else:
                print(f"Failed to update cost for link {link_name} from Router {router_name}. Link may not exist.")
        else:
            print(f"Failed to find router with name {router_name}.")
            return

if __name__ == '__main__':
    net = NetworkEmulator()
    net.rtInit("topology.json")
    net.displayFIBTables("Initial")
    net.initializeRouteUpdation()
    net.displayFIBTables("Final")
    print("Simulating link down...")
    net.linkDown("Router1", "Link1", 999999)
    print("Recomputing routes after link cost update:")
    net.initializeRouteUpdation()
    net.displayFIBTables("Final FIB Tables after link cost update:")
