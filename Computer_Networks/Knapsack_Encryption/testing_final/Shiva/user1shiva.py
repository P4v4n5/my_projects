#Name: Shiva Kumar Reddy Rangapuram
#Email: srangapuram@scu.edu
#Partner ID: psrinivasulu@scu.edu

import random
from itertools import combinations
import socket
import pickle
import time
import logging

def configure_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('logfile_user1shiva.log', mode='w')
    file_handler.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(funcName)s - line %(lineno)d - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

class User1:
    
    def __init__(self):
        self.logger = configure_logging()
    
    def create_superincreasing_knapsack(self, n_elements):
        knapsack = []
        element = 1
        for _ in range(n_elements):
            knapsack.append(element)
            element *= 2 
        return knapsack
    
    def gcd(self, a, b):
        if b == 0:
            return a
        return self.gcd(b, a % b)
    
    def create_multiplexer_and_modulus(self, super_knapsack):
        # Generate multiplexer and modulus
        total_sum = sum(super_knapsack)
        modulus = total_sum * random.randint(2, 5) 
        multiplexer = random.randint(2, modulus - 1)
        while self.gcd(multiplexer, modulus) != 1:
            multiplexer = random.randint(2, modulus - 1)
        return multiplexer, modulus
    
    def create_public_key(self, super_knapsack, multiplexer, modulus):
        public_key = []
        for each in super_knapsack:
            each_pub = (each * multiplexer) % modulus
            public_key.append(each_pub)
        return public_key
    
    def mod_inverse(self, multiplexer, modulus):
        return pow(multiplexer, -1, modulus)
    
    def create_decrypt_matrix(self, cipher_text, multiplexer, modulus):
        multiplexer_inverse = self.mod_inverse(multiplexer, modulus)  
        self.logger.info("multiplexer_inverse: %s", multiplexer_inverse)
        decrypting_matrix = []
        for each in cipher_text:
            decrypting_matrix.append((each * multiplexer_inverse) % modulus)
        return decrypting_matrix


    def find_combinations(self, pvt_key, n):
        valid_combinations = []
        for r in range(1, len(pvt_key) + 1):
            for combo in combinations(pvt_key, r):
                if sum(combo) == n:
                    valid_combinations.extend(combo)
        plain_text = [1 if each in valid_combinations else 0 for each in pvt_key]
        return plain_text


    def send_public_key(self, public_key, s, conn):
        BUFFER_SIZE = 1024
        data = pickle.dumps(public_key)
        conn.sendall(data)

    def recv_cipher_text(self, s, conn):
        BUFFER_SIZE = 1024
        data = conn.recv(BUFFER_SIZE)
        received_data = pickle.loads(data)
        ciphertext = received_data['ciphertext']
        length = received_data['length']
        return ciphertext, length
    
    def main(self, n):
        HOST = socket.gethostbyname(socket.gethostname())
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Start listening for connections
            try:
                s.bind((HOST, 0))
                PORT = s.getsockname()[1]
                self.logger.info(f"User1 is listening on {HOST}:{PORT}")
                s.listen()
                conn, addr = s.accept()
                self.logger.info(f"Connected by {addr}")
                with conn:
                    super_increasing_knapsack = self.create_superincreasing_knapsack(n)
                    self.logger.info("Super Increasing Key/Private key is: %s", super_increasing_knapsack)
                    multiplexer_and_modulus = self.create_multiplexer_and_modulus(super_increasing_knapsack)
                    self.logger.info("Multiplexer and Modulus respectively are: %s", multiplexer_and_modulus)
                    public_key = self.create_public_key(super_increasing_knapsack, multiplexer_and_modulus[0],
                                                        multiplexer_and_modulus[1])
                    self.logger.info("The Public Key that would be shared to user2 is: %s", public_key)
                    self.send_public_key(public_key, s, conn)
                    self.logger.info("Waiting for a Cipher text from user2!!")
                    time.sleep(10)
                    cipher_text, length = self.recv_cipher_text(s, conn)
                    decryption_matrix = self.create_decrypt_matrix(cipher_text, multiplexer_and_modulus[0],
                                                                    multiplexer_and_modulus[1])
                    final_list = []
                    for each in decryption_matrix:
                        combos = self.find_combinations(super_increasing_knapsack, each)
                        final_list.extend(combos)
                        n = length
                        final_binary_plain_text = final_list[:n]
                        final_plain_text = 0
                        for bit in final_binary_plain_text:
                            final_plain_text = final_plain_text * 2 + bit
                    self.logger.info("The Message that is shared by user2 to user1 is: %s",
                                        final_plain_text)
            except Exception as e:
                self.logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    user1 = User1()
    user1.logger.info("Starting USER 1 script...")
    n = 6
    user1.main(n)
