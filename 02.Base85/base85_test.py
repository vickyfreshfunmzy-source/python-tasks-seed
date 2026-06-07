"""
Unit tests for 02.Base85
"""

import pytest
import base85ed


def test_shorts_encode():
    """
    Test trivial short encodes
    """
    assert base85ed.encode(b"1") == b"F#"
    assert base85ed.encode(b"12") == b"F){"
    assert base85ed.encode(b"123") == b"F)}j"
    assert base85ed.encode(b"1234") == b"F)}kW"


def test_shorts_decode():
    """
    Test trivial short decodes
    """
    assert base85ed.decode(b"F#") == b"1"
    assert base85ed.decode(b"F){") == b"12"
    assert base85ed.decode(b"F)}j") == b"123"
    assert base85ed.decode(b"F)}kW") == b"1234"


def test_empty_data():
    """
    Test edge case with empty bytes input
    """
    assert base85ed.encode(b"") == b""
    assert base85ed.decode(b"") == b""


def test_roundtrip_text():
    """
    Test that decoding an encoded string returns the exact original text
    """
    original = b"Hello, World! This is a longer string."
    encoded = base85ed.encode(original)
    decoded = base85ed.decode(encoded)
    assert decoded == original


def test_roundtrip_binary():
    """
    Test roundtrip with pure binary data (all possible byte values)
    """
    # Create a bytes object containing values from 0 to 255
    original = bytes(range(256))
    encoded = base85ed.encode(original)
    decoded = base85ed.decode(encoded)
    assert decoded == original


def test_multiple_chunks():
    """
    Test data that spans across multiple 4-byte chunks
    """
    # 5 bytes : 1 full chunk (4 bytes) + 1 partial chunk (1 byte)
    original = b"12345"
    assert base85ed.decode(base85ed.encode(original)) == original

    # 8 bytes : exactly 2 full chunks
    original = b"12345678"
    assert base85ed.decode(base85ed.encode(original)) == original


def test_decode_invalid_character():
    """
    Test that decoding an invalid Base85 character raises a ValueError
    """
    # ' ' (space) is not in the ALPHABET
    with pytest.raises(ValueError, match="Invalid Base85 character"):
        base85ed.decode(b"F# ")


def test_decode_overflow():
    """
    Test that decoding a sequence that exceeds 32 bits raises a ValueError
    """
    # '~~~~~' evaluates to 85^5 - 1, which is strictly greater than 2^32 - 1
    with pytest.raises(ValueError, match="Base85 overflow"):
        base85ed.decode(b"~~~~~")

    # A 4-character sequence should represent at most 3 bytes (max 0xFFFFFF).
    # '~~~~' padded becomes '~~~~~', which also overflows 32 bits, correctly rejecting it.
    with pytest.raises(ValueError, match="Base85 overflow"):
        base85ed.decode(b"~~~~")


def test_partial_chunks_high_bytes():
    """
    Test partial chunks with maximum byte values to ensure padding doesn't corrupt data.
    This specifically stress-tests the fix made in the decode function.
    """
    # 1 byte (max value)
    original = b"\xff"
    assert base85ed.decode(base85ed.encode(original)) == original

    # 2 bytes (max value)
    original = b"\xff\xff"
    assert base85ed.decode(base85ed.encode(original)) == original

    # 3 bytes (max value)
    original = b"\xff\xff\xff"
    assert base85ed.decode(base85ed.encode(original)) == original


def test_all_modulo_lengths_roundtrip():
    """
    Test roundtrip for lengths 0 through 12 to exhaustively cover all modulo 4 boundaries.
    """
    for length in range(13):
        original = bytes([i % 256 for i in range(length)])
        encoded = base85ed.encode(original)
        decoded = base85ed.decode(encoded)
        assert decoded == original, f"Failed at length {length}"


def test_max_32bit_value_roundtrip():
    """
    Test the absolute maximum 32-bit value (4 bytes of 0xFF)
    to ensure no overflow occurs during the encode/decode cycle.
    """
    original = b"\xff\xff\xff\xff"
    encoded = base85ed.encode(original)
    decoded = base85ed.decode(encoded)
    assert decoded == original
    # Optional: verify the encoded output is exactly 5 characters
    assert len(encoded) == 5


def test_large_payload_roundtrip():
    """
    Test roundtrip with a large payload (e.g., 10,000 bytes)
    to ensure chunking logic holds up at scale without state leakage.
    """
    # Create a predictable but large patterned payload
    original = bytes([i % 256 for i in range(10000)])
    encoded = base85ed.encode(original)
    decoded = base85ed.decode(encoded)
    assert decoded == original
    # Base85 expands data by ~25% (5/4)
    assert len(encoded) == 12500


def test_decode_rejects_whitespace():
    """
    Test that common Base85 formatting characters (newlines, carriage returns)
    are correctly rejected, as this is a strict decoder.
    """
    with pytest.raises(ValueError, match="Invalid Base85 character"):
        base85ed.decode(b"F}\n")

    with pytest.raises(ValueError, match="Invalid Base85 character"):
        base85ed.decode(b"F}\r")

    with pytest.raises(ValueError, match="Invalid Base85 character"):
        base85ed.decode(b"F} ")


def test_encode_type_enforcement():
    """
    Test that @beartype correctly rejects string inputs for encode.
    """
    with pytest.raises(Exception):
        base85ed.encode("not a bytes object")  # type: ignore


def test_decode_type_enforcement():
    """
    Test that @beartype correctly rejects string inputs for decode.
    """
    with pytest.raises(Exception):
        base85ed.decode("not a bytes object")  # type: ignore