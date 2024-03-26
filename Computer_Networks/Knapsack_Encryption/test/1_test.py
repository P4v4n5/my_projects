import random
from itertools import combinations
import socket
import pickle
import time


def generate_superincreasing_knapsack(n_elements):
    knapsack = []
    total = 0
    for i in range(n_elements):
        element = total + 1  # Make sure the next element is greater than the sum of previous elements
        knapsack.append(element)
        total += element
    return knapsack


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def generate_multiplexer_and_modulus(super_knapsack):
    total_sum = sum(super_knapsack)

    # Generate modulus (m) greater than the sum of the private key
    modulus = random.randint(total_sum + 1, 2 * total_sum)

    # Generate a multiplexer (multiplier) with no common factors with modulus
    multiplexer = random.randint(2, modulus - 1)
    while gcd(multiplexer, modulus) != 1:
        multiplexer = random.randint(2, modulus - 1)

    return multiplexer, modulus


public_key = []


def generate_public_key(super_knapsack, multiplexer, modulus):
    for each in super_knapsack:
        each_pub = (each * multiplexer) % modulus
        public_key.append(each_pub)
    return public_key


def modInverse(multiplexer, modulus):
    for X in range(1, modulus):
        if (((multiplexer % modulus) * (X % modulus)) % modulus == 1):
            return X
    return -1


def decrypt_matrix_generator(cipher_text, multiplexer, modulus):
    multiplexer_inverse = modInverse(multiplexer, modulus)  # n inverse
    print("multiplexer_inverse", multiplexer_inverse)
    decrypting_matrix = []

    for each in cipher_text:
        decrypting_matrix.append((each * multiplexer_inverse) % modulus)  # each of cipher text multiplied by inverse of n and then mod with modulus number
    return decrypting_matrix


def find_combinations(pvt_key, n):
    valid_combinations = []
    valid_combinations_list = []

    if n == 0:
        valid_combinations.append(0)
    else:
        for r in range(1, len(pvt_key) + 1):
            for combo in combinations(pvt_key, r):
                if sum(combo) == n:
                    valid_combinations.append(combo)
    # print(valid_combinations)

    #  since valid_combination is a list contaning tuple (since we use combinations lib here), to make it a pure list we follow below
    if '(' in str(valid_combinations):
        valid_combinations_list.extend(valid_combinations[0])
        # print(valid_combinations_list)
    else:
        valid_combinations_list = [0]  # for n = 0

    plain_text = []
    for each in pvt_key:
        if each in valid_combinations_list:
            plain_text.append(1)
        else:
            plain_text.append(0)

    return plain_text


def send_public_key(public_key, tcp_socket, con):
    BUFFER_SIZE = 1024

    # bind_to_local(tcp_socket)  # Call bind_to_local to bind the socket
    # tcp_socket.listen(1)

    # conn, addr = tcp_socket.accept()

    data = pickle.dumps(public_key)
    conn.sendall(data)


def bind_to_local(tcp_socket):
    server_ip = socket.gethostbyname(socket.gethostname())
    tcp_socket.bind((server_ip, 0))
    port = tcp_socket.getsockname()[1]
    print("%s accepting datagram at port %s", server_ip, port)


def rceive_cipher_text(tcp_socket, conn):
    BUFFER_SIZE = 1024
    # conn, addr = tcp_socket.accept()
    data = conn.recv(BUFFER_SIZE)  # Receive data from the client
    cipher_text = pickle.loads(data)  # Deserialize the received data
    return cipher_text


if __name__ == "__main__":
    n = 6
    super_increasing_knapsack = generate_superincreasing_knapsack(n)
    print("super_increasing_knapsacks", super_increasing_knapsack)

    multiplexer_and_modulus = generate_multiplexer_and_modulus(super_increasing_knapsack)
    print("multiplexer_and_modulus", multiplexer_and_modulus)

    public_key = generate_public_key(super_increasing_knapsack, multiplexer_and_modulus[0], multiplexer_and_modulus[1])
    print("public_key that would be shared is", public_key)

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind_to_local(tcp_socket)
    tcp_socket.listen()
    conn, addr = tcp_socket.accept()

    send_public_key(public_key, tcp_socket, conn)
    print("The above Public key is shared to user 1")

    time.sleep(10)
    cipher_text = rceive_cipher_text(tcp_socket, conn)
    decryption_matrix = decrypt_matrix_generator(cipher_text, multiplexer_and_modulus[0], multiplexer_and_modulus[1])
    print("decryption_matrix:", decryption_matrix)

    final_list = []
    for each in decryption_matrix:
        combos = find_combinations(super_increasing_knapsack, each)
        final_list.extend(combos)

    print("Combinations:", final_list)
