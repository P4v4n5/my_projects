import socket
import pickle
import time


def modInverse(multiplexer, modulus):
    for X in range(1, modulus):
        if (((multiplexer % modulus) * (X % modulus)) % modulus == 1):
            return X
    return -1


def encrypt_message(message, public_key):
    ciphertext = []
    i = 0
    while i < len(message):
        block = message[i:i + len(public_key)]
        if len(block) < len(public_key):
            block += [0] * (len(public_key) - len(
                block))  # padding zero if the length of plain text is less than public key
        ciphertext.append(sum(block[j] * public_key[j] for j in range(len(block))))
        i += len(public_key)
    return ciphertext


def tcp_connection():
    BUFFER_SIZE = 1024
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = input("Enter the IP Address of the system you want to connect with: ")
    PORT = int(input("Enter the PORT number of the same system as above: "))

    print(f"Connected to - {HOST}:{PORT}")

    tcp_socket.connect((HOST, PORT))

    data = tcp_socket.recv(BUFFER_SIZE)  # Receive data from the client
    public_key = pickle.loads(data)  # Deserialize the received data

    return public_key, tcp_socket


def send_cipher_text(plaintext_message, public_key, tcp_socket):
    ciphertext = encrypt_message(plaintext_message, public_key)
    data = pickle.dumps(ciphertext)
    tcp_socket.sendall(data)
    return ciphertext


if __name__ == "__main__":
    public_key, tcp_socket = tcp_connection()
    print("Received Public key from User 1 is --> ", public_key)

    plaintext_message = [1, 0, 0, 1, 0, 0, 0, 0, 0]
    print("Calculation is in progress.....")
    time.sleep(5)
    print("Sending the Calculated Cipher text to USER 1.....")
    time.sleep(2)
    cipher_text = send_cipher_text(plaintext_message, public_key, tcp_socket)
    print("Cipher text that is sent to USER 1 is ---> ", cipher_text)
