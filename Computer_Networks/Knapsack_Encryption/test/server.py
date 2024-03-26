import socket
import pickle
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate a super-increasing knapsack
def generate_super_increasing(n):
    knapsack = [1]  # Start with the first element as 1
    total = 1
    for i in range(n - 1):
        total += knapsack[i]
        knapsack.append(total)
    return knapsack

# Function to transform a super-increasing knapsack into a non-super-increasing one
def transform_knapsack(knapsack, multiplier, modulus):
    transformed_knapsack = [(x * multiplier) % modulus for x in knapsack]
    return transformed_knapsack

# Function to decrypt a message using the private key
def decrypt_message(encrypted_message, private_key):
    decrypted_message = ""
    for item in encrypted_message:
        remainder = item
        for key in reversed(private_key):
            if key <= remainder:
                decrypted_message += "1"
                remainder -= key
            else:
                decrypted_message += "0"
        # Padding the decrypted message with zeros if its length is not a multiple of 8
        while len(decrypted_message) % 8 != 0:
            decrypted_message += "0"
    # Converting each 8-bit binary chunk to its corresponding ASCII character
    decrypted_message = [chr(int(decrypted_message[i:i+8], 2)) for i in range(0, len(decrypted_message), 8)]
    return "".join(decrypted_message)


# Establish TCP connection and share keys
def serve():
    # Generate super-increasing knapsack
    n = 8  # Number of elements
    super_increasing_knapsack = generate_super_increasing(n)
    logging.info("Super-increasing knapsack: %s", super_increasing_knapsack)

    # Transform knapsack
    multiplier = 3
    modulus = 17
    non_super_increasing_knapsack = transform_knapsack(super_increasing_knapsack, multiplier, modulus)
    logging.info("Non-super-increasing knapsack: %s", non_super_increasing_knapsack)

    # Server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    logging.info("Waiting for connection...")
    conn, addr = server_socket.accept()
    logging.info("Connected to: %s", addr)

    # Send public key
    conn.send(pickle.dumps(non_super_increasing_knapsack))
    logging.info("Public key sent")

    # Receive encrypted message
    encrypted_message = conn.recv(1024)
    encrypted_message = pickle.loads(encrypted_message)
    logging.info("Encrypted message received: %s", encrypted_message)

    # Decrypt message
    private_key = super_increasing_knapsack
    decrypted_message = decrypt_message(encrypted_message, private_key)
    logging.info("Decrypted message: %s", decrypted_message)

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    serve()
