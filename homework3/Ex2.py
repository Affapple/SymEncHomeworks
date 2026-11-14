from DES_util import (
    encrypt_7_rounds,
    sbox,
    expand,
    apply_p_inv,
    apply_inv_pc2,
    apply_inv_pc1,
    rshift,
)
from itertools import product
from math import prod
from tqdm import tqdm
import json


# Reimplemented these functions
# To avoid numpy import
def read_data(filepath):
    with open(filepath, "r") as f:
        data = f.read()
    return json.loads(data)


def hex_string_to_bytes(hex_string):
    return bytes.fromhex(hex_string)


def sbox_analysis(data):
    """IMplementation of Exercise 2.1"""
    # Value from the table
    # num_pairs = 2

    delta_out = int.from_bytes(hex_string_to_bytes(data["delta_out"]), byteorder="big")
    delta_in = int.from_bytes(hex_string_to_bytes(data["delta_in"]), byteorder="big")
    for i in range(2**6):
        i_xor_din = i ^ delta_in
        if sbox(1, i) ^ sbox(1, i_xor_din) == delta_out:
            print(f"Found pair: 0x{i:02x} and 0x{i_xor_din:02x}")


DELTA_PREV_LEFT = 0x40_5C_00_00
DELTA_PREV_RIGHT = 0x04_00_00_00


def attack_from_end(pairs):
    # Scores for each key guess for each S-box
    scores = {i: [0] * 64 for i in range(1, 9)}
    for c, c_star in pairs["c"]:
        # Get left and right halves
        c_left = c >> 32
        c_right = c & 0xFFFFFFFF
        c_star_left = c_star >> 32
        c_star_right = c_star & 0xFFFFFFFF

        # Get delta_out
        delta_out = c_left ^ c_star_left ^ DELTA_PREV_LEFT
        # Remove P permutation
        delta_sbox_out = apply_p_inv(delta_out)

        # Expanded right halves before key XOR
        E_c_right = expand(c_right)
        E_c_star_right = expand(c_star_right)

        delta_E = E_c_right ^ E_c_star_right

        for sbox_id in range(1, 8 + 1):
            # Get expected XOR for this S-box (we know its 0x)
            expected_xor = (delta_sbox_out >> (32 - 4 * sbox_id)) & 0b1111

            # 6-bit input to S-box (before key XOR)
            e_c_sbox = (E_c_right >> (48 - 6 * sbox_id)) & 0x3F
            e_c_star_sbox = (E_c_star_right >> (48 - 6 * sbox_id)) & 0x3F

            for k in range(64):
                out = sbox(sbox_id, e_c_sbox ^ k)
                out_star = sbox(sbox_id, e_c_star_sbox ^ k)
                if (out ^ out_star) == expected_xor:
                    scores[sbox_id][k] += 1

    potential_keys = {}
    print("--- Subkey K7 Recovery ---")
    for sbox_id in range(1, 9):
        max_score = max(scores[sbox_id])
        if max_score > 0:
            # Find all 6-bit keys that share the maximum score
            best_keys = [
                k for k, score in enumerate(scores[sbox_id]) if score == max_score
            ]
            hex_keys = [f"0x{k:02x}" for k in best_keys]
            potential_keys[sbox_id] = best_keys
            print(
                f"S-box {sbox_id}: Best K7 subkey(s) = {hex_keys} (Score: {max_score}/{len(pairs['c'])})"
            )
        else:
            print(f"S-box {sbox_id}: No data (Inactive)")
    return potential_keys


def reconstructMasterKey(
    potential_subkeys: dict[int, list[int]], known_plaintext, known_ciphertext
):
    key_combinations = product(*potential_subkeys.values())
    total_combinations = prod(len(keys) for keys in potential_subkeys.values())

    # Note: Only PC2 dropped bits, PC1 are EC parity bits
    # For PC2 (calculated with set(PC2))
    unknown_bits = [8, 17, 21, 24, 34, 37, 42, 53]  #
    unknown_bits = [2, 13, 18, 21, 31, 34, 38, 47]  # reverse way of counting bits

    found_key = None
    for combination in tqdm(
        key_combinations,
        desc="Testing key combinations",
        total=total_combinations,
    ):
        # Construct the 48-bit round key from the combination
        round_key = 0
        for sbox_id in range(8):
            round_key <<= 6
            round_key |= combination[sbox_id]

        key_guess = apply_inv_pc2(round_key)
        # Test with all bits that were lost in the key schedule
        for i in range(256):
            # keeps unknown bits as 0 and sets them according to the current combination
            test_key = key_guess
            for j in range(8):
                bit_pos = unknown_bits[j]
                bit_val = (i >> j) & 1
                test_key |= bit_val << bit_pos

            # Then shifts the key back to K_0 (no the best solution, but its not the bottleneck of the attack)
            Cn, Dn = test_key >> 28, test_key & 0xFFFFFFF
            Cn, Dn = rshift(Cn, Dn, num_shifts=12)
            test_key = Cn << 28 | Dn

            encrypted_guess = encrypt_7_rounds(known_plaintext, test_key)

            if encrypted_guess == known_ciphertext:
                found_64bitkey = apply_inv_pc1(test_key)
                return found_64bitkey


def differential_cryptanalysis_des(data):
    """Implementation of Exercise 2.2"""
    pairs = {
        "p": [
            (
                int.from_bytes(hex_string_to_bytes(data[f"p{i}"]), byteorder="big"),
                int.from_bytes(hex_string_to_bytes(data[f"p{i}*"]), byteorder="big"),
            )
            for i in range(1, len(data) // 4 + 1)
        ],
        "c": [
            (
                int.from_bytes(hex_string_to_bytes(data[f"c{i}"]), byteorder="big"),
                int.from_bytes(hex_string_to_bytes(data[f"c{i}*"]), byteorder="big"),
            )
            for i in range(1, len(data) // 4 + 1)
        ],
    }

    potential_subkeys = attack_from_end(pairs)
    master_key = reconstructMasterKey(
        potential_subkeys=potential_subkeys,
        known_plaintext=pairs["p"][0][0],
        known_ciphertext=pairs["c"][0][0],
    )
    if master_key is None:
        print("Failed to recover the master key.")
    else:
        print(f"Recovered Master Key: 0x{master_key:016X}")


if __name__ == "__main__":
    # Ex 2.1 Analyse one S-Box
    data = read_data("data.json")
    print("Exercise 2.1: S-Box Analysis")
    sbox_analysis(data["2.1"])

    print("\nExercise 2.2: Differential Cryptanalysis on DES")
    differential_cryptanalysis_des(data["2.2"])
