#!/usr/bin/python3

"""A utility for guessing DEC-encoded passwords in HackNet.

The input is a number from the header of the file, specifically the number
that appears before the last "::". This number will be the same as the one
two positions prior. The output will be a number of potential passwords.
Any of the passwords should work; the underscores can be replaced by any
character (or left as underscores). The trailing underscore can also be
removed if you like, if you are trying to guess the original password.

If the empty string ("") shows as valid, it means you don't need to provide
a password to the in-game program.
"""

import argparse
import array
import random
import struct
import sys

def do_one_hash(hash_val, int_val):
    """Computes the primitive hash operation."""
    hash_val = ((hash_val << 5) + hash_val + (hash_val >> 27)) & 0xFFFFFFFF
    hash_val ^= int_val
    if hash_val >= 0x80000000:
        hash_val -= 0x100000000
    return hash_val

def get_hash_code(string_in):
    """Implements C#'s String.GetHashCode() algorithm.

    There are actually multiple implementations, but this is the one used in
    HackNet. This function is too slow to be used directly, but is useful
    for testing/validation.
    """
    byt = string_in.encode('utf-16-le') + b'\0\0'
    b_len = len(byt)
    if (b_len & 2) == 2:
        b_len -= 2
    ints_list = [struct.unpack_from('<I', byt, x)[0] for x in range(0, b_len, 4)]
    return get_hash_code_internal(ints_list, len(ints_list))

def get_hash_code_internal(ints_list, ints_len):
    """Actual implementation of the hashing algorithm.

    This takes a list of integers and a length, so that the list doesn't
    need to be resized to change lengths.
    """
    hash1 = 352654597 #(5381<<16) + 5381
    hash2 = hash1

    off = 0
    while off <= ints_len - 2:
        hash1 = do_one_hash(hash1, ints_list[off])
        hash2 = do_one_hash(hash2, ints_list[off+1])
        off += 2

    if off <= ints_len - 1:
        hash1 = do_one_hash(hash1, ints_list[off])
    return (hash1 + (hash2 * 1566083941)) & 0xFFFFFFFF

def decode_list(ints_list, ints_len):
    """Decode the list-of-integers format back to a string."""
    return str(array.array('L', ints_list[:ints_len]), 'utf-16-le')

def display_hash_code(string_in):
    """For debugging/validation."""
    code = get_hash_code(string_in)
    signed = code
    if signed >= 0x80000000:
        signed = signed - 0x100000000
    print('The hash code for "%s" is: 0x%08X, %d' % (string_in, code, signed))

def scramble(string_in):
    """Permute a string, so that we try solutions in different orders."""
    return [ord(x) + (ord('_') << 16) for x in random.sample(string_in, len(string_in))]

def lowercase():
    """The source alphabet of our solutions: a-z."""
    return ''.join(chr(x) for x in range(ord('a'), ord('z') + 1))

def try_all(ints_list, source, pos, ints_len, target):
    """Recursively try all 'ints_len' solutions using 'source' as the alphabet"""
    if pos == ints_len:
        if (get_hash_code_internal(ints_list, ints_len) & 0xFFFF) == target:
            print('"%s" is valid' % decode_list(ints_list, ints_len))
        return
    for code in source:
        ints_list[pos] = code
        try_all(ints_list, source, pos + 1, ints_len, target)

def main():
    """main(). Thanks, pylint."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('value', type=int,
        help="""The encoded integer value that appears immediately before the last
        instance of "::" in the file header""")
    args = parser.parse_args()
    target = args.value - (ord('D') * 1822 + (65535 >> 1))
    if target < 0 or target >= 65536:
        print('Calculated target value of %d is out of range; no solution possible!'
            % target)
        sys.exit(1)

    source = scramble(lowercase())
    lst = []
    while len(lst) <= 4:
        try_all(lst, source, 0, len(lst), target)
        lst.append(0)

if __name__ == '__main__':
    main()
