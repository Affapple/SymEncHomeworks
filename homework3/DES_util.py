# fmt: off
S_BOXES: dict[int, list[list[int]]] = {
    1: [
        [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
        [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
        [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
        [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13],
    ],
    2: [
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
        [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
        [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
        [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9],
    ],
    3: [
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
        [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
        [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
        [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12],
    ],
    4: [
        [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
        [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
        [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
        [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14],
    ],
    5: [
        [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
        [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
        [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
        [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3],
    ],
    6: [
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
        [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
        [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
        [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13],
    ],
    7: [
        [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
        [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
        [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
        [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12],
    ],
    8: [
        [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
        [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
        [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
        [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11],
    ],
}
# Expansion E
E_TABLE = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1,
]
 
# P permutation
P_TABLE = [
    16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25,
]
# Inverse Permutation table
_P_INV = [0] * 32
for i, pos in enumerate(P_TABLE):
    _P_INV[pos - 1] = i + 1
# fmt: on


def sbox(sbox_id: int, input: int) -> int:
    s_box = S_BOXES[sbox_id]
    first_bit = (input >> 5) & 0b1
    last_bit = input & 0b1
    middle_bits = (input >> 1) & 0b1111

    row = (first_bit << 1) | last_bit
    col = middle_bits

    return s_box[row][col]


def _apply_perm(val: int, table: list[int], in_bits: int) -> int:
    """AI Generated Code"""
    result = 0
    out_bits = len(table)
    for i, bit_pos in enumerate(table):
        bit = (val >> (in_bits - bit_pos)) & 1
        result |= bit << (out_bits - 1 - i)
    return result


def expand(R: int) -> int:
    """32-bit -> 48-bit expansion."""
    return _apply_perm(R, E_TABLE, 32)


def apply_p(val: int) -> int:
    return _apply_perm(val, P_TABLE, 32)


def apply_p_inv(val: int) -> int:
    return _apply_perm(val, _P_INV, 32)


# fmt: off
def rshift(C: int, D: int, num_shifts: int) -> tuple[int, int]:
    """Right shift C and D, from round 7 to round 0."""
    num_bits = 28
    # Perform the right shift
    new_C = ((C >> num_shifts) | (C << num_bits-num_shifts)) & 0xFFFFFFF
    new_D = ((D >> num_shifts) | (D << num_bits-num_shifts)) & 0xFFFFFFF
    return new_C, new_D

PC1 = [
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
]
PC2 = [
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]
def apply_inv_pc1(key_56: int) -> int:
    """AI Generated Code, with adjustments"""
    key_64 = 0
    for idx, bit_pos in enumerate(PC1):
        bit = (key_56 >> (55 - idx)) & 1
        # 63 - 1 - bit_pos
        key_64 |= bit << (64 - bit_pos)
    return key_64

def apply_inv_pc2(key_48: int) -> int:
    """AI Generated Code, with adjustments"""
    key_56 = 0
    for idx, original_position in enumerate(PC2):
        bit = (key_48 >> (47 - idx)) & 1
        key_56 |= (bit << (56 - original_position))
    return key_56
# fmt: on


def lshift(C: int, D: int, num_shifts: int) -> tuple[int, int]:
    """Right shift C and D, from round 7 to round 0."""
    num_bits = 28
    # Perform the right shift
    new_C = ((C << num_shifts) | (C >> num_bits - num_shifts)) & 0xFFFFFFF
    new_D = ((D << num_shifts) | (D >> num_bits - num_shifts)) & 0xFFFFFFF
    return new_C, new_D


DES_LSHIFTS = [1, 1, 2, 2, 2, 2, 2]


def apply_pc2(key_56: int) -> int:
    """Standard DES PC-2: Compresses 56-bit to 48-bit"""
    """AI Generated Code"""
    res_48 = 0
    for i, pos in enumerate(PC2):
        bit = (key_56 >> (56 - pos)) & 1
        res_48 |= bit << (47 - i)
    return res_48


def apply_pc1(key_64: int) -> int:
    """Standard DES PC-1: Compresses 64-bit Master Key to 56-bit Internal Key"""
    """AI Generated Code"""
    res_56 = 0
    for i, pos in enumerate(PC1):
        bit = (key_64 >> (64 - pos)) & 1
        res_56 |= bit << (55 - i)
    return res_56


def encrypt_7_rounds(plaintext: int, key_56: int) -> int:
    """Quick and idrty implementation of 7 rounds of DES, used for the key recovery attack."""
    """Mostly AI generated code with manual adjustments"""
    L = plaintext >> 32
    R = plaintext & 0xFFFFFFFF

    C = key_56 >> 28
    D = key_56 & 0xFFFFFFF

    for round_idx in range(7):
        C, D = lshift(C, D, DES_LSHIFTS[round_idx])
        k_round = apply_pc2((C << 28) | D)

        E_R = expand(R)
        B = E_R ^ k_round

        sbox_out = 0
        for s in range(1, 9):
            chunk = (B >> (48 - 6 * s)) & 0x3F
            sbox_val = sbox(s, chunk)
            sbox_out |= sbox_val << (32 - 4 * s)

        f_out = apply_p(sbox_out)

        next_L = R
        next_R = L ^ f_out

        L = next_L
        R = next_R

    # Well, this actually also flips at the end according to FIPS 46-3...
    # Instead of L || R, it's R || L
    return (R << 32) | L
