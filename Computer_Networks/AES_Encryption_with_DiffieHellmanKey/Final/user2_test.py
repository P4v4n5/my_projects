# Maintainer: Srinivasulu Xiaoxiao Kumar
# Email: psrinivasulu@scu.edu

import socket
from log import MyLogger
import random
from MyAES import EncryptDecrypt

prime = 109
primitive_root = 6


class TCP_User2:
    def __init__(self):
        self.logger = MyLogger.setup_user2_logger()
        self.MyAES = EncryptDecrypt()

    def tcp_user2_connection(self):
        BUFFER_SIZE = 1024

        # Generating private key for User2
        user2_private_key = random.randint(0, prime-1)

        # User2 calculates his public key
        user2_public_key = (primitive_root ** user2_private_key) % prime

        HOST = input("Enter the IP Address of the system you want to connect with: ")
        self.logger.info("Entered IP Address : %s", HOST)
        PORT = int(input("Enter the PORT number of the same system as above: "))
        self.logger.info("Entered PORT Number : %s", PORT)

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

                self.logger.info("Shared Public Key is --> %s", user2_public_key)
                self.logger.info("Received Public Key is --> %s", user1_public_key)
                self.logger.info("Shared Secret is --> %s", shared_secret)
                self.logger.info("Waiting to receive the Encrypted message from USER1")

                encrypted_message = client_socket.recv(BUFFER_SIZE)
                self.logger.info("Encrypted text received from USER 1 is ---> %s", encrypted_message)

                # ---------calling encryption function-------

                decrypted_message = self.MyAES.decrypt(shared_secret, encrypted_message).decode()
                self.logger.info("Wohoooooo!!! Decrypted Message is --> %s", decrypted_message)


        except Exception as e:
            self.logger.error("An error occurred: %s", e)


if __name__ == "__main__":
    user2 = TCP_User2()
    user2.tcp_user2_connection()
