# Import des modules
import readchar
import subprocess

from module_globals import *


# Definition de la classe Command

class Command(object):
    def __init__(self, order=0, command_line="", wait_after=False):
        self.__order = order
        self.__command_line = command_line
        self.__wait_after = False
        self.__last_return_code = 0

        self.set_wait_after(wait_after)

    # Accesseurs
    def get_order(self):
        return self.__order

    def get_command_line(self):
        return self.__command_line

    def get_wait_after(self):
        return self.__wait_after

    def get_last_return_code(self):
        return self.__last_return_code

    # Mutateurs
    def set_order(self, order):
        self.__order = order

    def set_command_line(self, command_line):
        self.__command_line = str(command_line)

    def set_wait_after(self, wait_after):
        self.__wait_after = False
        if wait_after == "True":
            self.__wait_after = True

    # Méthodes privées

    # Méthodes publiques
    def execute(self, command_line="", what_if=False, extra_arguments=[]):
        if command_line != "":
            self.__command_line = command_line
        if len(extra_arguments) > 0:
            self.__command_line = self.__command_line + ' ' + ' '.join(extra_arguments) 
        if what_if:
            print_fmt("*** what_if *** : la commande [" + self.__command_line + "] n'a pas été exécutée",
                      text_format="YELLOW",
                      indent=4
                      )
        else:
            self.print_command_line()
            try:
                # Exécution de la commande
                p = subprocess.run(self.__command_line, shell=True)
                self.__last_return_code = p.returncode
            except Exception as e:
                print_fmt(e.__str__(), "ERROR")
                print_fmt("Code retour de la commande : " + str(self.__last_return_code), "ERROR")

        if self.__wait_after or self.__last_return_code != 0:
            print_fmt("Appuyez sur une touche pour continuer...", "CYAN")
            readchar.readchar()
        return self.__last_return_code

    def print_command_line(self):
        print_fmt(text="==> ", indent=2, newline=False)
        print_fmt(self.__command_line, "COMMAND", 1)

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
