import socket
import time

prime = 109
primitive_root = 6


def main():

    # Bob's private key
    bob_private_key = 4

    # Bob calculates his public key
    bob_public_key = (primitive_root ** bob_private_key) % prime

    # Establish TCP connection
    HOST = input("Enter the IP Address of the system you want to connect with: ")
    PORT = int(input("Enter the PORT number of the same system as above: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        # Receive Alice's public key from Alice
        alice_public_key = int(client_socket.recv(1024).decode())

        # Send Bob's public key to Alice
        client_socket.sendall(str(bob_public_key).encode())

        # Calculate shared secret
        shared_secret = (alice_public_key ** bob_private_key) % prime

        print("Shared Public Key (Bob's):", bob_public_key)
        time.sleep(10)
        print("Shared Secret:", shared_secret)


if __name__ == "__main__":
    main()
