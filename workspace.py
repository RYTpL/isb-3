import logging
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from encryption import Encryption
from symmetric_encryption import SymmetricEncryption
from asymmetric_encryption import AsymmetricEncryption


class Encryption(abc.ABC):
    """Abstract base class for encryption classes."""

    def __init__(self, size: int, way: str) -> None:
        """
        initialization function
        """
        self.size = int(size/8)
        self.way = way
        self.settings = {
            'encrypted_file': os.path.join(self.way, 'encrypted_file.txt'),
            'decrypted_file': os.path.join(self.way, 'decrypted_file.txt'),
            'iv_path': os.path.join(self.way, 'iv_path.txt')
        }

    @abc.abstractmethod
    def encrypt(self) -> None:
        """Encrypt data."""
        pass

    @abc.abstractmethod
    def decrypt(self) -> None:
        """Decrypt data."""
        pass
