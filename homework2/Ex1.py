import ast
from implementation import LFSR
from utils import read_data

if __name__ == "__main__":
    n = 128  # Number of bits in the LFSR

    data = read_data("data.json")["1"]
    taps = [tap for tap in ast.literal_eval(data["TAPS"])]
    print(taps)
    state = data["STREAM"][:n]

    # Example usage of LFSR
    lfsr = LFSR(n, taps)
    lfsr.init([int(bit) for bit in state])

    print("Initial state:", lfsr)

    # Generate and print the first 10 outputs of the LFSR
    state = [0] * 256
    for i in range(256):
        output = lfsr.clock()
        state[i] = output

    output_stream = "".join(str(bit) for bit in state)
    expected_stream = data["STREAM"][:256]
    print("Generated stream: ", output_stream)
    print("Output matched expected? ", output_stream == expected_stream)
