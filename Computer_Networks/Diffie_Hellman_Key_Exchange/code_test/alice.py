import socket
import time

PORT = 8008
BUFFER_SIZE = 1024
prime = 109
primitive_root = 6


def tcp_server():

    # Alice's private key
    alice_private_key = 3

    # Alice calculates her public key
    alice_public_key = (primitive_root ** alice_private_key) % prime

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind_to_local(tcp_socket)
    tcp_socket.listen(1)

    conn, addr = tcp_socket.accept()
    print("Connection from:", addr)

    # Send Alice's public key to Bob
    conn.sendall(str(alice_public_key).encode())

    # Receive Bob's public key from Bob
    bob_public_key = int(conn.recv(1024).decode())

    # Calculate shared secret
    shared_secret = (bob_public_key ** alice_private_key) % prime

    print("Shared Public Key (Alice's):", alice_public_key)
    print("Received Public Key (Bob's):", bob_public_key)
    time.sleep(10)
    print("Shared Secret:", shared_secret)

    conn.close()
    tcp_socket.close()


def bind_to_local(tcp_socket):
    server_ip = socket.gethostbyname(socket.gethostname())
    tcp_socket.bind((server_ip, 0))
    PORT = tcp_socket.getsockname()[1]
    print(f"{server_ip} accepting datagram at port {PORT}")


if __name__ == "__main__":
    tcp_server()
