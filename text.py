import logging
import sys

logging.getLogger().setLevel(logging.INFO)

class Text:
    """
    Class for workings text with bytes
    """
    def __init__(self)->None:
        """
        Constructor
        """
        self.__text = None
    
    def get_text(self)->bytes:
        """
        Getter
        """
        return self.__text
    
    def set_text(self, text:bytes)->None:
        """
            setter
        """
        self.__text = text

    def text_serialization(self, file_name:str)->None:
        """
        Funs that writes text in file
        """
        try:
            with open(file_name, "wb") as file:
                file.write(self.__text)
            logging.info("Text is saved")
        except OSError as error:
            logging.warning("Text is not saved")
            sys.exit(error)

    def text_deserialization(self, file_name:str)->None:
        """
        Func that reads text from file
        """
        try:
            with open(file_name, "rb") as file:
                self.__text = file.read()
            logging.info("Text is loaded from file")
        except OSError as error:
            logging.warning("Text is not loaded from file")
            sys.exit(error)
        
    txt = property(get_text, set_text)