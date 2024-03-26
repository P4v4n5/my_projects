import socket
import pickle
import time
from log import MyLogger  # Importing the setup_logger function


class TCP_User2:
    def __init__(self):
        self.logger = MyLogger.setup_user2_logger()

    def modInverse(self, multiplexer, modulus):
        for X in range(1, modulus):
            if (((multiplexer % modulus) * (X % modulus)) % modulus == 1):
                return X
        return -1

    def encrypt_message(self, message, public_key):
        ciphertext = []
        i = 0
        while i < len(message):
            block = message[i:i + len(public_key)]
            if len(block) < len(public_key):
                block += [0] * (len(public_key) - len(
                    block))
            ciphertext.append(sum(block[j] * public_key[j] for j in range(len(block))))
            i += len(public_key)
        return ciphertext

    def tcp_connection(self):
        BUFFER_SIZE = 1024
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        HOST = input("Enter the IP Address of the system you want to connect with: ")
        PORT = int(input("Enter the PORT number of the same system as above: "))

        self.logger.info(f"Connected to - {HOST}:{PORT}")

        tcp_socket.connect((HOST, PORT))

        data = tcp_socket.recv(BUFFER_SIZE)
        public_key = pickle.loads(data)
        return public_key, tcp_socket

    def send_cipher_text(self, plaintext_message, public_key, tcp_socket):
        ciphertext = self.encrypt_message(plaintext_message, public_key)
        data = pickle.dumps(ciphertext)
        tcp_socket.sendall(data)
        return ciphertext

    def main(self, plaintext_message):
        public_key, tcp_socket = self.tcp_connection()
        user2.logger.info("Received Public key from User 1 is --> %s", public_key)

        user2.logger.info("Cipher text calculation in progress.....")
        time.sleep(5)
        user2.logger.info("Sending the Calculated Cipher text to USER 1.....")
        time.sleep(2)
        cipher_text = self.send_cipher_text(plaintext_message, public_key, tcp_socket)
        user2.logger.info("Cipher text that is sent to USER 1 is ---> %s", cipher_text)


if __name__ == "__main__":
    user2 = TCP_User2()
    user2.logger.info("Starting USER 2 script...")
    # plaintext_message = [1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    plaintext_message = input()
    user2.main(plaintext_message)
