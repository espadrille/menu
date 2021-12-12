#!/usr/bin/env python3

# Import des modules
from _Command_class import Command

my_command = Command()

my_command.set_cmdline("ls -la")
my_command.print()
print(my_command.execute())
