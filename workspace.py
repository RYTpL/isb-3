import argparse
import json
import logging
import sys

from asymmetric_encryption import Asymmetric
from symmetric_encryption import Symmetric
from text import Text

logging.getLogger().setLevel(logging.INFO)

def load_settings(json_file_name:str)->dict:
    """
    Func that loads settings from json file
    """
    try:
        with open(json_file_name, "r") as file:
            settings = json.load(file)
        return settings
    except OSError as error:
        logging.warning("Settings are not loaded from json")
        sys.exit(error)

def save_settings(json_file_name:str, settings:dict)->None:
    """
    Func that save settings from json file
    """
    try:
        with open(json_file_name, "w") as file:
            json.dump(settings, file)
    except OSError as error:
        logging.warning("Settings are not saved to json")
        sys.exit(error)

def generation_action(symmetric:Symmetric, asymmetric:Asymmetric, settings:dict, key_len:int)->None:
    """
    Func that executes keys generation
    """
    
    symmetric.generate_symmeric_key(settings, key_len)
    asymmetric.keys_generation()
    symmetric.sym = asymmetric.encrypt(symmetric.sym)
    asymmetric.key_serialization(settings["private_key"], settings["public_Key"])
    symmetric.key_serialization(settings["symmetric_Key"])
    logging.info("Generation is done")

def encryption_action(text:Text, symmetric:Symmetric, asymmetric:Asymmetric,settings:dict)->dict:
    """
    Func that executes keys generation
    """
    asymmetric.secret_key_deserialization(settings["private_key"])
    symmetric.key_deserialization(settings["symmetric_key"])
    symmetric.sym = asymmetric.decrypt(symmetric.sym)
    text.text_deserialization(settings["initial_file"])
    text.txt, settings = symmetric.encrypt(text.txt, settings)
    text.text_serialization(settings["encrypted_file"])
    logging.info("Encryption is done")
    return settings

def decryption_action(text:Text, symmetric:Symmetric, asymmetric:Asymmetric,settings:dict)->None:
    """
    Func that executes keys generation
    """
    print(f"settings: {settings}")
    asymmetric.secret_key_deserialization(settings["private_key"])
    symmetric.key_deserialization(settings["symmetric_Key"])
    symmetric.sym = asymmetric.decrypt(symmetric.sym)
    text.text_deserialization(settings["encrypted_file"])
    text.txt = symmetric.decrypt(text.txt, settings)
    text.text_serialization(settings["decrypted_file"])
    logging.info("Decryption is done")


def menu()->None:
    """
    Func that operates with cmd user's commands 
    and execute keys ganeration, text encryption and decryption
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    parser.add_argument("len", type = int, help="Key length for symmetric encryption")
    parser.add_argument("path", type = str, help="Path to the json file with the settings")
    group.add_argument("-gen", "--generation",  help="Starts the key generation")
    group.add_argument("-enc", "--encryption",  help="Starts the encryption")
    group.add_argument("-dec", "--decryption",  help="Starts the decryption")
    args = parser.parse_args()
    settings = load_settings(args.path)

    if args.generation is not None:
        symmetric = Symmetric()
        asymmetric = Asymmetric()
        generation_action(symmetric, asymmetric, settings, args.len)
        settings["keyLen"] = int(args.len)
        save_settings(args.path, settings)

    elif args.encryption is not None:
        text = Text()
        symmetric = Symmetric()
        asymmetric = Asymmetric()
        settings = encryption_action(text, symmetric, asymmetric, settings)
    elif args.decryption:
        text = Text()
        symmetric = Symmetric()
        asymmetric = Asymmetric() 
        decryption_action(text, symmetric, asymmetric, settings)