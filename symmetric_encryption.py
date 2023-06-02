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

    def __sym_key(self) -> bytes:
        """
        Symmetric encryption key decryption function
        Returns the decrypted symmetric key
        """
        try:
            with open(self.settings['private_key'], "rb") as f:
                private_key = serialization.load_pem_private_key(
                    f.read(), password=None)
        except OSError as err:
            logging.warning(
                f"{err} error when writing to a file {self.settings['private_key']}")
        try:
            with open(self.settings['symmetric_key'], "rb") as f:
                encrypted_symmetric_key = f.read()
            symmetric_key = private_key.decrypt(encrypted_symmetric_key, padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        except OSError as err:
            logging.warning(
                f"{err} error when writing to a file {self.settings['symmetric_key']}")
        return symmetric_key