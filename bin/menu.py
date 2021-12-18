#!/usr/bin/env python3

# Import des modules
import os
from optparse import OptionParser
from module_globals import *

from _Menu_class import Menu

# Lecture des arguments d'appel
parser = OptionParser()
parser.add_option("-f",
                  "--menu-file",
                  dest="menu_file",
                  help="Fichier de menu",
                  default=os.path.expanduser('~') + "/.menu/menu.json"
                  )
(options, args) = parser.parse_args()

# Contrôle des arguments
if not os.path.isfile(options.menu_file):
    print_fmt("Le fichier " + options.menu_file + " n'existe pas...", "ERROR")
    exit(-1)

# Construction du menu
my_menu = Menu(options.menu_file,
               sort_items=True
               )

# Execution du menu
my_menu.execute()
