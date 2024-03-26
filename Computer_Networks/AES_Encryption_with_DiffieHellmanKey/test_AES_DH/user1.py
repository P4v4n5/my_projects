import socket
import time
import random
from log import MyLogger
from Crypto.Cipher import AES
import hashlib

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

        # ---------calling encryption function-------
        encrypted_message = self.encrypt(shared_secret)
        conn.sendall(encrypted_message)
        self.logger.info("Encrypted message sent is: " + str(encrypted_message))

        conn.close()
        tcp_socket.close()

    def bind_to_local(self, tcp_socket):
        server_ip = socket.gethostbyname(socket.gethostname())
        tcp_socket.bind((server_ip, 0))
        port = tcp_socket.getsockname()[1]
        self.logger.info("%s accepting datagram at port %s", server_ip, port)

    #----------encryption logic starts from here-------------------

    def pad_message(self, message):
        padding_length = AES.block_size - (len(message) % AES.block_size)
        padding = bytes([padding_length]) * padding_length
        return message + padding

    def encrypt(self, shared_secret):
        shared_secret = shared_secret
        password = str(shared_secret).encode()
        key = hashlib.sha256(password).digest()
        mode = AES.MODE_CBC  # how the code should encrypt or decrypt
        IV = b'This is an IV456'  # to add extra layer of encryption, making it impossible to decrypt

        cipher = AES.new(key, mode, IV)

        message = b"Hey! the secret spell to open the treasure door is - Alohomora"
        padded_message = self.pad_message(message)

        encrypted_message = cipher.encrypt(padded_message)

        # print(encrypted_message)
        return encrypted_message

if __name__ == "__main__":
    user1 = TCP_User1()
    user1.tcp_user1_connection()
