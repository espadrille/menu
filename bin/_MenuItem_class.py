# Import des modules
from module_globals import *
import _Command_class
import collections
from _Command_class import Command


# Definition de la classe MenuItem

class MenuItem:
    def __init__(self, key="", text="", text_format="MENU", commands=None):

        if commands is None:
            commands = {}
        self.__key = ""
        self.__text = ""
        self.__format = ""
        self.__commands = {}
        self.__key_length = 0
        self.__last_return_code = 0

        self.set_key(key)
        self.set_text(text)
        self.set_format(text_format)
        self.set_commands(commands)
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

    def get_command(self, command_id=0):
        return self.__commands[command_id]

    def get_commands(self):
        return self.__commands.items()

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

    def set_commands(self, commands):
        self.__commands = commands

    # Méthodes privées

    # Méthodes publiques
    def add_command(self, command):
        new_command = Command()
        if "order" in command:
            new_command.set_order(command["order"])
        if "command" in command:
            new_command.set_command_line(command["command"])
        if "wait_after" in command:
            new_command.set_wait_after(command["wait_after"])
        self.__commands[new_command.get_order()] = new_command

    def execute_commands(self):
        for my_key, my_command in collections.OrderedDict(sorted(self.__commands.items(),
                                                                 key=lambda t: t[1].get_order())).items():
            self.__last_return_code = my_command.execute()
        return self.__last_return_code

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
    my_item = MenuItem("1", "Premier choix")
    my_item.set_key_length(10)
    my_item.print()