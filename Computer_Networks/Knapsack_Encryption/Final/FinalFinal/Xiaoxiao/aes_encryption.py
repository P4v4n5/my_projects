
from Crypto.Cipher import AES

# Constans for AES
mode = AES.MODE_CBC
IV = b'This is an IV456'

def encrypt(shared_secret, message):
        cipher = generate_AES(shared_secret)
        message_to_bytes = pkcs7_pad(message.encode())
        cipher_text = cipher.encrypt(message_to_bytes)  
        return cipher_text


def decrypt(shared_secret, encrypted_message):
        cipher = generate_AES(shared_secret)
        decrypted_padded_message = cipher.decrypt(encrypted_message)
        plain_text = pkcs7_unpad(decrypted_padded_message) 
        return plain_text


def generate_AES(shared_secret):
        pad_key = pad_key_to_aes_length(shared_secret)
        cipher = AES.new(pad_key, mode, IV)
        return cipher


def pkcs7_pad(message):
    padding_size = AES.block_size - len(message) % AES.block_size
    padding = bytes([padding_size] * padding_size)
    return message + padding


def pkcs7_unpad(padded_message):
    padding_size = padded_message[-1]
    if padding_size > len(padded_message):
        raise ValueError("Invalid padding size")
    message = padded_message[:-padding_size]
    padding = padded_message[-padding_size:]
    if padding != bytes([padding_size] * padding_size):
        raise ValueError("Invalid padding bytes")
    return message

def pad_key_to_aes_length(key, desired_key_length=16):
    key = str(key).encode()
    if len(key) > desired_key_length:
        return key[:desired_key_length]
    elif len(key) < desired_key_length:
        padding_size = desired_key_length - len(key)
        return b'\0' * padding_size + key
    return key