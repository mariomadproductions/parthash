#!/usr/bin/env python3
import argparse
from zlib import crc32
import sys
from pathlib import Path

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', metavar='INPUT')
    parser.add_argument('--part-size', type=int,
                        default=16)
    return parser.parse_args()

def get_file_part_hashes(filename,partsize):
    with open(filename, mode='rb') as file:
        while True:
            crc32_result = 0
            data = file.read(partsize)
            if not data:
                break
            else:
                crc32_result = crc32(data, crc32_result)
                yield crc32_result

def main():
    args = get_args()
    input_file_path = Path(args.input_file)
    input_file_size = input_file_path.stat().st_size
    part_size = args.part_size
    
    sys.stdout.buffer.write(input_file_size.to_bytes(8, byteorder='big'))
    sys.stdout.buffer.write(part_size.to_bytes(8, byteorder='big'))
    
    for crc32_result in get_file_part_hashes(input_file_path, part_size):
        sys.stdout.buffer.write(crc32_result.to_bytes(4, byteorder='big'))

if __name__ == '__main__':
    main()
