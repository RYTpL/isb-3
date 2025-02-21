import logging
import sys
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

logging.getLogger().setLevel(logging.INFO)
class Symmetric:
    """
    Class for working with symmetric alg
    """
    def __init__(self)->None:
        self.__key = None
    
    def generate_symmeric_key(self,json_settings: dict, key_lenght: int = 128)->None:
        """
        Func that generates key of symmetric algorithm
        """
        if(key_lenght in [64,128,192]):
            self.__key = os.urandom(int(key_lenght/8))
            logging.info(f"Symmeric key is generated, lenght is {key_lenght}")
        else:
            logging.warning("Symmeric key is not generated. key_lenght is not correct")
            sys.exit("Try again")
    @property
    def sym(self):
        return self.__key
    @sym.setter
    def key(self, value):
        self.__key = value
        

    def key_deserialization(self, file_name: str)->None:
        """
            Func that loads key from file
        """
        try:
            with open(file_name, "rb") as file:
                self.__key = file.read()
            logging.info("Symmeric key is loaded")
        except OSError as error:
            logging.warning("Symmeric key is not loaded")
            sys.exit(error)

    def key_serialization(self, file_name:str)->None:
        """
            Func that saves key to file
        """
        try:
            with open(file_name, "wb") as file:
                file.write(self.__key)
            logging.info("Symmeric key is saved")
        except OSError as error:
            logging.warning("Symmeric key is not saved")
            sys.exit(error)

    def encrypt(self, text: bytes, json_settings: dict, )->bytes:
        """
            Funs that encrypts text
        """
        padder = padding.ANSIX923(json_settings["keyLen"]).padder()
        padded_text = padder.update(text)+padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(self.__key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        try:
            with open("./files/iv_path.txt", "wb") as file:
                file.write(iv)
        except OSError as error:
            logging.warning("iv is not saved")
            sys.exit(error)
        logging.info("Text is encrypted with symmetric algorithm")
        return c_text, json_settings

    def decrypt(self, text:bytes, json_settings: dict)->bytes:
        """
            Func that decrypt text
        """
        try:
            with open("./files/iv_path.txt", "rb") as file:
                iv = file.read()
        except OSError as error:
            logging.warning("iv is not saved")
            sys.exit(error)       
        cipher = Cipher(algorithms.TripleDES(self.__key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(text) + decryptor.finalize()
        unpadder = padding.ANSIX923(json_settings["keyLen"]).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        logging.info("Text is decrypted with symmetric algorithm")
        return unpadded_dc_text