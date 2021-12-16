# Import des modules
import collections
import mimetypes
import grp

from module_globals import *
from _MenuItem_class import MenuItem


# Definition de la classe Menu

class Menu:
    def __init__(self, menu_file=""):
        self.__id = ""
        self.__title = ""
        self.__description = ""
        self.__format = ""
        self.__items = dict()         # Collection des items originaux (lus dans le json)
        self.__s_items = dict()       # Collection des items avec la clé convertie en chaîne

        self.__menu = dict()
        self.__menu_file = ""
        self.__menu_file_mime_type = ""

        self.__ordered = False
        self.__last_choice = ""
        self.__last_return_code = 0
        self.__key_length_max = 0
        self.__int_sortable = True
        if menu_file != "":
            self.load_file(menu_file)

    # Accesseurs
    def get_menu_file(self):
        return self.__menu_file

    # Mutateurs
    def sort(self):
        self.__ordered = True

    # Méthodes privées
    def __update(self):
        self.__items.clear()
        if "menu" in self.__menu:
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
                    authorized = True
                    if "security" in my_item:
                        authorized = False
                        if "authorized_groups" in my_item["security"]:
                            for authorized_group in my_item["security"]["authorized_groups"]:
                                if authorized_group in [grp.getgrgid(g).gr_name for g in os.getgroups()]:
                                    authorized = True
                        if "authorized_users" in my_item["security"]:
                            if os.getlogin() in my_item["security"]["authorized_users"]:
                                authorized = True
                    if authorized:
                        new_item = MenuItem()
                        new_item.set_key(my_item["id"])
                        new_item.set_text(my_item["text"])
                        if "format" in my_item:
                            new_item.set_format(my_item["format"])
                        if "commands" in my_item:
                            for my_command in my_item["commands"]:
                                new_item.add_command(my_command)
                        self.add_item(new_item)

    # Méthodes publiques
    def add_item(self, item):
        self.__items[item.get_key()] = item
        self.__s_items[str(item.get_key())] = item
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
        except Exception as e:
            print_fmt("Format json incorrect dans le fichier [" + self.__menu_file + "]", "ERROR")
            print_fmt(e.__str__(), "ERROR")

    def print_title(self):
        print_fmt(self.__title, self.__format)

    def print_description(self):
        for my_line in self.__description:
            print_fmt(my_line, "MENU", 2)
        print_fmt("", "MENU")

    def print_items(self):
        if self.__ordered:
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

    def read_choice(self):
        # Transformer les clés en format chaîne avant rechercher la réponse utilisateur dans la liste
        str_keys = [str(key) for key in self.__items.keys()]
        if self.__ordered:
            str_keys.sort()
        self.__last_choice = read_fmt("Votre choix parmi " + str(str_keys))
        while not (str(self.__last_choice) in str_keys or str(self.__last_choice) == ""):
            print_fmt("Choisissez parmi les valeurs proposées " + str(str_keys), "ERROR")
            self.__last_choice = read_fmt("Votre choix parmi " + str(str_keys))

    def print_menu(self):
        self.print_title()
        self.print_description()
        self.print_items()

    def execute(self):
        self.print_menu()
        self.read_choice()
        if self.__last_choice == "":
            print_fmt("=> Abandon...", "MENU")
        else:
            self.__last_return_code = self.__s_items[self.__last_choice].execute_commands()
        return self.__last_return_code

    def debug(self):
        print("")
        print("            === Debug infos ===")
        print("menu_file            : " + self.__menu_file)
        print("menu_file_mime_type  : " + self.__menu_file_mime_type)
        print("id                   : " + self.__id)
        print("nb_items             : " + str(len(self.__items)))
        print("last_choice          : " + self.__last_choice)
        print("sorted               : " + str(self.__ordered))
        print("last_return_code     : " + str(self.__last_return_code))
        print("")


#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    my_menu = Menu()
    my_menu.load_file("../json/menu.json")

    my_menu.sort()
    my_menu.execute()

    my_menu.debug()
