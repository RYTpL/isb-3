import re
import sys
import argparse
from workspace import Encryption as en
import logging 

logging.basicConfig(level=logging.INFO) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A program for 3DES encryption and decryption')
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
        logging.info('Keys generated and saved in %s', way)


    if args.encrypt:
        key.encryption(args.encrypt)
        logging.info('Text encrypted and saved in %s.enc', args.encrypt)

    if args.decrypt:
        way = key.decryption(args.decrypt)
        logging.info('Text decrypted from %s', args.decrypt)
        print('Text decrypted:')
        print(way)
