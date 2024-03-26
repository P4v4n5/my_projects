# Name: Srinivasulu, Pavan Kumar
# Email: psrinivasulu@scu.edu

import logging
import sys
import random

from netemulate import netEmulator
from router import Router
from log import MyLogger  # Importing MyLogger class from log.py


class FIBDijkstra(netEmulator):

    def __init__(self):
        super().__init__()
        self.logger = MyLogger.setup_user1_logger()  # Initialize logger from MyLogger class


    def get_node_by_name(self, name):
        for node in self.routers:
            if node.name == name:
                return node
        return None

    def dijkstra(self, start, end):
        distance = {router.name: float('inf') for router in self.routers}
        predecessor = {}
        distance[start] = 0
        unvisited = set(router.name for router in self.routers)

        while unvisited:
            current = min(unvisited, key=lambda router: distance[router])
            unvisited.remove(current)

            if current == end or distance[current] == float('inf'):
                break

            for neighbour, cost in self.get_node_by_name(current).links.items():
                alt_route = distance[current] + cost
                if alt_route < distance[neighbour]:
                    distance[neighbour] = alt_route
                    predecessor[neighbour] = current

        path = []
        current = end
        if current in predecessor or current == start:
            while current is not None:
                path.insert(0, current)
                current = predecessor.get(current, None)
        else:
            self.logger.info(f"No path exists from {start} to {end}")
            return None, float('inf')

        # Update FIB for each router on the path
        for i in range(len(path) - 1):
            self.get_node_by_name(path[i]).update_fun_fib(path[-1], path[i + 1], distance[path[i + 1]] - distance[path[i]])

        return path, distance[end]

    def main(self):
        if len(sys.argv) < 4:
            self.logger.error("Usage: python Dijkstra.py <topology file> <start router> <end router>")
            sys.exit(1)

        topology_file, start_router, end_router = sys.argv[1], sys.argv[2], sys.argv[3]

        self.rtInit(topology_file)
        self.logger.info(f"Topology file that is considered is %s", topology_file)

        shortest_path, path_length = self.dijkstra(start_router, end_router)
        if shortest_path:
            self.logger.info(f"Shortest path from %s to %s is ---> %s", start_router, end_router, shortest_path)
            self.logger.info(f"Length of the shortest path is ---> %s", path_length)

            # Demonstrate sending a packet
            start_router_obj = self.get_node_by_name(start_router)
            if start_router_obj:
                start_router_obj.send_data(end_router, "Received the packet successfully")

            self.logger.info("\nTesting negative scenario: Packet drop simulation.")

            # randomly generating a high value of negative case
            random_number = random.randint(10000000, 20000000)
            invalid_router = "R" + str(random_number)

            self.logger.info(f"\nSending packet from %s to %s", start_router, invalid_router)
            if start_router_obj is not None:
                start_router_obj.send_data(invalid_router, "This packet should be dropped.")
        else:
            self.logger.error("Ooops!!, No path found between %s and %s.", start_router, end_router)


if __name__ == '__main__':
    fib = FIBDijkstra()
    fib.main()
