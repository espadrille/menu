import json
import os
import pathlib
import re
import sys
import unicodedata

# Jolies couleurs = vrai ;-)

COLORS = {
    "BOLD": "\033[1m",
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "MAUVE": "\033[34m",
    "PURPLE": "\033[35m",
    "CYAN": "\033[36m",
    "WHITE": "\033[37m",
    "BK_BLACK": "\033[40m",
    "BK_RED": "\033[41m",
    "BK_GREEN": "\033[42m",
    "BK_YELLOW": "\033[43m",
    "BK_MAUVE": "\033[44m",
    "BK_PURPLE": "\033[45m",
    "BK_CYAN": "\033[46m",
    "BK_WHITE": "\033[47m",
    "RESET": "\033[0m",
}


class GlobalVars:
    def __init__(self):
        # Declaration des variables globales
        self.CURRENT_ENVIRONMENT = ""
        self.CURRENT_PROJECT = ""
        self.TOOLS_DIRECTORY = ""
        self.refresh()

    def refresh(self):
        # Rafraichit les variables globales
        if os.path.isfile(str(pathlib.Path.home()) + "/.menu/conf.json"):
            with open(str(pathlib.Path.home()) + "/.menu/conf.json", "r") as environment_file:
                environment = json.load(environment_file)
            self.CURRENT_ENVIRONMENT = environment["globals"]["environment"]

            if len(os.getcwd().split("/")) == 7:
                self.CURRENT_PROJECT = ""
                if os.getcwd().split("/")[-3] == "AWS" and os.getcwd().split("/")[-2] == "roots":
                    self.CURRENT_PROJECT = os.getcwd().split("/")[-1]

            self.TOOLS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def clear_screen():
    # It is for macOS and Linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # It is for Windows platfrom
        _ = os.system('cls')


def repeat(text, nb=2):
    #
    # Repeter un caractere (ou plusieurs...), sans retour a la ligne
    #
    # Exemple :
    #    repeat("e", 10)
    # Retourne 10 caracteres 'e' a la suite...
    #
    retour = ""
    for i in range(nb):
        retour = retour + text
    return retour


def print_fmt(text, text_format="", indent=0, newline=True):
    #
    # Propose un affichage formate.
    #
    # Il est possible de cumuler plusieurs formats. Par exemple :
    #     print_fmt("Texte à afficher", text_format=["BLUE", "BOLD"], indent=4)
    # Affiche "Texte à afficher" en bleu gras, et indente de 4 espaces
    #
    # Les valeurs de text_format peuvent être les suivantes :
    #     TITRE1, TITRE2, TITRE3 : Formats de titre
    #     OK, WARNING, ERROR : Formats standards en couleur (respectivement vert, jaune, rouge)
    #     COMMAND : Utilise pour afficher une commande linux exécutée par un script (inverse video)
    #     BOLD, RED, GREEN, YELLOW, MAUVE, CYAN, PURPLE : Affiche le texte dans la couleur demandée
    #     (ou en gras pour BOLD)
    #
    # La valeur de 'indent' indique le nombre d'espaces à afficher avant la chaine (pour indenter)
    #     <valeur numérique> : Nombre d'espaces à afficher avant la chaine (pour l'indenter)
    #

    screen_heigth, screen_width = os.popen('stty size', 'r').read().split()

    my_text = str(text).rstrip()
    my_color = ""
    my_indent = indent
    if text_format == "TITRE1":
        my_color = COLORS["BOLD"] + COLORS["MAUVE"]
        my_indent = 8
    elif text_format == "TITRE2":
        my_color = COLORS["BOLD"] + COLORS["MAUVE"]
        my_indent = 4
    elif text_format == "TITRE3":
        my_color = COLORS["BOLD"] + COLORS["MAUVE"]
        my_indent = 2
    elif text_format == "COMMAND":
        my_color = COLORS["BLACK"] + COLORS["BK_WHITE"]
    elif text_format == "MENU":
        my_color = COLORS["BOLD"] + COLORS["MAUVE"]
    elif text_format == "OK":
        my_color = COLORS["BOLD"] + COLORS["GREEN"]
    elif text_format == "WARNING":
        my_color = COLORS["BOLD"] + COLORS["YELLOW"]
    elif text_format == "ERROR":
        my_color = COLORS["BOLD"] + COLORS["RED"]
    elif text_format == "":
        my_color = ""
    else:
        if text_format in COLORS:
            my_color = COLORS[text_format]

    if text_format == "TITRE1":
        print("")
        print(repeat(' ', my_indent) + my_color + repeat("=", len(my_text)) + COLORS["RESET"])
        print(repeat(' ', my_indent) + my_color + my_text + COLORS["RESET"])
        print(repeat(' ', my_indent) + my_color + repeat("=", len(my_text)) + COLORS["RESET"])
        print("", end="")
    elif text_format == "TITRE2":
        print("")
        print(repeat(' ', my_indent) + my_color + my_text + COLORS["RESET"])
        print(repeat(' ', my_indent) + my_color + repeat("-", len(my_text)) + COLORS["RESET"])
        print("", end="")
    elif text_format == "TITRE3":
        print("")
        print(repeat(' ', my_indent) + my_color + my_text + COLORS["RESET"])
        print("", end="")
    elif text_format == "COMMAND":
        print(repeat(' ', my_indent) + my_color + my_text + COLORS["RESET"], end="")
    elif text_format == "OK":
        print(repeat(' ', my_indent) + my_color + "[OK] " + my_text + COLORS["RESET"], end="")
    elif text_format == "WARNING":
        print(repeat(' ', my_indent) + my_color + "[WARNING] " + my_text + COLORS["RESET"], end="")
    elif text_format == "ERROR":
        print(repeat(' ', my_indent) + my_color + "[ERROR] " + my_text + COLORS["RESET"], end="")
    else:
        print(repeat(' ', my_indent) + my_color + my_text + COLORS["RESET"], end="")
    if newline:
        print("")


def print_tab(title="", headers=[], datas=[], footer=None, text_format="", indent=0):
    column_separator = " | "

    # Calcul des longueurs de champs pour ajuster la taille des colonnes du tableau
    # Le tableau $LongueurChamps contient une valeur pour chaque colonne
    field_lengths = []

    # Initialiser les largeurs de colonnes en parcourant les entêtes et les datas
    i_col = 0
    for my_header in headers:
        field_lengths.append(len(my_header.split("|")[0].strip()))
        i_col = i_col + 1
    for my_data_line in datas:
        # Pour chaque ligne, ajuster les largeurs de colonnes si besoin
        i_col = 0
        if type(my_data_line) is list:
            for my_data in my_data_line:
                if (i_col + 1) > len(field_lengths):
                    field_lengths.append(len(my_data.split("|")[0].strip()))
                if len(my_data.split("|")[0].strip()) > field_lengths[i_col]:
                    field_lengths[i_col] = len(my_data.split("|")[0].strip())
                i_col = i_col + 1
        else:
            if (i_col + 1) > len(field_lengths):
                field_lengths.append(len(my_data_line.split("|")[0].strip()))
            if len(my_data_line.split("|")[0].strip()) > field_lengths[i_col]:
                field_lengths[i_col] = len(my_data_line.split("|")[0].strip())

    # Définir une ligne de pied de tableau par défaut
    if footer is None:
        footer = str(len(datas)) + " element(s)"

    # Calcule la longueur de la ligne complete (avec tous les champs), et cré la ligne de séparation avec des '-'
    line_length = 0
    separator_line = "+-"
    for MyLength in field_lengths:
        if line_length != 0:
            line_length = line_length + len(column_separator)
            separator_line = separator_line + re.sub("\s", "-", re.sub("\S", "+", column_separator))
        line_length = line_length + MyLength
        separator_line = separator_line + repeat("-", MyLength)
    # Agrandir la longueur de ligne et la ligne de separation si nécessaire pour que le titre passe dedans
    if len(title) > line_length:
        separator_line = separator_line + repeat("-", len(title) - line_length)
        line_length = len(title)
    # Agrandir la longueur de ligne et la ligne de separation si nécessaire pour que le pied passe dedans
    if len(footer) > line_length:
        separator_line = separator_line + repeat("-", len(footer) - line_length)
        line_length = len(footer)
    separator_line = separator_line + "-+"

    # Ouverture du tableau
    print_fmt("")

    # Titre
    if len(title) > 0:
        print_fmt("+-" + repeat("-", line_length) + "-+", text_format=text_format, indent=indent)
        centered_title = ("{:^" + str(line_length) + "}").format(title)
        print_fmt("| " + centered_title + " |", text_format=text_format, indent=indent)

    # Entêtes
    if len(headers) > 0:
        print_fmt(separator_line, text_format=text_format, indent=indent)
        header_line = ""
        i_col = 0

        for my_header in headers:
            length = field_lengths[i_col]
            if len(header_line) > 0:
                header_line = header_line + column_separator

            if "|" in my_header:
                my_header_array = my_header.split("|")
                my_header = my_header_array[0].strip()
                for MyCommand in my_header_array[1].split(","):
                    key = MyCommand.split("=")[0]
                    value = MyCommand.split("=")[1]
                    if key == "align":
                        if value == "right":
                            header_line = header_line + ("{:>" + str(length) + "}").format(my_header)
                        elif value == "center":
                            header_line = header_line + ("{:^" + str(length) + "}").format(my_header)
                        elif value == "left":
                            header_line = header_line + ("{:<" + str(length) + "}").format(my_header)
                        else:
                            header_line = header_line + ("{:<" + str(length) + "}").format(my_header)
            else:
                header_line = header_line + ("{:<" + str(length) + "}").format(my_header)
            i_col = i_col + 1
        print_fmt("| " + ("{:<" + str(line_length) + "}").format(header_line) + " |", text_format=text_format, indent=indent)

    # datas
    if len(datas) > 0:
        print_fmt(separator_line, text_format=text_format, indent=indent)
        for my_data_line in datas:
            data_line = ""
            i_col = 0
            if type(my_data_line) is list:
                # Tableau a 2 dimensions
                for my_data in my_data_line:
                    length = field_lengths[i_col]
                    if len(data_line) > 0:
                        data_line = data_line + column_separator

                    if "|" in my_data:
                        tab_my_data = my_data.split("|")
                        my_data = tab_my_data[0].strip()
                        for MyCommand in tab_my_data[1].split(","):
                            key = MyCommand.split("=")[0]
                            value = MyCommand.split("=")[1]
                            if key == "align":
                                if value == "right":
                                    data_line = data_line + ("{:>" + str(length) + "}").format(my_data)
                                elif value == "center":
                                    data_line = data_line + ("{:^" + str(length) + "}").format(my_data)
                                elif value == "left":
                                    data_line = data_line + ("{:<" + str(length) + "}").format(my_data)
                                else:
                                    data_line = data_line + ("{:<" + str(length) + "}").format(my_data)
                    else:
                        data_line = data_line + ("{:<" + str(length) + "}").format(my_data)
                    i_col = i_col + 1
            else:
                # Tableau a 1 dimension
                length = field_lengths[i_col]
                if "|" in my_data_line:
                    tab_my_data = my_data_line.split("|")
                    my_data_line = tab_my_data[0].strip()
                    for MyCommand in tab_my_data[1].split(","):
                        key = MyCommand.split("=")[0]
                        value = MyCommand.split("=")[1]
                        if key == "align":
                            if value == "right":
                                data_line = data_line + ("{:>" + str(length) + "}").format(my_data_line)
                            elif value == "center":
                                data_line = data_line + ("{:^" + str(length) + "}").format(my_data_line)
                            elif value == "left":
                                data_line = data_line + ("{:<" + str(length) + "}").format(my_data_line)
                            else:
                                data_line = data_line + ("{:<" + str(length) + "}").format(my_data_line)
                else:
                    data_line = data_line + ("{:<" + str(length) + "}").format(my_data_line)

            print_fmt("| " + ("{:<" + str(line_length) + "}").format(data_line) + " |", text_format=text_format,
                      indent=indent)

    # Pied
    if len(footer) > 0:
        print_fmt(separator_line, text_format=text_format, indent=indent)
        print_fmt("| " + ("{:>" + str(line_length) + "}").format(footer) + " |", text_format=text_format, indent=indent)

    # Fermeture du tableau
    if len(footer) > 0:
        print_fmt("+-" + repeat("-", line_length) + "-+", text_format=text_format, indent=indent)
    else:
        print_fmt(separator_line, text_format=text_format, indent=indent)

    print_fmt("")


def read_fmt(question, default="", format="CYAN", indent=0, newline=False):
    if default != "":
        question = question + " [" + default + "]"
    question = question + " :"
    print_fmt(text=question, text_format=format, indent=indent, newline=newline)
    response = input()
    if response == "":
        response = default
    return response


def read_choice_fmt(title="", choices=[], question="", text_format="CYAN", indent=0):
    options = ""
    if len(choices) == 1:
        # S'il n'y a qu'un choix possible, on le selectionne automatiquement
        retour = choices[0]['value']
    else:
        if title != "":
            print_fmt(text=title, text_format=text_format, indent=indent)

        i = 1
        for my_item in choices:
            print_fmt(str(i) + " : " + str(my_item['text']), text_format, indent + 2)
            if options == "":
                options = str(i)
            else:
                options = options + " " + str(i)
            i = i + 1

        choix_ok = False
        response = ""
        while not choix_ok:
            if question == "":
                question = "Faites un choix parmi (" + options + ") ou 'Entree'  pour sortir : "

            response = read_fmt(question=question, format=text_format, indent=indent)
            if response == "" or (response.isnumeric() and int(response) in range(1, i)):
                choix_ok = True
            else:
                print_fmt("Choisissez parmi les valeurs proposées (" + options + ")", "ERROR")

        if response == "":
            print_fmt("==> Abandon.", "BOLD")
            sys.exit(255)
        else:
            retour = choices[int(response) - 1]['value']

    return retour


def remove_accents(text):
    try:
        text = text.encode('utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


#
# =================================================================================================
# Test du module
#
if __name__ == "__main__":
    print_fmt("Ceci est un titre 1", text_format="TITRE1")
    print_fmt("Ceci est un titre 2", text_format="TITRE2")
    print_fmt("Ceci est un titre 3", text_format="TITRE3")
    print_fmt("Format 'OK' avec indent 8", text_format="OK", indent=8)
    print_fmt("Format 'WARNING' avec indent 8", text_format="WARNING", indent=8)
    print_fmt("Format 'ERROR' avec indent 8", text_format="ERROR", indent=8)
    print_fmt("Format 'BOLD' avec indent 4", text_format="BOLD", indent=4)
    print_fmt("Format 'MENU' avec indent 4", text_format="MENU", indent=4)

    my_globals = GlobalVars()
    print_fmt("CURRENT_ENVIRONMENT=" + my_globals.CURRENT_ENVIRONMENT, text_format="")
    print_fmt("CURRENT_PROJECT=" + my_globals.CURRENT_PROJECT, text_format="")
    print_fmt("TOOLS_DIRECTORY=" + my_globals.TOOLS_DIRECTORY, text_format="")

    # Creation d'une liste de choix
    MyList = [{
        'text': 'Mon texte 1',
        'value': 'Ma valeur 1'
    }, {
        'text': 'Mon texte 2',
        'value': 'Ma valeur 2'
    }, {
        'text': 'Mon texte 3',
        'value': 3
    }, {
        'text': 'Le choix supplémentaire',
        'value': 'Vous avez choisi le dernier item'
    }]
    # Ajout d'un autre choix dans la liste
    reponse = str(read_choice_fmt(title="Voici une liste :", choices=MyList, question="Choisissez votre valeur : "))
    print_fmt("Valeur correspondante a votre choix : " + reponse, text_format="GREEN")

    print_tab(title="Mon tableau de test avec un titre de tres grande largeur pour voir si tout est bien aligne",
              headers=["col1", "colonne 2 avec un grand libelle"],
              datas=[["essai plus long", "test centré|align=center"], ["essai", "test"]],
              footer="C'est le pied !",
              indent=4,
              text_format="CYAN")

    print_tab(title="Mon tableau a 1 dimension",
              headers=["col1"],
              datas=["essai plus long", "test centré|align=center", "essai", "test"],
              footer="C'est le pied !",
              indent=4,
              text_format="CYAN")
