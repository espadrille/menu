# Import des modules
import collections
import grp
import mimetypes
import subprocess
import yaml

from module_globals import *
from _MenuItem_class import MenuItem
from pathlib import Path

mimetypes.add_type("application/x-yaml", ".yaml")
mimetypes.add_type("application/x-yaml", ".yml")


# Definition de la classe Menu

class Menu(object):
    def __init__(self, menu_file="", sort_items=False):
        self.__id = ""  # Identifiant du menu
        self.__title = ""  # Titre du menu
        self.__description = ""  # Description du menu
        self.__format = ""  # Format d'affichage du menu
        self.__items = dict()  # Collection des items originaux (lus dans le json)
        self.__s_items = dict()  # Collection des items avec les clés converties en chaîne

        self.__menu = dict()  # Contenu de l'objet menu
        self.__menu_file = ""  # Chemin d'accès au fichier de menu
        self.__menu_loaded = False  # Indique si un menu a été chargé
        self.__menu_file_mime_type = ""  # Type mime du fichier de menu (actuellement,
        # 'application/json' et 'application/x-yaml' sont supportés)

        self.__sorted = sort_items  # Indique s'il faut trier les items de menu par le champ 'id'
        self.__last_choice = ""  # Clé de l'item choisi par l'utilisateur
        self.__last_return_code = 0  # Code retour de la dernière commande exécutée
        self.__key_length_max = 0  # Longueur de la plus longue clé (sert pour justifier l'affichage)
        self.__int_sortable = True  # Indique si le tri peut être numérique (sinon, il sera alphabétique)
        if menu_file != "":
            self.load_file(menu_file)

    # Accesseurs
    def get_menu_file(self):
        return self.__menu_file

    # Mutateurs
    def sort(self):
        self.__sorted = True

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
                    if "conditions" in my_item:
                        for my_condition in my_item["conditions"]:
                            p = subprocess.run(my_condition, shell=True)
                            if not p.returncode == 0:
                                authorized = False
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
                        if "id" in my_item:
                            new_item.set_key(my_item["id"])
                        if "text" in my_item:
                            new_item.set_text(my_item["text"])
                        if "format" in my_item:
                            new_item.set_text_format(my_item["format"])
                        if "commands" in my_item:
                            for my_command in my_item["commands"]:
                                new_item.add_command(my_command)
                        if "wait_after" in my_item:
                            new_item.set_wait_after(my_item["wait_after"])
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
        try:
            self.__menu_file_mime_type = mimetypes.guess_type(self.__menu_file)[0]
            fp = open(self.__menu_file, "r")
            if self.__menu_file_mime_type == "application/json":
                self.load_json(fp.read())
            elif self.__menu_file_mime_type == "application/x-yaml":
                self.load_yaml(fp)
            else:
                print_fmt("Format non pris en charge : " + str(self.__menu_file_mime_type), "ERROR")
            fp.close()
            self.__update()
        except Exception as e:
            print_fmt("Impossible de charger le fichier de menu [" + self.__menu_file + "]", "ERROR")
            print_fmt(e.__str__(), "ERROR")

    def load_json(self, json_string):
        try:
            self.__menu_loaded = False
            self.__menu = json.loads(json_string)
            self.__menu_loaded = True
        except Exception as e:
            print_fmt("Format json incorrect dans le fichier [" + self.__menu_file + "]", "ERROR")
            print_fmt(e.__str__(), "ERROR")

    def load_yaml(self, yaml_fp):
        try:
            self.__menu_loaded = False
            self.__menu = yaml.safe_load(yaml_fp)
            self.__menu_loaded = True
        except Exception as e:
            print_fmt("Format yaml incorrect dans le fichier [" + self.__menu_file + "]", "ERROR")
            print_fmt(e.__str__(), "ERROR")

    def print_title(self):
        print_fmt(self.__title, self.__format)

    def print_description(self):
        for my_line in self.__description:
            print_fmt(my_line, "MENU", 2)
        print_fmt("", "MENU")

    def print_items(self):
        if self.__sorted:
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
        if self.__sorted:
            str_keys.sort()
        self.__last_choice = read_fmt("Votre choix parmi [" + ", ".join(str_keys) + "]")
        while not (str(self.__last_choice) in str_keys or str(self.__last_choice) == ""):
            print_fmt("Choisissez parmi les valeurs proposées " + str(str_keys), "ERROR")
            self.__last_choice = read_fmt("Votre choix parmi [" + ", ".join(str_keys) + "]")

    def print_menu(self):
        clear_screen()
        self.print_title()
        self.print_description()
        self.print_items()
        print_fmt("")

    def execute(self, extra_arguments=[]):
        if self.__menu_loaded:
            exit_menu = False
            while not exit_menu:
                if len(extra_arguments) == 0:
                    self.print_menu()
                if len(self.__items) > 0:
                    if len(extra_arguments) > 0:
                        self.__last_choice = extra_arguments.pop(0)
                        self.__s_items[self.__last_choice].set_wait_after("False")
                        exit_menu = True
                    else:
                        self.read_choice()

                    if self.__last_choice == "":
                        print_fmt("=> Abandon...", "MENU", 4)
                        exit_menu = True
                    else:
                        self.__last_return_code = self.__s_items[self.__last_choice].execute_commands(extra_arguments)

                else:
                    print_fmt("Aucun item a proposer. Complétez le fichier " + self.__menu_file + " !", "ERROR")
                    self.__last_return_code = -1
                    exit_menu = True

            return self.__last_return_code
        else:
            print_fmt("Aucun menu à afficher", "ERROR")

    def debug(self):
        print("")
        print("            === Debug infos ===")
        print("menu_file            : " + self.__menu_file)
        print("menu_file_mime_type  : " + self.__menu_file_mime_type)
        print("id                   : " + self.__id)
        print("nb_items             : " + str(len(self.__items)))
        print("last_choice          : " + self.__last_choice)
        print("sorted               : " + str(self.__sorted))
        print("last_return_code     : " + str(self.__last_return_code))
        print("")


#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    my_menu = Menu()
#    my_menu.load_file(str(Path.home()) + "/git/menu/.menu/menu_example.json")
    my_menu.load_file(str(Path.home()) + "/git/menu/json/menu.json")

    my_menu.sort()
    my_menu.execute()

    my_menu.debug()
