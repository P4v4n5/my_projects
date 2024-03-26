from Crypto.Cipher import AES
import hashlib
import os

shared_secret = 23
password = str(shared_secret).encode()
print("Length of encoded shared secret:", len(password))
key = hashlib.sha256(password).digest()
mode = AES.MODE_CBC
IV = b'This is an IV456'

def pad_message(message):
    padding_length = AES.block_size - (len(message) % AES.block_size)
    padding = bytes([padding_length]) * padding_length
    return message + padding

def unpad_message(padded_message):
    padding_length = padded_message[-1]
    return padded_message[:-padding_length]

cipher = AES.new(key, mode, IV)

encrypted_message = b'\x8c\x88\x04\xdd\xd3\x02R\xb8\\\xfb\xbb\xb1=d\xc8\x8c\x84Ac\x1e\xf8\xe3\x1d\xeab\x15\xaf\x939\x1fO\xa1\xfd\xe1\xccE\x8b\xae\xbbw\x0e\r?lwP\x14\xc1'

decrypted_padded_message = cipher.decrypt(encrypted_message)
decrypted_message = unpad_message(decrypted_padded_message)
print(decrypted_message)
