#Name: Shiva Kumar Reddy Rangapuram
#Email: srangapuram@scu.edu
#Partner ID: psrinivasulu@scu.edu

import socket
import pickle
import time
import logging

def configure_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('logfile_user2shiva.log', mode='w')
    file_handler.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(funcName)s - line %(lineno)d - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

class User2:
    
    def __init__(self):
        self.logger = configure_logging()
    
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
    
    def send_cipher_text(self, plaintext_message, public_key, s, length):
        ciphertext = self.encrypt_message(plaintext_message, public_key)
        data_to_send = {'ciphertext': ciphertext, 'length': length}
        serialized_data = pickle.dumps(data_to_send)
        s.sendall(serialized_data)
        return ciphertext
    
    def decimal_to_binary(self, decimal_num):
        binary_num = bin(decimal_num)[2:]
        return binary_num

    def input_to_list(self, plain_text_input):
        plain_text_input_list = []
        for bit in plain_text_input:
            if bit not in ['0', '1']:
                raise ValueError("Input should contain only '0's and '1's")
            plain_text_input_list.append(int(bit))
        return plain_text_input_list
    
    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                user1_ip_address = input("Enter IP address: ")
                PORT = int(input("Enter PORT: "))
                self.logger.info(f"Connecting to user1 at {user1_ip_address}:{PORT}...")
                s.connect((user1_ip_address, PORT))
                decimal_input = int(input("Enter a decimal number: "))
                self.logger.info(f"Decimal number is: {decimal_input}")
                binary_plain_text = user2.decimal_to_binary(decimal_input)
                plain_text_input_list = user2.input_to_list(binary_plain_text)
                length = len(plain_text_input_list)
                data = s.recv(1024)
                public_key = pickle.loads(data)
                self.logger.info("Received Public key from User 1 is: %s", public_key)
                self.logger.info("Cipher text calculation in progress.....")
                time.sleep(5)
                self.logger.info("Sending the Calculated Cipher text to USER 1.....")
                time.sleep(2)
                cipher_text = self.send_cipher_text(plain_text_input_list, public_key, s, length)
                self.logger.info("Cipher text that is sent to USER 1 is: %s", cipher_text)
            except Exception as e:
                self.logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    user2 = User2()
    user2.logger.info("Starting USER 2 script...")
    user2.main()
