import random
import socket
from logger_helper import setup_logger

logger = setup_logger('csen233hw5JiangXiaoxiao_user2.log')

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
            zero_knowledge_key_exchange(client_socket)
    except Exception as e:
        logger.error("Failed to establish connection or key exchange", exc_info=True)


if __name__ == "__main__":
    main()
