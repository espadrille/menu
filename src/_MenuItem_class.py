# Import des modules
from module_globals import *
import _Command_class


# Definition de la classe MenuItem

class MenuItem:
    def __init__(self, key="", text="", text_format="MENU"):

        self.__key = ""
        self.__text = ""
        self.__format = ""

        self.__key_length = len(str(key))
        self.set_key(key)
        self.set_text(text)
        self.set_format(text_format)
        self.set_key_length(len(str(key)))

    # Accesseurs
    def get_key(self):
        return self.__key

    def get_text(self):
        return self.__text

    def get_format(self):
        return self.__format

    def get_key_length(self):
        return self.__key_length

    # Mutateurs
    def set_key(self, key):
        self.__key = key
        self.__key_length = len(str(key))

    def set_text(self, text):
        self.__text = text

    def set_format(self, text_format):
        self.__format = text_format

    def set_key_length(self, length):
        self.__key_length = length

    # Methodes privees

    # Methodes publiques
    def print(self):
        if type(self.__key) is int:
            print_fmt(str(self.__key).rjust(self.__key_length) + " : " + self.__text, self.__format, 2)
        else:
            print_fmt(str(self.__key).ljust(self.__key_length) + " : " + self.__text, self.__format, 2)


#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    my_item = MenuItem("1", "Premier choix", 5)
    my_item.set_key_length(10)
    my_item.print()
