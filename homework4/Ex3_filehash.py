from tqdm import tqdm
from cryptography.hazmat.primitives import hashes
import random


def infinite_loop():
    while True:
        yield


def compute_file_hash(file_data, nonce: bytes):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(file_data)
    if nonce is not None:
        digest.update(b"# " + nonce)
    return digest.finalize()


if __name__ == "__main__":
    file_name = "./Ex3.py"
    with open(file_name, "rb") as fr:
        file_data = fr.read()

    # We only care about the first 2 bytes of the hash
    digest = hashes.Hash(hashes.SHA256())
    digest.update(b"Joao")
    expected_hash = digest.finalize()[:2]

    # Initial verificatoin just to make sure we dont need to write the nonce to the file
    computed_hash = compute_file_hash(file_data, None)
    if expected_hash == computed_hash:
        print(
            "Verification successful: Hash values match! No need to add a nonce to the file."
        )
        exit(0)

    for _ in tqdm(
        infinite_loop(), desc="Searching for a nonce that produces the expected hash..."
    ):
        nonce = random.randbytes(16).hex().encode()  # Generate a random nonce
        computed_hash = compute_file_hash(file_data, nonce)[:2]

        if expected_hash == computed_hash:
            print("Hash values match!")
            print("Writing the correct hash value to the file...")
            with open(file_name, "ab") as fw:
                fw.write(b"# " + nonce)
                break

    # Verification
    with open(file_name, "rb") as fr:
        file_data = fr.read()
    computed_hash = compute_file_hash(file_data, None)
    if expected_hash == computed_hash:
        print("Verification successful: Hash values match!")
