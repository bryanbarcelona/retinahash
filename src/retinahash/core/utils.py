import numpy as np


def bits_to_hex(bits: np.ndarray) -> str:
    """
    Converts a boolean/binary array into a hex string.
    Scales automatically based on the size of the input array.
    """
    # Make 'em 1D
    flat_bits = bits.flatten()

    # Make 'em bits eine GANZZAHL!
    bit_string = "".join(str(int(b)) for b in flat_bits)
    hash_int = int(bit_string, 2)

    # How many hex digits do we need?
    hex_length = len(flat_bits) // 4

    # Zero-padding...you know if you know
    return f"{hash_int:0{hex_length}x}"


def hamming_distance(hex1: str, hex2: str) -> int:
    """
    Computes the number of bit positions in which the two hex strings differ.
    """
    # XOR!!!!!! RAWRRRR
    return bin(int(hex1, 16) ^ int(hex2, 16)).count("1")
