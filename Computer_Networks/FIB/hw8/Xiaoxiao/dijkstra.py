# @Author
# xiaoxiao jiang > xjiang3@scu.edu

# @Usage
# To execute this program, simply run the following command in your terminal or command prompt:
# python dijkstra.py or python3 dijkstra.py

# @Description
# In the main function of this script, two routers are randomly selected from the network to serve as the source and destination for testing the sendData function. 
# Prior to this test, the shortest path between these two routers is calculated using the Dijkstra's algorithm from homework 7. 

# In the negative test scenario, a non-existent router 'R21' is chosen as the destination router. 
# The expected outcome is that the source router will report that there is no corresponding entry in its FIB for 'R21'. 
# This result should be observable both in the standard output (stdout) and the log file.

# Note: The FIB (Forwarding Information Base) of each router is not printed due to its large size, which would clutter the output.

from netemulate import netEmulator
import heapq
from logger_helper import setup_logger
import random

logger = setup_logger('csen233hw8JiangXiaoxiao.log')


class Dijkstra(netEmulator):
	def __init__(self):
		super().__init__()

	def calculate_and_distribute_fib(self):
		if len(self.routers) <= 0:
			logger.warning("Empty network!")
			return
		
		for source in self.routers:
			for dest in self.routers:
				if source.name == dest.name:
					continue
				path = self.dijkstra(source.name , dest.name)
				next_hop_name = path[1]
				next_hop = next((r for r in self.routers if r.name == next_hop_name), None)
				source.updateFib(dest.name, next_hop, self.calculate_path_cost(source.name, dest.name))



	def dijkstra(self, r1, r2):
		path = []
		pair = [r for r in self.routers if r.name == r1 or r.name == r2]
		if len(pair) != 2:
			return None

		# Homework code	
		# Initialization
		distances = {router.name: float('infinity') for router in self.routers}
		previous = {router.name: None for router in self.routers}
		distances[r1] = 0
		visited = {r1}  # This set will hold all the router name with known shortest distance
		# Priority queue: Use a heap queue to get the minimum distance router name
		pq = []
		source = next((r for r in pair if r.name == r1), None)
		for neighbor, cost in source.links.items():
			distances[neighbor] = cost
			previous[neighbor] = r1
			heapq.heappush(pq, (cost, neighbor))
			 
		# Loop
		while pq:
			# Find the router w not in visted such that D(w) is a minimum
			_, w = heapq.heappop(pq)
			if w in visited:
				continue
			
			# Add w to visted
			visited.add(w)
			
			if w == r2:
				break  # Found the shortest path to the target router

			# For each neighbor v of w not in visted
			w_router = next((router for router in self.routers if router.name == w), None)
			for v, cost in w_router.links.items():
				if v not in visited:
					# Update D(v) for each neighbor v of w and not in visted
					if distances[w] + cost < distances[v]:
						distances[v] = distances[w] + cost
						previous[v] = w
						heapq.heappush(pq, (distances[v], v))



		# Backtrace to reconstruct the shortest path from r1 to r2
		current_vertex = r2
		while current_vertex is not None:
			path.insert(0, current_vertex)
			current_vertex = previous[current_vertex]
		
		return path


	# This function calculates the shortest path cost from router r1 to router r2
	# It is designed to verify the correctness of dijkstra function above in test.py
	def calculate_path_cost(self, r1, r2):
		total_cost = 0
		path = self.dijkstra(r1, r2)
		if len(path) < 2:
			return total_cost 

		for i in range(len(path) - 1):
			current_router_name = path[i]
			next_router_name = path[i + 1]

			current_router = next((router for router in self.routers if router.name == current_router_name), None)

			if current_router and next_router_name in current_router.links:
				total_cost += current_router.links[next_router_name]
			else:
				return float('infinity')
			
		return total_cost

if __name__ == "__main__":
    filename = 'net.json'
    net = Dijkstra()
    net.rtInit(filename)

    net.calculate_and_distribute_fib()

    source_router, dest_router = random.sample(net.routers, 2)
    logger.info(f'Randomly choose two routers -- source router: {source_router.name}, dest router: {dest_router.name}')
    logger.info(f'Positive test: Trying to send data from {source_router.name} to {dest_router.name}')

    # positive test
    path = net.dijkstra(source_router.name, dest_router.name)
    short_path_cost = net.calculate_path_cost(source_router.name, dest_router.name)

    logger.info(f'Shortest path from {source_router.name} to {dest_router.name} shall be {path}')

    router = next((r for r in net.routers if r.name == source_router.name), None)
    router.sendData(dest_router.name, "hello world");

    logger.info(f'Negative test: Trying to send data from {source_router.name} to R21, which is not reachable in FIB')
    # negative test
    router.sendData('R21','shall not see this msg in stdout')