import random


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


super_knapsack = [1, 2, 4, 10, 20, 40]


def generate_multiplexer_and_modulus(super_knapsack):
    total_sum = sum(super_knapsack)

    # Generate modulus (m) greater than the sum of the private key
    modulus = random.randint(total_sum + 1, 2 * total_sum)

    # Generate a multiplexer (multiplier) with no common factors with m
    multiplexer = random.randint(2, modulus - 1)
    while gcd(multiplexer, modulus) != 1:
        multiplexer = random.randint(2, modulus - 1)

    return multiplexer, modulus


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


list = []
def generate_public_key(super_knapsack, multipexer, modulus):
    for each in super_knapsack:
        each_pub = (each * multipexer) % modulus
        list.append(each_pub)
    return list

k = generate_multiplexer_and_modulus(super_knapsack)
print(k)

kk = generate_public_key(super_knapsack, k[0], k[1])
print(kk)