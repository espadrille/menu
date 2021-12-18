# Menu

Projet de menu en python

## Installation

Créer un utilisateur 'menu' :
```commandline
sudo adduser menu
```
Répondez à toutes les questions qui sont posées.
Ouvrir une session pour l'utilisateur 'menu'
```commandline
su - menu
```
Cloner le présent dépôt git
```commandline
git clone https://github.com/espadrille/menu.git
```
Un nouveau dossier 'menu' s'est créé dans le dossier courant.
Quitter la session 'menu'
```commandline
exit
```
Lorsqu'on cré un utilisateur, le système cré automatiquement un groupe qui porte le même
nom que l'utilisateur. Le groupe 'menu' a donc été créé.
Enregistrer votre utilisateur dans le groupe 'menu' (remplacez ```<votre_login>``` par votre compte utilisateur)
```commandline
sudo usermod --append --groups menu <votre_login>
```
Pour utiliser le menu en tapant simplement 'menu', il faut créer un alias
à l'ouverture de session pour tous les membres du groupe 'menu'.
Modifiez le fichier /etc/bash.bashrc
```commandline
sudo nano /etc/bash.bashrc
```
Ajouter les lignes suivantes à la fin du fichier /etc/bash.bashrc
```commandline
# Ajoutez les utilisateurs au groupe 'menu' pour 
# qu'ils accedent au menu avec la commande 'menu'
if groups | grep &>/dev/null "menu"; then
    alias menu="/home/menu/menu/bin/menu.py"
fi
```
Enregistrer le fichier.
La phase d'installation proprement dite est terminée. Il reste à créer un fichier de configuration pour le menu.

Créez un nouveau fichier ~/.menu/menu.json avec le contenu suivant
```json
{
  "menu": {
    "id": "mon_id",
    "title": "Mon menu JSON",
    "description": [
      "Exemple de fichier json pour paramétrer un menu"
    ],
    "format": "TITRE1",
    "items": [
      {
        "id": 1,
        "text": "Premier item",
        "format": "MENU",
        "commands": [
          {
            "order": 1,
            "command": "echo 'Première commande du premier item'"
          }
        ]
      },
      {
        "id": "2a2",
        "text": "Deuxième item",
        "format": "MENU",
        "commands": [
          {
            "order": 1,
            "command": "echo 'Première commande du deuxième item'",
            "wait_after": "True"
          },
          {
            "order": 2,
            "command": "echo 'Deuxième commande du deuxième item'"
          }
        ]
      },
      {
        "id": 3,
        "text": "Troisième item réservé au groupe 'menu'",
        "format": "GREEN",
        "commands": [
          {
            "order": 1,
            "command": "echo 'Première commande du troisième item'",
            "wait_after": "false"
          }
        ],
        "security": {
          "authorized_groups": [
            "menu"
          ]
        }
      }
    ]
  }
}
```
puis testez le menu
```commandline
menu
```
Ceci vous donne un premier aperçu de l'utilisation de ce menu.
À vous d'imaginer les options qui vous seront utiles, et les configurer dans le fichier json.

Si vous êtes plus à l'aise avec yaml, il est également possible d'écrire le fichier de configuration en yaml.

Un exemple de menu en json et son équivalent en yaml sont fournis dans le dossier '.menu' du dépôt git.

## Utilisation
Lancez simplement la commande
```commandline
menu
```
Et le menu s'affiche
```text

        =============
        Mon menu JSON
        =============

  Exemple de fichier json pour paramétrer un menu

  1   : Premier item
  2a2 : Deuxième item
  3   : Troisième item réservé au groupe 'menu'

Votre choix parmi [1, 2a2, 3] :
```
