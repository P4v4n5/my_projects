import socket
import time
from log import MyLogger
import random
from Crypto.Cipher import AES
import hashlib

prime = 109
primitive_root = 6


class TCP_User2:
    def __init__(self):
        self.logger = MyLogger.setup_user2_logger()

        # ----------decryption logic starts from here-------------------

    def unpad_message(self, padded_message):
        padding_length = padded_message[-1]
        return padded_message[:-padding_length]

    def decrypt(self, shared_secret, encrypted_message):
        shared_secret = shared_secret
        password = str(shared_secret).encode()
        key = hashlib.sha256(password).digest()
        mode = AES.MODE_CBC  # how the code should encrypt or decrypt
        IV = b'This is an IV456'  # to add extra layer of encryption, making it impossible to decrypt

        cipher = AES.new(key, mode, IV)

        encrypted_message = encrypted_message

        decrypted_padded_message = cipher.decrypt(encrypted_message)
        decrypted_message = self.unpad_message(decrypted_padded_message)

        return decrypted_message

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

                encrypted_message = client_socket.recv(BUFFER_SIZE)
                # self.logger.info("encrypted text recvd is: " + encrypted_message)

                decrypted_message = self.decrypt(shared_secret, encrypted_message)
                self.logger.info(decrypted_message.decode())

        except Exception as e:
            self.logger.error("An error occurred: %s", e)


if __name__ == "__main__":
    user2 = TCP_User2()
    user2.tcp_user2_connection()
