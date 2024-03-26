# Miller-Rabin Random number generator
# Authored by Antoine Prudhomme, 2018
# From https://medium.com/@ntnprdhmm/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
#
import math
from random import randrange, getrandbits
def is_prime(n, k=128):
	""" Test if a number is prime
		Args:
		n -- int -- the number to test
		k -- int -- the number of tests to do
		return True if n is prime
	"""
	if n <= 1 or n % 2 == 0:
		return False

	if is_true_prime(n):
		return True
	
	# find r and s
	s = 0
	r = n - 1
	while r & 1 == 0:
		s += 1
		r //= 2
	# do k tests
	for _ in range(k):
		a = randrange(2, n - 1)
		x = pow(a, r, n)
		if x != 1 and x != n - 1:
			j = 1
			while j < s and x != n - 1:
				x = pow(x, 2, n)
				if x == 1:
					return False
				j += 1
				if x != n - 1:
					return False
	return True

# mathematically proven primality
def is_true_prime(n):
# first 100 prime numbers
	prime1000=(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
	89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
	181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271,
	277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
	383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479,
	487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
	601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
	709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823,
	827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
	947, 953, 967, 971, 977, 983, 991, 997)

	if n < 0:
		return False

	if n in prime1000:
		return True

	if n <= prime1000[len(prime1000)-1]**2:
		for k in [x for x in prime1000 if x < n]:
			if math.gcd(n, k) != 1:
				return False
		return True
	return False

def generate_prime_candidate(length):
	""" Generate an odd integer randomly
		Args:
		length -- int -- the length of the number to generate, in bits
		return a integer
	"""
	# generate random bits
	p = getrandbits(length)
	# apply a mask to set MSB and LSB to 1
	p |= (1 << length - 1) | 1
	return p

def generate_prime_number(length=1024):
	""" Generate a prime
		Args:
		length -- int -- length of the prime to generate, in          bits
		return a prime
	"""
	p = generate_prime_candidate(length)
	# keep generating while the primality test fail
	while not is_prime(p, 128):
		p = generate_prime_candidate(length)
	return p
