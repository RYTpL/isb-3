import logging
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from encryption import Encryption

class SymmetricEncryption(Encryption):
    """Class for symmetric encryption."""

    def __init__(self, size: int, way: str) -> None:
        super().__init__(size, way)
        self.settings['symmetric_key'] = os.path.join(self.way, 'symmetric_key.txt')

    def encrypt(self) -> None:
        pass

    def decrypt(self) -> None:
        pass