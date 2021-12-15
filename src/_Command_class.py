# Import des modules
from module_globals import *


# Definition de la classe Command

class Command:
    def __init__(self, order=0, command_line="", wait_after=False):
        self.__order = order
        self.__command_line = command_line
        self.__wait_after = wait_after
        self.__last_return_code = 0

    # Accesseurs
    def get_order(self):
        return self.__order

    def get_command_line(self):
        return self.__command_line

    def get_last_return_code(self):
        return self.__last_return_code

    # Mutateurs
    def set_order(self, order):
        self.__order = order

    def set_command_line(self, command_line):
        self.__command_line = str(command_line)

    def set_wait_after(self, wait_after):
        self.__wait_after = wait_after

    # Méthodes privées

    # Méthodes publiques
    def execute(self, command_line="", what_if=False):
        if command_line != "":
            self.__command_line = command_line
        self.print_command_line()
        if what_if:
            print_fmt("*** what_if *** : la commande [" + self.__command_line + "] n'a pas été exécutée",
                      format="YELLOW",
                      indent=4
                      )
        else:
            print_fmt("Execution de la commande [" + self.__command_line + "]",
                      format="YELLOW",
                      indent=4
                      )
            self.__last_return_code = os.system(self.__command_line)
        return self.__last_return_code

    def print_command_line(self):
        print_fmt(self.__command_line, "COMMAND", 4)

    def print(self):
        self.print_command_line()


#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    my_command = Command()

    my_command.set_command_line("ls -la")
    my_command.print()
    print(my_command.execute())
