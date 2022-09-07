#!/usr/bin/env python3
import argparse
import hashlib

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', metavar='INPUT')
    parser.add_argument('--part-size', type=int,
                        default=16)
    return parser.parse_args()

def get_file_part_hashes(filename,partsize):
    with open(filename, mode='rb') as file:
        while True:
            sha256_hash_object = hashlib.sha256()
            start_offset = file.tell()
            data = file.read(partsize)
            end_offset = file.tell()
            amount_read = end_offset - start_offset
            if not data:
                break
            else:
                sha256_hash_object.update(data)
                sha256_hash_object_str = sha256_hash_object.hexdigest()
                yield start_offset, amount_read, sha256_hash_object_str

def main():
    args = get_args()
    input_file = args.input_file
    part_size = args.part_size
    for start_offset, amount_read, hash_str in get_file_part_hashes(input_file,
                                                              part_size):
        print(f'{start_offset:x} {amount_read:x} {hash_str}')

if __name__ == '__main__':
    main()
