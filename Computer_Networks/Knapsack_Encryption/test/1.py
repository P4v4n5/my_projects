import random
from itertools import combinations


def generate_superincreasing_knapsack(n_elements):
    knapsack = []
    total = 0
    for i in range(n_elements):
        element = total + 1  # Make sure the next element is greater than the sum of previous elements
        knapsack.append(element)
        total += element
    return knapsack


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def generate_multiplexer_and_modulus(super_knapsack):
    total_sum = sum(super_knapsack)

    # Generate modulus (m) greater than the sum of the private key
    modulus = random.randint(total_sum + 1, 2 * total_sum)

    # Generate a multiplexer (multiplier) with no common factors with modulus
    multiplexer = random.randint(2, modulus - 1)
    while gcd(multiplexer, modulus) != 1:
        multiplexer = random.randint(2, modulus - 1)

    return multiplexer, modulus


public_key = []


def generate_public_key(super_knapsack, multipexer, modulus):
    for each in super_knapsack:
        each_pub = (each * multipexer) % modulus
        public_key.append(each_pub)
    return public_key


def modInverse(multiplexer, modulus):
    for X in range(1, modulus):
        if (((multiplexer % modulus) * (X % modulus)) % modulus == 1):
            return X
    return -1


# receive encrypted message from user, Cipher text
cipher_text = [176, 0]


def decrypt_matrix_generator(multiplexer, modulus):
    multiplexer_inverse = modInverse(multiplexer, modulus)  # n inverse
    print("multiplexer_inverse", multiplexer_inverse)
    decrypting_matrix = []

    for each in cipher_text:
        decrypting_matrix.append((each * multiplexer_inverse) % modulus)  # each of cipher text multiplied by inverse of n and then mod with modulus number
    return decrypting_matrix


# now compare decrypting matrix with plain text and see how to match it to make this each sum corrsponding to the plaintext with 0's and 1's

def find_combinations(pvt_key, n):
    valid_combinations = []
    for r in range(1, len(pvt_key) + 1):
        for combo in combinations(pvt_key, r):
            if sum(combo) == n:
                valid_combinations.append(combo)
    print(valid_combinations)

    #  since valid_combination is a list contaning tuple (since we use combinations lib here), to make it a pure list we follow below
    valid_combinations_list = []
    valid_combinations_list.extend(valid_combinations[0])
    print(valid_combinations_list)

    plain_text = []
    for each in pvt_key:
        if each in valid_combinations_list:
            plain_text.append(1)
        else:
            plain_text.append(0)

    return plain_text

if __name__ == "__main__":
    n = 6
    super_increasing_knapsack = generate_superincreasing_knapsack(n)
    print("super_increasing_knapsacks", super_increasing_knapsack)

    multiplexer_and_modulus = generate_multiplexer_and_modulus(super_increasing_knapsack)
    print("multiplexer_and_modulus", multiplexer_and_modulus)

    public_key = generate_public_key(super_increasing_knapsack, multiplexer_and_modulus[0], multiplexer_and_modulus[1])
    print("public_key", public_key)

    decryption_matrix = decrypt_matrix_generator(multiplexer_and_modulus[0], multiplexer_and_modulus[1])
    print("decryption_matrix:", decryption_matrix)

    # super_increasing_knapsack = [1, 2, 4, 8, 16, 32]
    # decryption_matrix = [23, 1, 65]
    final_list = []
    for each in decryption_matrix:
        combos = find_combinations(super_increasing_knapsack, each)
        final_list.extend(combos)

    print("Combinations:", final_list)
# from itertools import combinations
#
# def find_combinations(pvt_key, n):
#     valid_combinations = []
#     for i in n:
#         for r in range(1, len(pvt_key) + 1):
#             for combo in combinations(pvt_key, r):
#                 if sum(combo) == i:
#                     valid_combinations.append(combo)
#     print(valid_combinations)
#
#     #  since valid_combination is a list contaning tuple (since we use combinations lib here), to make it a pure list we do it as below
#     valid_combinations_list = []
#     for each_tuple in valid_combinations:
#         valid_combinations_list.extend(valid_combinations[valid_combinations.index(each_tuple)])
#         print(valid_combinations_list)
#
#     plain_text = []
#     for each in pvt_key:
#         if each in valid_combinations_list:
#             plain_text.append(1)
#         else:
#             plain_text.append(0)
#
#     return plain_text
#
# # Example usage:
# plaintext = [1, 2, 4, 10, 20, 40]
# target_number = [11, 17]
#
# # Find combinations
# combinations = find_combinations(plaintext, target_number)
# print("Combinations:", combinations)
