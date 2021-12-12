# Import des modules
from module_globals import *


# Definition de la classe Command

class Command:
    def __init__(self, cmdline=""):
        self.__cmdline = cmdline
        self.__last_return_code = 0

    # Accesseurs
    def get_cmdline(self):
        return self.__cmdline

    def get_last_return_code(self):
        return self.__last_return_code

    # Mutateurs
    def set_cmdline(self, cmdline):
        self.__cmdline = str(cmdline)

    # Methodes privees

    # Methodes publiques
    def execute(self, cmdline="", whatif=False):
        if cmdline != "":
            self.__cmdline = cmdline
        print_fmt(cmdline, "COMMAND")
        if whatif:
            print_fmt("*** Whatif *** : la commande [" + self.__cmdline + "] n'a pas ete executee", format="YELLOW", indent=4)
        else:
            print_fmt("Execution de la commande [" + self.__cmdline + "]", format="YELLOW", indent=4)
            self.__last_return_code = os.system(self.__cmdline)
        return self.__last_return_code

    def print_cmdline(self):
        print_fmt(self.__cmdline, "COMMAND", 4)

    def print(self):
        print_fmt("Commande", "TITRE1")
        print_fmt("Ligne de commande", "TITRE2")
        self.print_cmdline()

#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    my_command = Command()

    my_command.set_cmdline("ls -la")
    my_command.print()
    print(my_command.execute())
