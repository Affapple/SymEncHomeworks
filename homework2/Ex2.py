import numpy as np
from utils import read_data
import ast


def squareAndMultiply(M, n):
    A = np.eye(M.shape[0], dtype=M.dtype)  # Identity matrix
    B = M.copy()
    binary_n = bin(n)[2:][::-1]  # Get binary representation of n

    for bit in binary_n:
        if bit == "1":  # If n is odd
            A = np.mod(A @ B, 2)
        B = np.mod(B @ B, 2)  # Square the matrix

    return A


def getStateAfterTicks(A, s_0, num_ticks):
    A_n = squareAndMultiply(A, num_ticks)
    return np.mod(A_n @ s_0, 2)


def main():
    data = read_data("data.json")
    exponent = 2**64 + 13
    ex_data = data["1"]
    taps: list[int] = [127 - tap for tap in ast.literal_eval(ex_data["TAPS"])]

    # Create LFSR Matrix A
    A = np.zeros(shape=(128, 128), dtype=np.int64)
    A[0, taps] = 1  # Set the taps in the first row
    A[1:, :] = np.eye(127, 128)  # Add the identity matrix for the shift

    # Initial state with all bits set to 1
    s_0 = np.ones(128, dtype=np.int64)
    s_n = getStateAfterTicks(A, s_0, exponent)

    print(f"Internal State after 2^64+13 ticks:\n{s_n}")


if __name__ == "__main__":
    main()
