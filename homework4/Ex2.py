from tqdm import tqdm
from cryptography.hazmat.primitives import hashes
import random


def infinite_loop():
    """Used for tqdm"""
    while True:
        yield


def hash_message(message: str | bytes) -> bytes:
    hash_function = hashes.Hash(hashes.SHA256())
    hash_function.update(message.encode() if isinstance(message, str) else message)
    hash = hash_function.finalize()

    # Returns the first 6*8 = 48 bits
    return hash[:6]


NAME = b"Joao"


def step(digest: bytes) -> bytes:
    return hash_message(NAME + digest)


if __name__ == "__main__":
    # Set same starting point for both fast and slow
    initial = fast = slow = step(random.randbytes(8))

    # DO first step outside the loop to avoid immediate collision
    fast = step(step(fast))
    slow = step(slow)

    for _ in tqdm(
        infinite_loop(),
        desc="Finding Cicle",
        unit="attempts",
        total=2**24,  # birthday bound is 2**24
    ):
        if fast == slow:
            # There is a collision
            break

        fast = step(step(fast))
        slow = step(slow)

    finder = initial
    for _ in tqdm(
        infinite_loop(),
        desc="Finding Collision",
        unit="attempts",
        total=2**24,  # birthday bound is 2**24
    ):
        nf = step(finder)
        ns = step(slow)
        if nf == ns and slow != finder:
            break  # Collision found
        finder = nf
        slow = ns

    m1 = NAME + finder
    m2 = NAME + slow
    print("Collision found!")
    print(f"Message 1: {NAME.decode()}||{finder.hex()}")
    print(f"Message 2: {NAME.decode()}||{slow.hex()}")

    print(f"Hash 1: {hash_message(m1).hex()}")
    print(f"Hash 2: {hash_message(m2).hex()}")
