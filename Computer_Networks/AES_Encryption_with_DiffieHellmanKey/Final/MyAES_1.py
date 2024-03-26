import socket
import time
import random
from log import MyLogger
from Crypto.Cipher import AES
import hashlib


class EncryptDecrypt:
    def __init__(self):
        pass

    # ----------encryption logic starts from here-------------------

    def pad_message(self, message):
        padding_length = AES.block_size - (len(message) % AES.block_size)  # AES block size 16 bytes default
        padding = bytes([padding_length]) * padding_length
        return message + padding

    def pad_shared_secret(self, key):
        key_str = str(key)
        padding_length = 128 - len(key_str)
        padded_key = '0' * padding_length + key_str
        return padded_key

    def encrypt(self, shared_secret, message):
        password = str(shared_secret).encode()
        key = hashlib.sha256(password).digest()
        mode = AES.MODE_CBC  # how the code should encrypt or decrypt
        IV = b'This is an IV456'  # to add extra layer of encryption, making it impossible to decrypt

        cipher = AES.new(key, mode, IV)

        padded_message = self.pad_message(message)

        cipher_text = cipher.encrypt(padded_message)  # plain text encrypted to cipher text

        # print(encrypted_message)
        return cipher_text

    # ----------decryption logic starts from here-------------------

    def unpad_message(self, padded_message):
        padding_length = padded_message[-1]
        return padded_message[:-padding_length]

    def decrypt(self, shared_secret, encrypted_message):
        password = str(shared_secret).encode()
        key = hashlib.sha256(password).digest()
        mode = AES.MODE_CBC  # how the code should encrypt or decrypt
        IV = b'This is an IV456'  # to add extra layer of encryption, making it impossible to decrypt

        cipher = AES.new(key, mode, IV)

        decrypted_padded_message = cipher.decrypt(encrypted_message)
        plain_text = self.unpad_message(decrypted_padded_message)  # cipher text decrypted to plain text

        return plain_text
