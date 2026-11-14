from random import randint


class LFSR(object):
    def __init__(self, n, taps):
        self.n = n

        self.taps = tuple(taps)
        assert self.taps[0] == 0
        assert 0 <= min(self.taps) <= max(self.taps) <= n - 1

        self.state = (0,) * n

    def init(self, state):
        assert len(state) == self.n
        self.state = tuple(state)

    def init_random(self):
        self.state = tuple(randint(0, 1) for _ in range(self.n))

    def clock(self):
        output = self.state[0]
        new_val = 0
        for t in self.taps:
            new_val ^= self.state[t]
        self.state = self.state[1:] + (new_val,)
        return output

    def filter(self, eq):
        """Example:
        eq = [(0, 2), (4, 20), (3,), (7,)]
        corresponds to filter
        s0*s2 + s4*s20 + s3*s7
        """
        output = 0
        for monomial in eq:
            monomial_value = 1
            for varindex in monomial:
                monomial_value &= self.state[varindex]
            output ^= monomial_value
        return output

    def __str__(self):
        output = ""
        for i in reversed(range(0, self.n)):
            # reversed because we print S_0 to the right
            output += str(self.state[i])
        return output


class Geffe(object):
    def __init__(self, n, all_taps, F):
        assert len(all_taps) == 3
        assert len(F) == 8
        self.L = [LFSR(n, taps) for taps in all_taps]
        self.n = n
        self.F = F

    def set_state(self, k):
        states = [[], [], []]
        k = list(k)
        for i in range(self.n):
            for s in range(3):
                states[s].append(k[s] % 2)
                k[s] = k[s] // 2

        for s in range(3):
            self.L[s].init(states[s])

    def clock(self):
        f_input = 0
        for s in range(3):
            f_input = (f_input << 1) | (self.L[s].clock())
        return self.F[f_input]

    def __str__(self):
        output = ""
        for s in range(3):
            output += str(self.L[s]) + " "
        return output[:-1]


class FilteredLFSR(object):
    """
    example: F = [(0, 2), (4, 20), (3,), (7,)]
    """

    def __init__(self, n, taps, F):
        self.L = LFSR(n, taps)
        self.L.init_random()  # random initial state
        self.eq = tuple(F)

    def clock(self):
        output = self.L.filter(self.eq)
        self.L.clock()
        return output


class ModifiedRC5(object):
    def __init__(self, k0, k1):
        assert 0 <= k0 < 2**32
        assert 0 <= k1 < 2**32
        self.k = k0, k1

    def rotate_left(self, w, n):
        w &= 0xFFFFFFFF
        w = (w << n) | (w >> (32 - n))
        w &= 0xFFFFFFFF
        return w

    def encrypt(self, xl, xr):
        assert 0 <= xl < 2**32
        assert 0 <= xr < 2**32
        for roundno in range(12):
            xl ^= xr
            xl = self.rotate_left(xl, 7)
            xl ^= self.k[0]

            # swap
            xl, xr = xr, xl

            xl ^= xr
            xl = self.rotate_left(xl, 7)
            xl ^= self.k[1]

            # swap
            xl, xr = xr, xl
        return xl, xr


if __name__ == "__main__":
    # # 1. Example using LFSR with taps 0,3,5,9
    # #    and initial state s0=0, s1=1, s2=0, s3=1, s4=1, ...
    # lfsr = LFSR(32, [0, 3, 5, 9])
    # lfsr.init(
    #     [
    #         0,
    #         1,
    #         0,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #         1,
    #     ]
    # )
    # print("LFSR")
    # print("taps", lfsr.taps)
    # print("state", lfsr)
    # stream = [lfsr.clock() for i in range(10)]
    # print("stream", stream)
    # print()
    #
    # # 2. Example of Geffe cipher
    # #    3 LFSRs of 16-bit size with taps
    # #    [0, 3, 5, 7], [0, 1, 8], [0, 10, 11, 12]
    # #    filter function's truth table [0, 0, 1, 0, 1, 1, 0, 0]
    # G = Geffe(16, [[0, 3, 5, 7], [0, 1, 8], [0, 10, 11, 12]], [0, 0, 1, 0, 1, 1, 0, 0])
    # #    integer representaations of initial states ("keys")
    # G.set_state(
    #     [
    #         # MSB .... LSB
    #         # s15,s14,...,s0
    #         0b0101100101010011,
    #         0b1010010111010010,
    #         0b0001111101010011,
    #     ]
    # )
    # print("Geffe", G)
    # for l in G.L:
    #     print("taps", l.taps, "state", l)
    # stream = [G.clock() for i in range(50)]
    # print("stream", stream)
    # print()
    #
    # 3. Example of Modified-RC5
    # Operates on 32-bit integers
    # using 2 32-bit keys
    print("Modified-RC5")
    key = 0xABCDEFFF, 0xCAFE1234
    key = 0x0, 0x0
    Cipher = ModifiedRC5(key[0], key[1])
    plaintext = 0x11223344, 0xAABBCCDD
    plaintext = 0xCCCCCCCC, 0xDDDDDDDD
    ciphertext = Cipher.encrypt(plaintext[0], plaintext[1])
    print("       key {:032b} {:032b}".format(*key))
    print(" plaintext {:032b} {:032b}".format(*plaintext))
    print("ciphertext {:032b} {:032b}".format(*ciphertext))

"""
LFSR
taps (0, 3, 5, 9)
state 11111111111111111111111111111010
stream [0, 1, 0, 1, 1, 1, 1, 1, 1, 1]

Geffe 0101100101010011 1010010111010010 0001111101010011
taps (0, 3, 5, 7) state 0101100101010011
taps (0, 1, 8) state 1010010111010010
taps (0, 10, 11, 12) state 0001111101010011
stream [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1]

Modified-RC5
       key abcdefff cafe1234
 plaintext 11223344 aabbccdd
ciphertext c982aba4 c22946ad
"""
