# Maintainer: Srinivasulu Xiaoxiao Kumar
# Email: psrinivasulu@scu.edu

import socket
import random
from log import MyLogger
from MyAES import EncryptDecrypt

prime = 109
primitive_root = 6


class TCP_User1:
    def __init__(self):
        self.logger = MyLogger.setup_user1_logger()
        self.MyAES = EncryptDecrypt()

    def tcp_user1_connection(self):
        BUFFER_SIZE = 1024

        # Generating private key for User2
        user1_private_key = random.randint(0, prime - 1)

        # User1 calculates their public key
        user1_public_key = (primitive_root ** user1_private_key) % prime

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_to_local(tcp_socket)
        # self.bind_to_local(tcp_socket)
        tcp_socket.listen(1)

        conn, addr = tcp_socket.accept()
        self.logger.info("Connection from: %s", addr)

        # Sending User1's public key to User2
        conn.sendall(str(user1_public_key).encode())

        # Receiving User1's public key
        user2_public_key = int(conn.recv(BUFFER_SIZE).decode())

        # Calculate shared secret
        shared_secret = (user2_public_key ** user1_private_key) % prime

        message = input("Shhhhhhhh!!! Enter the message that you secretly want to send --> ")

        self.logger.info("Shared Public Key is --> %s", user1_public_key)
        self.logger.info("Received Public Key is --> %s", user2_public_key)
        self.logger.info("Shared Secret is --> %s", shared_secret)

        # ---------calling encryption function-------

        encrypted_message = self.MyAES.encrypt(shared_secret, message)
        self.logger.info(f"Encrypted message sent to USER 2 is --> %s", encrypted_message)
        conn.sendall(encrypted_message)

        conn.close()
        tcp_socket.close()

    def bind_to_local(self, tcp_socket):
        server_ip = socket.gethostbyname(socket.gethostname())
        tcp_socket.bind((server_ip, 0))
        port = tcp_socket.getsockname()[1]
        self.logger.info("%s accepting datagram at port %s", server_ip, port)


if __name__ == "__main__":
    user1 = TCP_User1()
    user1.tcp_user1_connection()
