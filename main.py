import re
import sys
from code import Encryption as en


class Terminal:
    def __init__(self):
        """
        initialization

        """
        self.size = None
        self.key = None

    def run(self):
        """
        this function gives a choice of action

        """
        while True:
            print("Select an action:")
            print("1. Set the key size")
            print("2. Generate keys")
            print("3. Encrypt Text")
            print("4. Decrypt the text")
            print("5. Exit")

            choice = input()

            if choice == "1":
                self.set_key_size()
            elif choice == "2":
                self.generate_keys()
            elif choice == "3":
                self.encrypt_text()
            elif choice == "4":
                self.decrypt_text()
            elif choice == "5":
                sys.exit()
            else:
                print("Wrong choice")

    def set_key_size(self):
        """
        this function allows you to select the key size

        """
        print("Choose the key size")
        print("1. 64 bit")
        print("2. 128 bit")
        print("3. 192 bit")

        choice = input()

        if choice == "1":
            self.size = 64
        elif choice == "2":
            self.size = 128
        elif choice == "3":
            self.size = 192
        else:
            print("Wrong choice")

    def generate_keys(self):
        """
        in this function keys are generated

        """
        if not self.size:
            print("The key size is not set")
            return

        way = input("Enter the path to save the keys: ")
        self.key = en(self.size, way)
        self.key.generation_key()
        print("Keys generated")

    def encrypt_text(self):
        """
        in this function, the text is encrypted

        """
        if not self.key:
            print("Keys are not generated")
            return

        way = input("Enter the path to the file to encrypt: ")
        self.key.encryption(way)
        print("The text is encrypted")

    def decrypt_text(self):
        """
        in this function, the text is decrypted

        """
        if not self.key:
            print("Keys not generated")
            return

        way = self.key.decryption()
        print("The text is decoded:")
        print(way)


if __name__ == "__main__":
    terminal = Terminal()
    terminal.run()
