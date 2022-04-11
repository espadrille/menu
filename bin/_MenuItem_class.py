# Import des modules
import collections
import readchar

from module_globals import *
from _Command_class import Command


# Definition de la classe MenuItem

class MenuItem(object):
    def __init__(self, key="", text="", text_format="MENU", commands=None, wait_after="False"):

        if commands is None:
            commands = {}
        self.__key = ""
        self.__text = ""
        self.__text_format = ""
        self.__commands = {}
        self.__key_length = 0
        self.__last_return_code = 0
        self.__wait_after = True

        self.set_key(key)
        self.set_text(text)
        self.set_text_format(text_format)
        self.set_commands(commands)
        self.set_key_length(len(str(key)))
        self.set_wait_after(wait_after)

    # Accesseurs
    def get_key(self):
        return self.__key

    def get_text(self):
        return self.__text

    def get_text_format(self):
        return self.__text_format

    def get_key_length(self):
        return self.__key_length

    def get_command(self, command_id=0):
        return self.__commands[command_id]

    def get_commands(self):
        return self.__commands.items()

    def get_wait_after(self):
        return self.__wait_after

    # Mutateurs
    def set_key(self, key):
        self.__key = key
        self.__key_length = len(str(key))

    def set_text(self, text):
        self.__text = text

    def set_text_format(self, text_format):
        self.__text_format = text_format

    def set_key_length(self, length):
        self.__key_length = length

    def set_commands(self, commands):
        self.__commands = commands

    def set_wait_after(self, wait_after):
        self.__wait_after = False
        if str(wait_after).lower() == "true":
            self.__wait_after = True

    # Méthodes privées

    # Méthodes publiques
    def add_command(self, command):
        new_command = Command()
        if "order" in command:
            new_command.set_order(command["order"])
        if "command_line" in command:
            new_command.set_command_line(command["command_line"])
        if "wait_after" in command:
            new_command.set_wait_after(command["wait_after"])
        self.__commands[new_command.get_order()] = new_command

    def execute_commands(self, extra_arguments=[]):
        wait_after_command = False
        for my_key, my_command in collections.OrderedDict(sorted(self.__commands.items(),
                                                                 key=lambda t: t[1].get_order())).items():
            self.__last_return_code = my_command.execute(extra_arguments=extra_arguments)
            wait_after_command = my_command.get_wait_after()
            if self.__last_return_code != 0:
                break
        # Attendre après l'exécution si c'est demandé et si la dernière commande ne l'a pas déjà fait
        if self.__wait_after and (not wait_after_command) and self.__last_return_code == 0 and len(extra_arguments) == 0:
            print_fmt("Appuyez sur une touche pour continuer...", "CYAN")
            readchar.readchar()
        return self.__last_return_code

    def print(self):
        if type(self.__key) is int:
            print_fmt(str(self.__key).rjust(self.__key_length) + " : " + self.__text, self.__text_format, 2)
        else:
            print_fmt(str(self.__key).ljust(self.__key_length) + " : " + self.__text, self.__text_format, 2)

    def debug(self):
        print("")
        print("          === Debug infos ===")
        print("key                : " + str(self.__key))
        print("text               : " + self.__text)
        print("format             : " + self.__text_format)
        print("key_length         : " + str(self.__key_length))
        print("last_return_code   : " + str(self.__last_return_code))
        print("wait_after         : " + str(self.__wait_after))
        print("")


#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    my_item = MenuItem("1", "Premier choix")
    my_item.set_key_length(10)
    my_item.print()
