
import logging
from netemulate import netEmulator
import sys

class Kruskal(netEmulator):
    def __init__(self):
        super().__init__()

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

def configure_logger():
    logger = logging.getLogger('KruskalLogger')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(message)s")
    file_handler = logging.FileHandler('kruskal.log', mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Please provide a topology file.')
        sys.exit(1)

    logger = configure_logger()
    logger.info('Loading {}'.format(sys.argv[1]))

    net = Kruskal()
    net.rtInit(sys.argv[1])
    logger.info('The network has {} routers.'.format(len(net.routers)))

    minimum_spanning_tree, total_cost = net.kruskal()
    if minimum_spanning_tree:
        logger.info("Minimum Spanning Tree:")
        for edge in minimum_spanning_tree:
            logger.info("{} -- {} -> {}".format(edge[0], edge[2], edge[1]))
        logger.info("Total Cost of MST: {}".format(total_cost))
    else:
        logger.info("No minimum spanning tree found.")
