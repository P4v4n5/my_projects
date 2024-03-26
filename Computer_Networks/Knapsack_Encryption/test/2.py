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


# Example usage:
plaintext_message = [1, 0, 0, 1, 0, 0, 0]
public_key = [68, 27, 54, 108, 107, 105]

# Encrypt the message
ciphertext = encrypt_message(plaintext_message, public_key)
print(ciphertext)

# n_inv = modInverse(31,110)
# print(n_inv)
