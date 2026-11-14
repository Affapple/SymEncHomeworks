from dataclasses import dataclass, field
import json
import numpy as np


def read_data(filepath):
    with open(filepath, "r") as f:
        data = f.read()
    return json.loads(data)


def hex_string_to_bytes(hex_string):
    return bytes.fromhex(hex_string)


def to_hex(x) -> str:
    return f"{x:02x}"


def print_hex(b: np.ndarray):
    with np.printoptions(formatter={"int": to_hex, "int_kind": to_hex}):
        print(b)


def convert_to_matrix(array: np.ndarray) -> np.ndarray:
    temp = np.zeros((4, 4), dtype=np.uint8)
    temp[:, 0] = array[0:4]
    array = temp  # type: ignore
    return array
