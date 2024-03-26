import random
import socket
from aes_encryption import encrypt
from logger_helper import setup_logger

logger = setup_logger('csen233extra1JiangXiaoxiao_user_1.log')

PORT = 8008
BUFFER_SIZE = 1024
PRIME = 109
PRIMITIVE_ROOT = 6

private_key = random.randint(1, PRIME - 1)

def zero_knowledge_key_exchange(conn):
    server_public_key = (PRIMITIVE_ROOT ** private_key) % PRIME
    conn.sendall(str(server_public_key).encode())
    logger.info(f"Shared Public Key (Server's): {server_public_key}")

    client_public_key = int(conn.recv(BUFFER_SIZE).decode())
    logger.info(f"Received Public Key (Client's): {client_public_key}")

    shared_secret = (client_public_key ** private_key) % PRIME
    logger.info(f"Shared Secret: {shared_secret}")
    return shared_secret

def tcp_server():
    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            server_ip = socket.gethostbyname(socket.gethostname())
            tcp_socket.bind((server_ip, PORT))
            logger.info(f"{server_ip} accepting connections at port {PORT}")
            tcp_socket.listen(1)
            conn, addr = tcp_socket.accept()
            with conn:
                logger.info(f"Connection established with: {addr}")
                shared_secret = zero_knowledge_key_exchange(conn)

                msg = input("Input the msg you want to send to client:")
                logger.info(f"The original meesage is: {msg}")

                encryped_msg = encrypt(shared_secret, msg)
                logger.info(f"Send encryped message: {encryped_msg}")

                conn.sendall(encryped_msg)

                conn.close()

    except Exception as e:
        logger.error("Server failed to start or accept connections", exc_info=True)

if __name__ == "__main__":
    tcp_server()
