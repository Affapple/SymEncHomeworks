from utils import read_data
from implementation import LFSR, Geffe


def findLFSRKey(lfsr: LFSR, stream: list[int], expected_corr: float) -> list[int]:
    lfsrSize = lfsr.n
    bestMatchProb = 0.0
    minMatchDiff = 1.0
    bestState = [0] * lfsrSize

    for lfsr_key in range(2**lfsrSize):
        state = [(lfsr_key >> bitPos) & 1 for bitPos in range(lfsrSize)]
        lfsr.init(state)

        match_count = 0
        for outputIdx in range(len(stream)):
            expected_bit = stream[outputIdx]
            output_bit = lfsr.clock()

            if output_bit == expected_bit:
                match_count += 1

        prob = match_count / len(stream)
        diff = abs(expected_corr - prob)
        if diff < minMatchDiff:
            minMatchDiff = diff
            bestMatchProb = prob
            bestState = state

    print("Best correlation probability: ", bestMatchProb)
    return bestState


def findSecondLFSRKey(
    lfsrs: tuple[LFSR, LFSR, LFSR], stream: list[int], F_function: list[int]
) -> list[int]:
    lfsrSize = lfsrs[0].n
    maxMatch_count = 0
    bestState = [0] * lfsrSize

    lfsr0, lfsr1, lfsr2 = lfsrs
    x0_outputs = [lfsr0.clock() for _ in range(len(stream))]
    x2_outputs = [lfsr2.clock() for _ in range(len(stream))]

    for lfsr_key in range(2**lfsrSize):
        state = [(lfsr_key >> bitPos) & 1 for bitPos in range(lfsrSize)]
        lfsr1.init(state)

        match_count = 0
        for outputIdx in range(len(stream)):
            first_lfsr_bit = x0_outputs[outputIdx]
            second_lfsr_bit = lfsr1.clock()
            third_lfsr_bit = x2_outputs[outputIdx]

            output_bit = F_function[
                (first_lfsr_bit << 2) | (second_lfsr_bit << 1) | third_lfsr_bit
            ]
            expected_bit = stream[outputIdx]
            if output_bit == expected_bit:
                match_count += 1

        if maxMatch_count < match_count:
            maxMatch_count = match_count
            bestState = state

    print(f"Best match count: {maxMatch_count} out of {len(stream)}")
    return bestState


def checkFinalStream(geffe: Geffe, stream: list[int]):
    numMatches = 0
    for outputIdx in range(len(stream)):
        expected_bit = stream[outputIdx]
        output_bit = geffe.clock()
        if output_bit == expected_bit:
            numMatches += 1
    print(f"Number of matches: {numMatches} out of {len(stream)}")


def main():
    data = read_data("data.json")
    ex_data = data["2"]
    stream = ex_data["KEYSTREAM"]
    f_function = ex_data["F-FUNCTION"]
    F_function = [int(bit) for bit in f_function]

    streamArray = [int(bit) for bit in stream]

    LFSR_SIZE = 16
    lfsr0_taps = [0, 1, 4, 7]
    lfsr1_taps = [0, 1, 7, 11]
    lfsr2_taps = [0, 2, 3, 5]

    lfsr0 = LFSR(LFSR_SIZE, lfsr0_taps)
    lfsr1 = LFSR(LFSR_SIZE, lfsr1_taps)
    lfsr2 = LFSR(LFSR_SIZE, lfsr2_taps)

    # Find first LFSR key
    corr = 2 / 8
    lfsr0_bestState = findLFSRKey(lfsr0, streamArray, corr)
    print("Best state for LFSR 0:")
    print(lfsr0_bestState)

    # Find third LFSR key
    corr = 2 / 8
    lfsr2_bestState = findLFSRKey(lfsr2, streamArray, corr)
    print("Best state for LFSR 2:")
    print(lfsr2_bestState)

    # Find second LFSR key
    lfsr0.init(lfsr0_bestState)
    lfsr2.init(lfsr2_bestState)
    lfsr1_bestState = findSecondLFSRKey((lfsr0, lfsr1, lfsr2), streamArray, F_function)
    print("Best state for LFSR 1:")
    print(lfsr1_bestState)

    print("\n### Final Machine ###")
    # Get K = (k0, k1, k2)
    key = lfsr0_bestState, lfsr1_bestState, lfsr2_bestState
    # Get all states, convert them into an integer representation of the key
    ikey = [sum([2**i * ki[i] for i in range(len(ki))]) for ki in key]
    geffe = Geffe(
        LFSR_SIZE,
        [lfsr0_taps, lfsr1_taps, lfsr2_taps],
        F_function,
    )
    geffe.set_state(ikey)

    # Just to do a final redudant check as we expect the exact same value as before
    checkFinalStream(geffe, streamArray)


if __name__ == "__main__":
    main()
