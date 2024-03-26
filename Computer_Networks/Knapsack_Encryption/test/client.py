import socket
import pickle
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Establish TCP connection and share keys
def communicate():
    # Client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    # Receive public key
    public_key = client_socket.recv(1024)
    public_key = pickle.loads(public_key)
    logging.info("Public key received: %s", public_key)

    # Define the message to be encrypted
    message = "Hello, this is a secret message!"
    logging.info("Message to encrypt: %s", message)

    # Encrypt the message using the public key
    encrypted_message = encrypt_message(message, public_key)
    logging.info("Encrypted message: %s", encrypted_message)

    # Send encrypted message
    client_socket.send(pickle.dumps(encrypted_message))
    logging.info("Encrypted message sent")

    client_socket.close()

# Function to encrypt a message using the public key
def encrypt_message(message, public_key):
    encrypted_message = []
    for char in message:
        char_code = ord(char)
        encrypted_char = sum([public_key[i] for i in range(len(public_key)) if char_code & (1 << i)])
        encrypted_message.append(encrypted_char)
    return encrypted_message

if __name__ == "__main__":
    communicate()
