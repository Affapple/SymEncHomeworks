import sys
from tqdm import tqdm
from cryptography.hazmat.primitives import hashes
import random
from itertools import product

baseline_text = (
    "Hash functions are functions that take an arbitrarily sized input and produce a fixed size output."
    " They are an essential component of modern cryptography."
)
alternatives = (
    "{} {} {} {} {} {} {} {} {} {} {} {} {} {}. {} {} {} {} of modern cryptography."
)


def hash_message(message: str | bytes) -> bytes:
    hash_function = hashes.Hash(hashes.SHA256())
    hash_function.update(message.encode() if isinstance(message, str) else message)
    hash = hash_function.finalize()
    return hash[:2]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Ex3.py [4-letter hex string]")
        sys.exit(1)
    target = bytes.fromhex(sys.argv[1])[:2]
    hash = hash_message(baseline_text)

    print(f"Message hash: {hash.hex()}")
    print(f"Target  hash: {target.hex()}")

    modifications = [
        ["Hash functions", "Hashing algorithms", "Cryptographic hash functions"],
        ["are", "represent"],
        ["functions", "tools"],
        ["that", ", which"],
        ["take", "accept", "ingest"],
        ["an arbitrarily", "a varying"],
        ["sized", "length"],
        ["input", "data block", "data"],
        ["and", "to then"],
        ["produce", "generate", "return"],
        ["a", "a single"],
        ["fixed", "constant", "static"],
        ["size", "length"],
        ["output", "result", "digest"],
        ["They", "These", "Such functions"],
        ["are", "represent", "constitute"],
        ["a vital", "a key", "an essential"],
        ["component", "part", "element"],
    ]

    colision_found = True
    modified_text = baseline_text
    for permutation in tqdm(product(*modifications), total=16):
        modified_text = alternatives.format(*permutation)
        if hash_message(modified_text) == target:
            colision_found = True
            break

    if colision_found:
        print(f"Found a collision:\n{modified_text}")
        print("With hash:", hash_message(modified_text).hex())
    else:
        print("No collision found.")

# Ensure that the hash of the program = hash(Joao)
# =5f2e
# Random nonce:
# d124b0beee2ad075bc341e8fac913440