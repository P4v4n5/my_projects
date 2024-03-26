# Maintainer: Srinivasulu, Xiaoxiao Kumar
# Email: psrinivasulu@scu.edu

from netemulate import netEmulator
import sys
from log import MyLogger  # Importing MyLogger class from log.py
import json


class PathFinder(netEmulator):
    def __init__(self):
        super().__init__()
        self.logger = MyLogger.setup_user1_logger()  # Initialize logger from MyLogger class

    def main(self):

        # to check if the provided router names are valid or not
        router_list = []
        with open(sys.argv[2]) as f:
            data = json.load(f)
            router_data = data["Network"]
            for each in router_data:
                router_list.append(each["Router"])

        if sys.argv[2] not in router_list or sys.argv[3] not in router_list:
            self.logger.error('Invalid Router name!! Please provide valid router names')
            sys.exit(1)

        # to check if the json file is fed or not
        if len(sys.argv) <= 1:
            self.logger.error('You have not fed net.json file, So I cannot proceed further!!')
            sys.exit(1)

        # to check if user has given correct number of router names
        if len(sys.argv) <= 3:
            self.logger.error('You might have not given required number of router nodes. Please ensure you give two routers.')
            sys.exit(1)

        self.logger.info('Loading and parsing through the file, {}'.format(sys.argv[1]))
        self.rtInit(sys.argv[1])

        self.logger.info('Total number of routers present in {0} are ---> {1}'.format(sys.argv[1], len(self.routers)))

        shortest_path, path_length = self.find_shortest_path(sys.argv[2], sys.argv[3])
        if shortest_path:
            self.logger.info("Shortest path from {} to {} is ---> {}".format(sys.argv[2], sys.argv[3], shortest_path))
            self.logger.info("Length of the shortest path is ---> {}".format(path_length))
        else:
            self.logger.error("Ooops!!, No path found between {} and {}.".format(sys.argv[2], sys.argv[3]))

    def find_shortest_path(self, start_node, end_node):
        if start_node == end_node:
            self.logger.warning("*-*-*-*-*-*-*-*---Start node and the End node are the same!---*-*-*-*-*-*-*-*")
            return [start_node], 0

        def get_node_by_name(name):
            for node in self.routers:
                if node.name == name:
                    return node
            return None

        distances = {node.name: float('inf') for node in self.routers}
        distances[start_node] = 0

        predecessors = {}

        unvisited = [node.name for node in self.routers]

        while unvisited:
            min_node = min(unvisited, key=lambda x: distances[x])

            if min_node == end_node:
                break

            unvisited.remove(min_node)

            current_node = get_node_by_name(min_node)
            for neighbor, cost in current_node.links.items():
                alt_distance = distances[min_node] + cost
                if alt_distance < distances[neighbor]:
                    distances[neighbor] = alt_distance
                    predecessors[neighbor] = min_node

        path = []
        current = end_node
        while current != start_node:
            path.insert(0, current)
            current = predecessors[current]
        path.insert(0, start_node)

        path_length = sum(get_node_by_name(path[i]).links[path[i + 1]] for i in range(len(path) - 1))

        return path, path_length


if __name__ == '__main__':
    path_finder = PathFinder()
    path_finder.main()
