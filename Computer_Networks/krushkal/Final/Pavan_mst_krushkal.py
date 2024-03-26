# Maintainer: Srinivasulu, Pavan Kumar
# Email: psrinivasulu@scu.edu

from netemulate import netEmulator
import sys
from log import MyLogger  # Importing MyLogger class from log.py
import json


class KruskalAlgorithm(netEmulator):
    def __init__(self):
        super().__init__()
        self.logger = MyLogger.setup_user1_logger()

    def main_execution(self):

        # to check if the json file is fed or not
        if len(sys.argv) <= 1:
            self.logger.error('You have not fed net.json file, So I cannot proceed further!!')
            sys.exit(1)

        self.rtInit(sys.argv[1])  # Using the current instance instead of creating a new one
        self.logger.info('The total number of routers present in the network are %s', len(self.routers))

        minimum_spanning_tree, total_cost = self.kruskal_algorithm()  # Using the current instance
        if minimum_spanning_tree:
            self.logger.info("--**--**--**--Minimum Spanning Tree--**--**--**--")
            for edge in minimum_spanning_tree:
                self.logger.info("(From: %s ---> To: %s | Cost: %s) ", edge[0], edge[1], edge[2])
            self.logger.info("Total Cost of MST: %s", total_cost)
        else:
            self.logger.info("Minimum Spanning tree, Not found!!")

    def kruskal_algorithm(self):

        def find_root(parent, node):
            if parent[node] == node:
                return node
            return find_root(parent, parent[node])

        def unite(parent, rank, x, y):
            x_root = find_root(parent, x)
            y_root = find_root(parent, y)

            if rank[x_root] < rank[y_root]:
                parent[x_root] = y_root
            elif rank[x_root] > rank[y_root]:
                parent[y_root] = x_root
            else:
                parent[y_root] = x_root
                rank[x_root] += 1

        parent = {}
        rank = {}

        for router in self.routers:
            parent[router.name] = router.name
            rank[router.name] = 0

        edges = []
        for router in self.routers:
            for neighbor, cost in router.links.items():
                edges.append((router.name, neighbor, cost))
        edges.sort(key=lambda x: x[2])

        mst_list = []
        total_cost = 0

        for edge in edges:
            source, destination, cost = edge
            x = find_root(parent, source)
            y = find_root(parent, destination)

            if x != y:
                mst_list.append((source, destination, cost))
                unite(parent, rank, x, y)
                total_cost += cost

        return mst_list, total_cost


if __name__ == '__main__':
    mst = KruskalAlgorithm()
    mst.main_execution()
