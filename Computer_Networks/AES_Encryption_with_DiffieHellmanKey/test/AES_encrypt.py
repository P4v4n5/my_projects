from Crypto.Cipher import AES
import hashlib

shared_secret = 23
password = str(shared_secret).encode()
print("Length of encoded shared secret:", len(password))
key = hashlib.sha256(password).digest()
mode = AES.MODE_CBC  # how the code should encrypt or decrypt
IV = b'This is an IV456'  # to add extra layer of encryption, making it impossible to decrypt


def pad_message(message):
    padding_length = AES.block_size - (len(message) % AES.block_size)
    padding = bytes([padding_length]) * padding_length
    return message + padding


cipher = AES.new(key, mode, IV)

message = b"My Name is Xiaoxiao Kumar Srinivasulu"
padded_message = pad_message(message)

encrypted_message = cipher.encrypt(padded_message)

print(encrypted_message)
