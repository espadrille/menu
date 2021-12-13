# Import des modules
import collections
import json
import mimetypes

from module_globals import *
import _Command_class
from _MenuItem_class import MenuItem


# Definition de la classe Menu

class Menu:
    def __init__(self, menu_file=""):
        self.__id = ""
        self.__title = ""
        self.__description = ""
        self.__format = ""
        self.__items = {}

        self.__menu = []
        self.__json_string = ""
        self.__menu_file = ""
        self.__menu_file_mime_type = ""

        self.__last_return_code = 0
        self.__key_length_max = 0
        self.__int_sortable = True
        if menu_file != "":
            self.load_file(menu_file)

    # Accesseurs
    def get_menu_file(self):
        return self.__menu_file

    # Mutateurs

    # Methodes privees
    def __update(self):
        if "id" in self.__menu["menu"]:
            self.__id = self.__menu["menu"]["id"]
        if "title" in self.__menu["menu"]:
            self.__title = self.__menu["menu"]["title"]
        if "description" in self.__menu["menu"]:
            self.__description = self.__menu["menu"]["description"]
        if "format" in self.__menu["menu"]:
            self.__format = self.__menu["menu"]["format"]
        if "items" in self.__menu["menu"]:
            for my_item in self.__menu["menu"]["items"]:
                new_item = MenuItem()
                new_item.set_key(my_item["id"])
                new_item.set_text(my_item["text"])
                if "format" in my_item:
                    new_item.set_format(my_item["format"])
                self.add_item(new_item)

    # Methodes publiques
    def add_item(self, item):
        self.__items[item.get_key()] = item
        if item.get_key_length() > self.__key_length_max:
            self.__key_length_max = item.get_key_length()

        # Verifier si la cle est un entier
        if type(item.get_key()) is not int:
            self.__int_sortable = False

        # Ajustement des largeurs de colonnes pour la cle sur les autres items
        for my_key, my_item in self.__items.items():
            if not self.__int_sortable:
                my_item.set_key(str(my_key))
            my_item.set_key_length(self.__key_length_max)

    def load_file(self, menu_file):
        self.__menu_file = menu_file
        self.__menu_file_mime_type = mimetypes.MimeTypes().guess_type(self.__menu_file)[0]
        if self.__menu_file_mime_type == "application/json":
            fp = open(self.__menu_file, "r")
            self.load_json(fp.read())
            fp.close()
        else:
            print_fmt("Format non pris en charge : " + str(self.__menu_file_mime_type), "ERROR")
        self.__update()

    def load_json(self, json_string):
        try:
            self.__menu = json.loads(json_string)
            self.__json_string = json_string
        except Exception as e:
            print_fmt("Format json incorrect dans le fichier [" + self.__menu_file + "]", "ERROR")
            print_fmt(e.__str__(), "ERROR")

    def print(self, ordered=False):
        print_fmt(self.__title, self.__format)
        if ordered:
            if self.__int_sortable:
                for my_key, my_item in collections.OrderedDict(
                        sorted(self.__items.items(), key=lambda t: t[0])).items():
                    my_item.print()
            else:
                for my_key, my_item in collections.OrderedDict(
                        sorted(self.__items.items(), key=lambda t: str(t[0]))).items():
                    my_item.print()
        else:
            for my_key, my_item in self.__items.items():
                my_item.print()
        return self.__last_return_code

    def debug(self):
        print("                === Debug infos ===")
        print("Fichier de configuration : " + self.__menu_file)
        print("id                       : " + self.__id)


#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    my_menu = Menu()
    my_menu.load_file("../json/menu.json")

    my_menu.print(ordered=True)

    my_menu.debug()
