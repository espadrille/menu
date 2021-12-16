#!/usr/bin/env python3

# Import des modules
import os
import sys

from _Menu_class import Menu

# Construction du menu
my_menu = Menu(menu_file=os.path.dirname(sys.argv[0]) + "/../json/menu.json",
               sort_items=True
               )

# Execution du menu
my_menu.execute()
