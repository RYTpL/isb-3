import re
import sys
import argparse
from coding import Encryption as en


parser = argparse.ArgumentParser(description='A program for 3DES encryption and decryption')

parser.add_argument('-s', '--size', type=int, choices=[64, 128, 192], help='Choose the key size in bits')
parser.add_argument('-g', '--generate', action='store_true', help='Generate keys and save them in a directory')
parser.add_argument('-e', '--encrypt', type=str, help='Encrypt a text file')
parser.add_argument('-d', '--decrypt', type=str, help='Decrypt a text file')


args = parser.parse_args()

if args.size:
    
    key = en(args.size)
else:
    
    key = en()


if args.generate:

    way = input('Enter the directory to save the keys: ')

    key.generation_key(way)
    print('Keys generated and saved')


if args.encrypt:
    key.encryption(args.encrypt)
    print('Text encrypted and saved')

if args.decrypt:
    way = key.decryption(args.decrypt)
    print('Text decrypted:')
    print(way)