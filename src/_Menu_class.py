# Import des modules
from module_globals import *
import _Command_class
from _MenuItem_class import MenuItem


# Definition de la classe Menu

class Menu:
    def __init__(self, menu_file=""):
        self.__menu_file = ""
        self.__items = {}
        self.__last_return_code = 0
        self.__key_length_max = 0
        if menu_file != "":
            self.load_file(menu_file)

    # Accesseurs
    def get_menu_file(self):
        return self.__menu_file

    # Mutateurs
    def add_item(self, item):
        self.__items[item.get_key()] = item
        if item.get_key_length() > self.__key_length_max:
            self.__key_length_max = item.get_key_length()

        # Ajustement des largeurs de colonnes pour la cle sur les autres items
        for my_key, my_item in self.__items.items():
            my_item.set_key_length(self.__key_length_max)

    def load_file(self, menu_file):
        self.__menu_file = menu_file

    # Methodes privees

    # Methodes publiques
    def print(self):
        print_fmt("Menu", "TITRE1")
        if self.__menu_file != "":
            print_fmt("Fichier de configuration : " + self.__menu_file)
        for my_key, my_item in self.__items.items():
            my_item.print()
        return self.__last_return_code


#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    my_menu = Menu()
    my_menu.load_file("../toto")
    my_menu.add_item(MenuItem("1", "Premier choix"))
    my_menu.add_item(MenuItem("200", "Deux centième choix"))
    my_menu.add_item(MenuItem("3", "Troisième choix"))

    my_menu.print()
