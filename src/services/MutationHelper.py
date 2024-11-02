import random
from pathlib import Path

def flip(original_input, max_variants):
    """
    Returns up to max_variants of bit-flipped input.
    For each variant, ~6% of total bytes are altered.
    """
    input_len = len(original_input)
    max_flips = input_len // 16

    for _ in range(max_variants):
        var = bytearray(original_input)
        for f in range(max_flips):
            i = random.randrange(input_len)
            var[i] = original_input[i] ^ random.randrange(255)
        yield var

def yield_bad_string():
    """
    Yields a single string from a database of known bad strings.
    """
    db = Path('/src/input_handlers/bad-strings.txt')
    store = []
    
    with open(db, 'r') as bad_strings:
        for bad_string in bad_strings:
            if not bad_string.startswith(('#', '\n')):
                store.append(bad_string[:-1].encode())

    i = 0
    while True:
        yield store[i]
        i = (i + 1) % len(store)