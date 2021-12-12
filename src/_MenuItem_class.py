# Import des modules
from module_globals import *
import _Command_class


# Definition de la classe MenuItem

class MenuItem:
    def __init__(self, key="", text="", key_length=0):
        self.__key = ""
        self.__text = ""
        self.__key_length = len(key)
        self.set_key(key)
        self.set_key_length(len(key))
        self.set_text(text)

    # Accesseurs
    def get_key(self):
        return self.__key

    def get_text(self):
        return self.__text

    def get_key_length(self):
        return self.__key_length

    # Mutateurs
    def set_key(self, key):
        self.__key = key
        self.__key_length = len(key)

    def set_text(self, text):
        self.__text = text

    def set_key_length(self, length):
        self.__key_length = length

    # Methodes privees

    # Methodes publiques
    def print(self):
        print_fmt(self.__key.rjust(self.__key_length) + " : " + self.__text + " l=" + str(self.__key_length), "MENU", 2)

#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    my_item = MenuItem("1", "Premier choix", 5)
    my_item.set_key_length(10)
    my_item.print()
