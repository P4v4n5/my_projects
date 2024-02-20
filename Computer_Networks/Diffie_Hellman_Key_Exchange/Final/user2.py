import socket
import time
from log import MyLogger
import random

prime = 109
primitive_root = 6


class TCP_User2:
    def __init__(self):
        self.logger = MyLogger.setup_user2_logger()

    def tcp_user2_connection(self):
        BUFFER_SIZE = 1024

        # Initialize logger
        # logger = MyLogger.setup_user2_logger()

        # Generating private key for User2
        user2_private_key = random.randint(0, prime-1)

        # User2 calculates his public key
        user2_public_key = (primitive_root ** user2_private_key) % prime

        HOST = input("Enter the IP Address of the system you want to connect with: ")
        # self.logger.info("Entered IP Address : %s", HOST)
        PORT = int(input("Enter the PORT number of the same system as above: "))
        # self.logger.info("Entered PORT Number : %s", PORT)

        self.logger.info("Shared Public Key : %s", user2_public_key)

        # Establish TCP connection
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))

                # Receive User1's public key
                user1_public_key = int(client_socket.recv(BUFFER_SIZE).decode())

                # Sending User2's public key to User1
                client_socket.sendall(str(user2_public_key).encode())

                # Calculate shared secret
                shared_secret = (user1_public_key ** user2_private_key) % prime

                self.logger.info("Shared Public Key : %s", user2_public_key)
                self.logger.info("Received Public Key : %s", user1_public_key)
                self.logger.info("Shared Secret: %s", shared_secret)

        except Exception as e:
            self.logger.error("An error occurred: %s", e)


if __name__ == "__main__":
    user2 = TCP_User2()
    user2.tcp_user2_connection()
