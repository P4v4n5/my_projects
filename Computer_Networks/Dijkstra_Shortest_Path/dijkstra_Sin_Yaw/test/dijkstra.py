from netemulate import netEmulator
import sys
import random

class Dijkstra(netEmulator):
	def __init__(self):
		super().__init__()

	# Homework #5
	def dijkstra(self, r1, r2):
		path = []
		pair = [r for r in self.routers if r.name == r1 or r.name == r2]
		if len(pair) != 2:
			return None
		# homework code goes here
		return path;

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('need topology file')
	if len(sys.argv) <= 3:
		print('need node names')

	net=Dijkstra()
	print('loading {}'.format(sys.argv[1]))
	net.rtInit(sys.argv[1])
	print('net has {} routers'.format(len(net.routers)))

	# this is where you test your homework
	# assign two routers and find their shortest path
	# than print out the path
	shortest = net.dijkstra(sys.argv[2], sys.argv[3])
