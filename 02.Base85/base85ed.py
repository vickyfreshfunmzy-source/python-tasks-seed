#!/usr/bin/env python3
"""
Base85 encoder and decoder
"""

from __future__ import annotations
from beartype import beartype

ALPHABET = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~"
DECODE_MAP = {char: i for i, char in enumerate(ALPHABET)}


@beartype
def encode(b: bytes) -> bytes:
    """
    Base85 encoder implemented from scratch
    """
    result: list[int] = []
    # Process input 4 bytes at a time
    for i in range(0, len(b), 4):
        chunk = b[i:i + 4]

        # Pad the chunk with null bytes to make it exactly 4 bytes long
        padded_chunk = chunk.ljust(4, b'\x00')

        # Convert the 4 bytes into a single 32-bit unsigned integer
        num = int.from_bytes(padded_chunk, byteorder='big')

        # Extract 5 Base85 characters by repeatedly dividing by 85
        encoded_chunk = []
        for _ in range(5):
            encoded_chunk.append(ALPHABET[num % 85])
            num //= 85

        # The division gives us the characters in reverse order
        encoded_chunk.reverse()

        # Remove padding characters (equivalent to pad=False)
        num_chars_to_keep = len(chunk) + 1
        result.extend(encoded_chunk[:num_chars_to_keep])

    return bytes(result)


@beartype
def decode(b: bytes) -> bytes:
    """
    Base85 decoder implemented from scratch
    """
    result: list[int] = []
    for i in range(0, len(b), 5):
        chunk = b[i:i + 5]

        padded_chunk = chunk.ljust(5, ALPHABET[-1:])

        # Convert the 5 Base85 characters back into a 32-bit integer
        num = 0
        try:
            for char in padded_chunk:
                num = num * 85 + DECODE_MAP[char]
        except KeyError:
            raise ValueError(f"Invalid Base85 character in chunk starting at byte {i}")

        try:
            decoded_bytes = num.to_bytes(4, byteorder='big')
        except OverflowError:
            raise ValueError(f"Base85 overflow in chunk starting at byte {i}")

        # Remove the padding bytes that were added during encoding
        num_bytes_to_keep = len(chunk) - 1
        result.extend(decoded_bytes[:num_bytes_to_keep])

    return bytes(result)