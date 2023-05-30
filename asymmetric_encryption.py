import logging
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from encryption import Encryption

class AsymmetricEncryption(Encryption):
    """Class for asymmetric encryption."""

    def __init__(self, size: int, way: str) -> None:
        super().__init__(size, way)
        self.settings['public_key'] = os.path.join(self.way, 'public_key.txt')
        self.settings['private_key'] = os.path.join(self.way, 'private_key.txt')

    def encrypt(self) -> None:
        pass

    def decrypt(self) -> None:
        pass


    def generation_key(self) -> None:
        """
        Key generation function
        """
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()
        try:
            with open(self.settings['public_key'], 'wb') as public_out:
                public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except OSError as err:
            logging.warning(
                f"{err} error when writing to a file {self.settings['public_key']}")
        else:
            logging.info("The public key is recorded")
        try:
            with open(self.settings['private_key'], 'wb') as private_out:
                private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                            encryption_algorithm=serialization.NoEncryption()))
        except OSError as err:
            logging.warning(
                f"{err} error when writing to a file {self.settings['private_key']}")
        else:
            logging.info("The private key is recorded")
        symmetric_key = os.urandom(self.size)
        ciphertext = public_key.encrypt(symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        try:
            with open(self.settings['symmetric_key'], "wb") as f:
                f.write(ciphertext)
        except OSError as err:
            logging.warning(
                f"{err} error when writing to a file {self.settings['symmetric_key']}")
        else:
            logging.info("The symmetric key is written")


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
    

    def encryption(self, way: str) -> None:
        """
        The function of text encryption by the 3DES algorithm
        """
        way_e = way
        symmetric_key = self.__sym_key()
        try:
            with open(way_e, 'r', encoding='utf-8') as f:
                text = f.read()
        except OSError as err:
            logging.warning(f"{err} error when writing to a file {way_e}")
        else:
            logging.info("The text has been read")
        padder = sym_padding.ANSIX923(128).padder()
        padded_text = padder.update(bytes(text, 'utf-8')) + padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        try:
            with open(self.settings['iv_path'], 'wb') as key_file:
                key_file.write(iv)
        except OSError as err:
            logging.warning(
                f"{err} error when writing to a file {self.settings['iv_path']}")
        try:
            with open(self.settings['encrypted_file'], 'wb') as f_text:
                f_text.write(c_text)
        except OSError as err:
            logging.warning(
                f"{err} error when writing to a file {self.settings['encrypted_file']}")
        else:
            logging.info("The text is encrypted")
        

    def decryption(self) -> str:
        """
       3DES algorithm text decryption function
        Returns the path to the decrypted file
        """
        symmetric_key = self.__sym_key()
        try:
            with open(self.settings['encrypted_file'], 'rb') as f:
                en_text = f.read()
        except OSError as err:
            logging.warning(
                f"{err} error when reading from a file {self.settings['encrypted_file']}")
        try:
            with open(self.settings['iv_path'], "rb") as f:
                iv = f.read()
        except OSError as err:
            logging.warning(
                f"{err} error when reading from a file {self.settings['iv_path']}")
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(en_text) + decryptor.finalize()
        unpadder = sym_padding.ANSIX923(128).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        try:
            with open(self.settings['decrypted_file'], 'wb') as f:
                f.write(unpadded_dc_text)
        except OSError as err:
            logging.warning(
                f"{err} error writing to a file {self.settings['decrypted_file']}")
        else:
            logging.info("The text is decoded")
        return self.settings['decrypted_file']