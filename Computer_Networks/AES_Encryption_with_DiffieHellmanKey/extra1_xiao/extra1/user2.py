import random
import socket
from logger_helper import setup_logger
from aes_encryption import decrypt

logger = setup_logger('csen233extra1JiangXiaoxiao_client.log')

PRIME = 109
PRIMITIVE_ROOT = 6

private_key = random.randint(1, PRIME - 1)

def zero_knowledge_key_exchange(client_socket):
    global private_key, PRIME, PRIMITIVE_ROOT

    try:
        client_public_key = (PRIMITIVE_ROOT ** private_key) % PRIME

        logger.info(f"Sending client public key: {client_public_key}")
        client_socket.sendall(str(client_public_key).encode())

        server_public_key = int(client_socket.recv(1024).decode())
        logger.info(f"Received server public key: {server_public_key}")

        shared_secret = (server_public_key ** private_key) % PRIME
        logger.info(f"Shared Secret: {shared_secret}")

        return shared_secret

    except Exception as e:
        logger.error("Error during key exchange", exc_info=True)

def main():
    host = input("Enter the IP Address of the system you want to connect with: ")
    port = int(input("Enter the PORT number of the same system as above: "))

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            logger.info(f"Attempting to connect to {host}:{port}")

            client_socket.connect((host, port))
            logger.info("Connection established")

            shared_secret = zero_knowledge_key_exchange(client_socket)
            logger.info("Waiting to receive message from server...")

            encryped_msg = client_socket.recv(1024)
            logger.info(f"Receive encryped message from server: {encryped_msg}")

            decryped_msg = decrypt(shared_secret, encryped_msg).decode()
            logger.info(f"Decryped Message: {decryped_msg}")

            client_socket.close()

    except Exception as e:
        logger.error("Failed to establish connection or key exchange", exc_info=True)


if __name__ == "__main__":
    main()
