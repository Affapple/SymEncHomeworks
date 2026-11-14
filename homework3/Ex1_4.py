import numpy as np
from tqdm import tqdm
from utils import print_hex, read_data, hex_string_to_bytes
from Crypto.Cipher import AES as AES_Cipher
from AES import AES
# Let C = AES128(AES128(P, k1), k2), i.e. the plaintext P is encrypted using
# AES-128 with key k1 and then the result is encrypted with the key k2. Assume
# that k1 and k2 are both 24-bit keys followed by 104 zero bits. Recover the keys
# given a single plaintext-ciphertext pair (P, C). Report the recovered keys, code,
# time and memory complexity of your attack.


naive = AES()
# ECB because we only encrypt one block


def encrypt(plaintext_bytes, key_int):
    key_bytes = key_int.to_bytes(3, "big") + bytes(13)  # 24 bits + 104 zero bits
    aes = AES_Cipher.new(key_bytes, AES_Cipher.MODE_ECB)
    return aes.encrypt(plaintext_bytes)


def decrypt(ciphertext_bytes, key_int):
    key_bytes = key_int.to_bytes(3, "big") + bytes(13)
    aes = AES_Cipher.new(key_bytes, AES_Cipher.MODE_ECB)
    return aes.decrypt(ciphertext_bytes)


def meet_in_the_middle(P, C) -> tuple[int, int] | tuple[None, None]:
    # Encrypt P
    table = {}
    for k1 in tqdm(range(2**24)):
        M = int.from_bytes(encrypt(P, k1), "big")
        table[M] = k1

    # Decrypt C, look for match
    for k2 in tqdm(range(2**24)):
        # Big or little doesnt matter, just that it is consitent with previous step
        M = int.from_bytes(decrypt(C, k2), "big")
        if M in table:  # Found a match
            k1 = table[M]
            return k1, k2  # Return full keys

    return None, None


if __name__ == "__main__":
    data = read_data("data.json")["1.4"]
    P = hex_string_to_bytes(data["plaintext"])
    C = hex_string_to_bytes(data["ciphertext"])

    k1, k2 = meet_in_the_middle(P, C)

    if k1 is None or k2 is None:
        print("Something went wrong, no keys found")
        exit(-1)

    k1 <<= 104  # Shift back to full key
    k2 <<= 104  # Shift back to full key
    print("Found keys:")
    print(f"k1: {k1:x}")
    print(f"k2: {k2:x}")
