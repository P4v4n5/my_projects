#!/usr/bin/env python3
import argparse
import socket
import random
import math
import millerrabin

# Desired key length
# Use it to compute the number of bytes to hold the value
keyLength = 128
byteLen = math.ceil((keyLength+2)/8)
byteLen = byteLen + byteLen % 2

def isPrimitiveRoot(m, p):
	return math.gcd(m, p) == 1

# Diffie-Hellman Key Exchange
# This code runs on both sides.  Side "A" runs without argument
# Side "B" then runs with "host" and "port" as reported from side "A"
def dhExchange(host=None, port=None):
	# Each side has its own "secret".  It need not be a large number
	toAddr = None
	mySecret = random.randint(10000,20000)
	udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	if host is not None:
		# this is side "B"
		# it generate a pair of numbers that are relatively prime.
		# One of them must be longer than the desire key bit length. Here we try for 128
		# bits.
		baseLow  = 250
		baseHi   = 1000
		prime = millerrabin.generate_prime_number(keyLength+1)
		modulo = random.randint(baseLow, baseHi)
		while not isPrimitiveRoot(modulo, prime):
			modulo = random.randint(baseLow, baseHi)
		senddata = modulo.to_bytes(4,'big')+prime.to_bytes(byteLen,'big')
		toAddr = (host, port)
		udpSocket.sendto(senddata,toAddr)
		print(f'Send p={prime} ({len(bin(prime)[2:])} bits) and g={modulo} to {toAddr}')
	else:
		bindToLocal(udpSocket)
		# Then both parties enter the loop, both waiting for the 1st message from the other side
		data, toAddr = udpSocket.recvfrom(1024);
		modulo = int.from_bytes(data[:4],'big')
		prime  = int.from_bytes(data[4:],'big')
		print(f'Received p={prime} ({len(bin(prime)[2:])} bits) g={modulo}')

	print(f'Use local secret = {mySecret}')
	msg = doSecret(mySecret, modulo, prime)
	udpSocket.sendto(msg,toAddr)
	data,addr = udpSocket.recvfrom(1024)
	msg = int.from_bytes(data, 'big')
	print(f'Received {msg} bits={len(bin(msg)[2:])}')
	msg = doSecret(mySecret, msg, prime)
	shared = int.from_bytes(msg, 'big')
	print(f'   Key = {shared} ({len(bin(shared)[2:])} bits)')
	udpSocket.close()

def bindToLocal(udpSocket):
		s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('www.scu.edu', 80))
		localhost = s.getsockname()[0]
		s.close()
		udpSocket.bind((localhost, 0))
		port = udpSocket.getsockname()[1]	# that's the port number
		print('{} @ {} accepting UDP'.format(socket.gethostbyname(localhost), port))

def doSecret(s, m, p):
	n = (m ** s) % p
	print(f'Compute {m}^{s} % {p}')
	print(f'Result = {n} ({len(bin(n)[2:])} bits)')
	return n.to_bytes(byteLen, 'big')

if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument('-w', '--wait', action='store_true', help="wait for msg first")
	parser.add_argument('-s', '--host', action='store', default=None, help="server mame")
	parser.add_argument('-p', '--port', type=int, help="server port")
	args = parser.parse_args()

	dhExchange(args.host, args.port)
