from implementation import ModifiedRC5
import random


def split(x):
    return x >> 32, x & 0xFFFFFFFF


def join(xl, xr):
    return (xl << 32) | xr


def main():
    K0 = random.getrandbits(32)
    K1 = random.getrandbits(32)
    encryptor = ModifiedRC5(K0, K1)

    P = random.getrandbits(64)
    C = join(*encryptor.encrypt(*split(P)))

    print(f"Key: {K0:x} {K1:x}")
    print(f"Known Plaintext: {P:x}")
    print(f"Known Ciphertext: {C:x}")

    # Get E(M, 0, 0)
    M = random.getrandbits(64)
    print(f"\nRandom Message: {M:x}")

    # E(M, K0, K1)
    E_message_original = encryptor.encrypt(*split(M))
    E_message_original = join(*E_message_original)
    print("Encrypting M with the original key")
    print(f"E(M, K0, K1) =  {E_message_original:x}")

    print("\nPerforming attack with known plaintext-ciphertext pair...")
    zero_encryptor = ModifiedRC5(0, 0)

    # Get E(P, 0, 0)
    E_Pzero = zero_encryptor.encrypt(*split(P))
    E_Pzero = join(*E_Pzero)
    print(f"E(P, 0, 0) = {E_Pzero:x}")

    # Get E(0, K0, K1) = E(P, K0, K1) xor E(P, 0, 0)
    E_zeroK0K1 = C ^ E_Pzero
    print(f"E(0, K0, K1) = {E_zeroK0K1:x}")

    # Get E(M, 0, 0)
    E_Mzero = zero_encryptor.encrypt(*split(M))
    E_Mzero = join(*E_Mzero)
    print(f"E(M, 0, 0) = {E_Mzero:x}")

    # E(M, K0, K1) = E(M, 0, 0) xor E(0, K0, K1)
    E_message = E_Mzero ^ E_zeroK0K1
    print("E(M, K0, K1) = E(M, 0, 0) xor E(0, K0, K1)")
    print(f"\t= {E_Mzero:x} xor {E_zeroK0K1:x}")
    print(f"\t= {E_message:x}")

    print(f"E_message == E_message_original ? {E_message == E_message_original}")


if __name__ == "__main__":
    main()
