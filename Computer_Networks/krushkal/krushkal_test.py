# Maintainer: Srinivasulu, Pavan Kumar
# Email: psrinivasulu@scu.edu

from netemulate import netEmulator
import sys
from log import MyLogger  # Importing MyLogger class from log.py
import json


class KruskalAlg(netEmulator):
    def __init__(self):
        super().__init__()
        self.logger = MyLogger.setup_user1_logger()

    def kruskal(self):
        def find_parent(parent, node):
            if parent[node] == node:
                return node
            return find_parent(parent, parent[node])

        def union(parent, rank, x, y):
            x_root = find_parent(parent, x)
            y_root = find_parent(parent, y)

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

        mst = []
        total_cost = 0

        for edge in edges:
            src, dest, cost = edge
            x = find_parent(parent, src)
            y = find_parent(parent, dest)

            if x != y:
                mst.append((src, dest, cost))
                union(parent, rank, x, y)
                total_cost += cost

        return mst, total_cost

    def main(self):
        # to check if the json file is fed or not
        if len(sys.argv) <= 1:
            self.logger.error('You have not fed net.json file, So I cannot proceed further!!')
            sys.exit(1)

        net = KruskalAlg()
        net.rtInit(sys.argv[1])
        self.logger.info('The total number of routers present in the network is %s', len(net.routers))

        minimum_spanning_tree, total_cost = net.kruskal()
        if minimum_spanning_tree:
            self.logger.info("--**--**--**--Minimum Spanning Tree--**--**--**--")
            for edge in minimum_spanning_tree:
                self.logger.info("From: %s ---> To: %s | Cost: %s ", edge[0], edge[1], edge[2])
            self.logger.info("Total Cost of MST: %s",total_cost)
        else:
            self.logger.info("No minimum spanning tree found.")

if __name__ == '__main__':
    mst = KruskalAlg()
    mst.main()
