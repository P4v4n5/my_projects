import socket
import time
import random
from log import MyLogger

prime = 109
primitive_root = 6


class TCP_User1:
    def __init__(self):
        self.logger = MyLogger.setup_user1_logger()

    def tcp_user1_connection(self):
        BUFFER_SIZE = 1024

        # Generating private key for User2
        user1_private_key = random.randint(0, prime - 1)

        # User1 calculates their public key
        user1_public_key = (primitive_root ** user1_private_key) % prime

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_to_local(tcp_socket)
        tcp_socket.listen(1)

        conn, addr = tcp_socket.accept()
        self.logger.info("Connection from: %s", addr)

        # Sending User1's public key to User2
        conn.sendall(str(user1_public_key).encode())

        # Receiving User1's public key
        user2_public_key = int(conn.recv(BUFFER_SIZE).decode())

        # Calculate shared secret
        shared_secret = (user2_public_key ** user1_private_key) % prime

        self.logger.info("Shared Public Key : %s", user1_public_key)
        self.logger.info("Received Public Key : %s", user2_public_key)
        self.logger.info("Shared Secret: %s", shared_secret)

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
