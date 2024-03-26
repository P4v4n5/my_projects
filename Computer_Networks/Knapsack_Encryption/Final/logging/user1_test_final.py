# Maintainer: Pavan Kumar Srinivasulu
# Email: psrinivasulu@scu.edu

# Partner Info:
# Name: Shiva Kumar Reddy Rangapuram
# Email: srangapuram@scu.edu

import random
from itertools import combinations
import socket
import pickle
import time
from log import MyLogger  # Importing the setup_logger function


class TCP_User1:
    def __init__(self):
        self.logger = MyLogger.setup_user1_logger()

    def generate_superincreasing_knapsack(self, n_elements):
        knapsack = []
        total = 0
        for i in range(n_elements):
            element = total + 1  # to make sure the next element is greater than the sum of previous elements
            knapsack.append(element)
            total += element
        return knapsack

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def generate_multiplexer_and_modulus(self, super_knapsack):
        total_sum = sum(super_knapsack)

        # Generate modulus greater than the sum of the private key
        modulus = random.randint(total_sum + 1, 2 * total_sum)

        # Generate a multiplexer (multiplier) with no common factors with modulus
        multiplexer = random.randint(2, modulus - 1)
        while self.gcd(multiplexer, modulus) != 1:
            multiplexer = random.randint(2, modulus - 1)

        return multiplexer, modulus

    def generate_public_key(self, super_knapsack, multiplexer, modulus):
        public_key = []
        for each in super_knapsack:
            each_pub = (each * multiplexer) % modulus
            public_key.append(each_pub)
        return public_key

    def modInverse(self, multiplexer, modulus):
        for X in range(1, modulus):
            if (((multiplexer % modulus) * (X % modulus)) % modulus == 1):
                return X
        return -1

    def decrypt_matrix_generator(self, cipher_text, multiplexer, modulus):
        multiplexer_inverse = self.modInverse(multiplexer, modulus)  # n inverse
        self.logger.info("multiplexer_inverse: %s", multiplexer_inverse)
        decrypting_matrix = []

        for each in cipher_text:
            decrypting_matrix.append((each * multiplexer_inverse) % modulus)
        return decrypting_matrix

    def find_combinations(self, pvt_key, n):
        valid_combinations = []
        valid_combinations_list = []

        if n == 0:
            valid_combinations.append(0)
        else:
            for r in range(1, len(pvt_key) + 1):
                for combo in combinations(pvt_key, r):
                    if sum(combo) == n:
                        valid_combinations.append(combo)

        if '(' in str(valid_combinations):
            valid_combinations_list.extend(valid_combinations[0])
        else:
            valid_combinations_list = [0]

        plain_text = []
        for each in pvt_key:
            if each in valid_combinations_list:
                plain_text.append(1)
            else:
                plain_text.append(0)

        return plain_text

    def send_public_key(self, public_key, tcp_socket, conn):
        BUFFER_SIZE = 1024

        data = pickle.dumps(public_key)
        conn.sendall(data)

    def bind_to_local(self, tcp_socket):
        server_ip = socket.gethostbyname(socket.gethostname())
        tcp_socket.bind((server_ip, 0))
        port = tcp_socket.getsockname()[1]
        self.logger.info("%s accepting datagram at port %s", server_ip, port)

    def receive_cipher_text(self, tcp_socket, conn):
        BUFFER_SIZE = 1024
        data = conn.recv(BUFFER_SIZE)
        received_data = pickle.loads(data)

        ciphertext = received_data['ciphertext']
        length = received_data['length']

        return ciphertext, length

    def main(self, n):
        super_increasing_knapsack = self.generate_superincreasing_knapsack(n)
        user1.logger.info("Randomly generated Super Increasing Key/Private key is ---> %s", super_increasing_knapsack)

        multiplexer_and_modulus = self.generate_multiplexer_and_modulus(super_increasing_knapsack)
        user1.logger.info("Multiplexer and Modulus respectively are ---> %s", multiplexer_and_modulus)

        public_key = self.generate_public_key(super_increasing_knapsack, multiplexer_and_modulus[0],
                                              multiplexer_and_modulus[1])
        user1.logger.info("The calculated Public Key that would be shared is ---> %s", public_key)

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_to_local(tcp_socket)
        tcp_socket.listen()
        conn, addr = tcp_socket.accept()

        self.send_public_key(public_key, tcp_socket, conn)
        self.logger.info("The above Public key is shared to USER 2, so as to receive a Cipher text")
        self.logger.info("Waiting for a Cipher text from USER 2........")

        time.sleep(10)
        cipher_text, length = self.receive_cipher_text(tcp_socket, conn)
        decryption_matrix = self.decrypt_matrix_generator(cipher_text, multiplexer_and_modulus[0],
                                                          multiplexer_and_modulus[1])

        final_list = []
        for each in decryption_matrix: # this is responsible to match each of the decrypting matrix with the super increasing knapsack and give the binary values further
            combos = self.find_combinations(super_increasing_knapsack, each)
            final_list.extend(combos)
            n = length

            final_binary_plain_text = final_list[:n]

            final_plain_text = 0
            for bit in final_binary_plain_text:
                final_plain_text = final_plain_text * 2 + bit

        self.logger.info("The final Plaintext/Message that is shared by USER 2 to USER 1 is --> %s", final_plain_text)


if __name__ == "__main__":
    user1 = TCP_User1()
    user1.logger.info("Starting USER 1 script...")
    n = 6
    user1.main(n)
