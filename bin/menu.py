#!/usr/bin/env python3

# Import des modules
import os
import sys

from _Menu_class import Menu

my_menu = Menu()
my_menu.load_file(os.path.dirname(sys.argv[0]) + "/../json/menu.json")

my_menu.sort()
my_menu.execute()
