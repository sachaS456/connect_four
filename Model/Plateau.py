from Model.Constantes import *
from Model.Pion import *


#
# Le plateau représente la grille où sont placés les pions.
# Il constitue le coeur du jeu car c'est dans ce fichier
# où vont être programmées toutes les règles du jeu.
#
# Un plateau sera simplement une liste de liste.
# Ce sera en fait une liste de lignes.
# Les cases du plateau ne pourront contenir que None ou un pion
#
# Pour améliorer la "rapidité" du programme, il n'y aura aucun test sur les paramètres.
# (mais c'est peut-être déjà trop tard car les tests sont fait en amont, ce qui ralentit le programme...)
#

def type_plateau(plateau: list) -> bool:
    """
    Permet de vérifier que le paramètre correspond à un plateau.
    Renvoie True si c'est le cas, False sinon.

    :param plateau: Objet qu'on veut tester
    :return: True s'il correspond à un plateau, False sinon
    """
    if type(plateau) != list:
        return False
    if len(plateau) != const.NB_LINES:
        return False
    wrong = "Erreur !"
    if next((wrong for line in plateau if type(line) != list or len(line) != const.NB_COLUMNS), True) == wrong:
        return False
    if next((wrong for line in plateau for c in line if not(c is None) and not type_pion(c)), True) == wrong:
        return False
    return True

def construirePlateau()->list:
    """
    Créé un plateau de taille const.NB_LINES lignes et const.NB_COLUMNS colonnes

    :return: un tableau représentant un plateau
    """
    lst = []
    for i in range(const.NB_LINES):
        lst.append([])
        for j in range(const.NB_COLUMNS):
            lst[i].append(None)
    return lst

def placerPionPlateau(p:list, pion:dict, nc:int)->int:
    """
    Dépose un pion dans le plateau dans une colonne indiqué

    :param p: Dépose un pion dans ce plateau
    :param pion: Dépose ce pion
    :param nc:  Dépose le pion dans la colonne indiquée
    :return:  numéro de ligne où se retrouve le pion
    """

    if type_plateau(p) == False:
        raise TypeError("placerPionPlateau : Le premier paramètre ne correspond pas à un plateau")

    if type_pion(pion) == False:
        raise TypeError("placerPionPlateau : Le second paramètre n’est pas un pion")

    if type(nc) != int:
        raise TypeError("placerPionPlateau : Le troisième paramètre n’est pas un entier")
    if nc < 0 or nc > const.NB_COLUMNS:
        raise ValueError(f"placerPionPlateau : La valeur de la colonne {nc} n’est pas correcte")

    i = -1
    while i < const.NB_LINES - 1 and p[i+1][nc] == None:
        i+=1

    p[i][nc] = pion
    return i