import numpy as np

from AES import AES
from utils import read_data, print_hex, convert_to_matrix

DATA = read_data("data.json")


def ComputeB(aes: AES, a: np.ndarray):
    # Subbytes
    b = aes.SubBytes(a)
    # Create matrix instead of just column, for compatibility with MixColumns
    b = convert_to_matrix(b)
    # MixColumns
    b = aes.MixColumns(b)
    print_hex(b[:, 0])

    return b


def ComputeAB_star(aes: AES, a: np.ndarray, b: np.ndarray, delta: np.ndarray):
    # Compute b*
    delta = convert_to_matrix(delta)
    b_star = b ^ delta

    # Compute a*
    a_star = aes.inv_SubBytes(aes.inv_MixColumns(b_star))  # type: ignore

    print("a_star")
    print_hex(a_star[:, 0])

    print("b_star")
    print_hex(b_star[:, 0])

    return a_star[:, 0], b_star[:, 0]


aes = AES()
if __name__ == "__main__":
    print("Ex1.1.1: ")
    a_str = DATA["1.1"]["a-bytes"]
    a = np.array([byte for byte in bytes.fromhex(a_str)], dtype=np.uint8)
    b = ComputeB(aes, a)
    print()

    print("Ex1.1.2: ")
    delta = np.array(
        [byte for byte in bytes.fromhex(DATA["1.1"]["delta"])], dtype=np.uint8
    )
    a_star, b_star = ComputeAB_star(aes, a, b, delta)
