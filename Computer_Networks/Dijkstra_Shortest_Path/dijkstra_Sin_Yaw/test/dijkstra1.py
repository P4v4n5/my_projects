from netemulate import netEmulator
import sys

class Dijkstra(netEmulator):
    def __init__(self):
        super().__init__()

    def dijkstra(self, r1, r2):
        if r1 == r2:
            return [r1], 0

        # Helper function to get the router object by name
        def get_router_by_name(name):
            for router in self.routers:
                if router.name == name:
                    return router
            return None

        # Initialize distance dictionary with infinity for all routers
        distance = {router.name: float('inf') for router in self.routers}
        distance[r1] = 0

        # Initialize predecessor dictionary
        predecessor = {}

        # List of unvisited routers
        unvisited = [router.name for router in self.routers]

        while unvisited:
            # Get router with minimum distance
            min_router = min(unvisited, key=lambda x: distance[x])

            # Break if the target router is reached
            if min_router == r2:
                break

            # Remove the minimum router from unvisited
            unvisited.remove(min_router)

            # Update distances to neighbors
            router = get_router_by_name(min_router)
            for neighbor, cost in router.links.items():
                alt_distance = distance[min_router] + cost
                if alt_distance < distance[neighbor]:
                    distance[neighbor] = alt_distance
                    predecessor[neighbor] = min_router

        # Reconstruct the shortest path
        path = []
        current = r2
        while current != r1:
            path.insert(0, current)
            current = predecessor[current]
        path.insert(0, r1)

        # Calculate the length of the path
        path_length = sum(get_router_by_name(path[i]).links[path[i+1]] for i in range(len(path)-1))

        return path, path_length

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('need topology file')
        sys.exit(1)
    if len(sys.argv) <= 3:
        print('need node names')
        sys.exit(1)

    net = Dijkstra()
    print('loading {}'.format(sys.argv[1]))
    net.rtInit(sys.argv[1])
    print('net has {} routers'.format(len(net.routers)))

    # print out the path and length
    shortest_path, path_length = net.dijkstra(sys.argv[2], sys.argv[3])
    if shortest_path:
        print("Shortest path from {} to {}: {}".format(sys.argv[2], sys.argv[3], shortest_path))
        print("Length of the shortest path: {}".format(path_length))
    else:
        print("No path found between {} and {}.".format(sys.argv[2], sys.argv[3]))