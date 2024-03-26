import socket
import pickle
import time
from GitHub_Personal.my_projects.Computer_Networks.Knapsack_Encryption.testing_final.Pavan.log import MyLogger  # Importing the setup_logger function


class TCP_User2:
    def __init__(self):
        self.logger = MyLogger.setup_user2_logger()

    def modInverse(self, multiplexer, modulus):
        for X in range(1, modulus):
            if (((multiplexer % modulus) * (X % modulus)) % modulus == 1):
                return X
        return -1

    def encrypt_message(self, message, public_key):
        ciphertext = []
        i = 0
        while i < len(message):
            block = message[i:i + len(public_key)]
            if len(block) < len(public_key):
                block += [0] * (len(public_key) - len(
                    block))
            ciphertext.append(sum(block[j] * public_key[j] for j in range(len(block))))
            i += len(public_key)
        return ciphertext

    def tcp_connection(self):
        BUFFER_SIZE = 1024
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        HOST = input("Enter the IP Address of the system you want to connect with: ")
        PORT = int(input("Enter the PORT number of the same system as above: "))

        self.logger.info(f"Connected to - {HOST}:{PORT}")

        tcp_socket.connect((HOST, PORT))

        data = tcp_socket.recv(BUFFER_SIZE)
        public_key = pickle.loads(data)
        return public_key, tcp_socket

    def send_cipher_text(self, plaintext_message, public_key, tcp_socket, length):
        ciphertext = self.encrypt_message(plaintext_message, public_key)
        data_to_send = {'ciphertext': ciphertext, 'length': length}
        serialized_data = pickle.dumps(data_to_send)
        tcp_socket.sendall(serialized_data)
        return ciphertext

    def main(self, plaintext_message, length):
        public_key, tcp_socket = self.tcp_connection()
        user2.logger.info("Received Public key from User 1 is --> %s", public_key)

        user2.logger.info("Cipher text calculation in progress.....")
        time.sleep(5)
        user2.logger.info("Sending the Calculated Cipher text to USER 1.....")
        time.sleep(2)
        cipher_text = self.send_cipher_text(plaintext_message, public_key, tcp_socket, length)
        user2.logger.info("Cipher text that is sent to USER 1 is ---> %s", cipher_text)

    def decimal_to_binary(self, decimal_num):
        binary_num = bin(decimal_num)[2:]
        return binary_num

    def input_to_list(self, plaint_text_input):
        plaint_text_input_list = []
        for bit in plaint_text_input:
            if bit not in ['0', '1']:
                raise ValueError("Input should contain only '0's and '1's")
            plaint_text_input_list.append(int(bit))
        return plaint_text_input_list


if __name__ == "__main__":
    user2 = TCP_User2()
    user2.logger.info("Starting USER 2 script...")
    decimal_input = int(input("Enter a decimal number: "))
    user2.logger.info("Entered decimal number is %s", decimal_input)
    print(decimal_input)

    binary_plain_text = user2.decimal_to_binary(decimal_input)  # Convert decimal to binary
    plaint_text_input_list = user2.input_to_list(binary_plain_text)
    length = len(plaint_text_input_list)
    user2.main(plaint_text_input_list, length)
