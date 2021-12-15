#!/usr/bin/env python3

# Import des modules
from _Menu_class import Menu

my_menu = Menu()
my_menu.load_file("../json/menu.json")

my_menu.sort()
my_menu.execute()
