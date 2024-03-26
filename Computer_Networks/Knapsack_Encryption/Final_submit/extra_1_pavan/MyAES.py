# Maintainer: Srinivasulu Pavan Kumar
# Email: psrinivasulu@scu.edu

from Crypto.Cipher import AES

mode = AES.MODE_CBC
IV = b'This is an IV456'


class EncryptDecrypt:
    def __init__(self):
        pass

    def pad_shared_secret(self, key, desired_key_length=16):
        key = str(key).encode()
        if len(key) > desired_key_length:
            return key[:desired_key_length]
        elif len(key) < desired_key_length:
            padding_size = desired_key_length - len(key)
            return b'\0' * padding_size + key
        return key

    def pad_message(self, message):
        padding_size = AES.block_size - len(message) % AES.block_size
        padding = bytes([padding_size] * padding_size)
        return message + padding

    def encrypt(self, shared_secret, message):
        padded_key = self.pad_shared_secret(shared_secret)
        cipher = AES.new(padded_key, mode, IV)  # Initialize AES cipher in CBC mode with the padded key and IV
        message_to_bytes = self.pad_message(message.encode())  # Pad the message and convert it to bytes
        cipher_text = cipher.encrypt(message_to_bytes)  # Encrypt the padded message
        return cipher_text

    def unpad_message(self, padded_message):
        padding_size = padded_message[-1]
        if padding_size > len(padded_message):
            raise ValueError("Invalid padding size")
        message = padded_message[:-padding_size]
        padding = padded_message[-padding_size:]
        if padding != bytes([padding_size] * padding_size):
            raise ValueError("Invalid padding bytes")
        return message

    def decrypt(self, shared_secret, encrypted_message):
        padded_key = self.pad_shared_secret(shared_secret)
        cipher = AES.new(padded_key, mode, IV)  # Initialize AES cipher in CBC mode with the padded key and IV
        decrypted_padded_message = cipher.decrypt(encrypted_message)  # Decrypt the encrypted message
        plain_text = self.unpad_message(decrypted_padded_message)  # Remove padding from the decrypted message

        return plain_text
