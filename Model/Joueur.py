import random

from Model.Constantes import *
from Model.Pion import *
from Model.Plateau import *


#
# Ce fichier contient les fonctions gérant le joueur
#
# Un joueur sera un dictionnaire avec comme clé :
# - const.COULEUR : la couleur du joueur entre const.ROUGE et const.JAUNE
# - const.PLACER_PION : la fonction lui permettant de placer un pion, None par défaut,
#                       signifiant que le placement passe par l'interface graphique.
# - const.PLATEAU : référence sur le plateau de jeu, nécessaire pour l'IA, None par défaut
# - d'autres constantes nécessaires pour lui permettre de jouer à ajouter par la suite...
#

def type_joueur(joueur: dict) -> bool:
    """
    Détermine si le paramètre peut correspondre à un joueur.

    :param joueur: Paramètre à tester
    :return: True s'il peut correspondre à un joueur, False sinon.
    """
    if type(joueur) != dict:
        return False
    if const.COULEUR not in joueur or joueur[const.COULEUR] not in const.COULEURS:
        return False
    if const.PLACER_PION not in joueur or (joueur[const.PLACER_PION] is not None
            and not callable(joueur[const.PLACER_PION])):
        return False
    if const.PLATEAU not in joueur or (joueur[const.PLATEAU] is not None and
        not type_plateau(joueur[const.PLATEAU])):
        return False
    return True

def construireJoueur(col:int)->dict:
    """
    Créé un joueur

    :param col: définit la couleur des pions du joueur
    :return: un joueur sous forme de dictionnaire
    """

    if type(col) != int:
        raise TypeError("construireJoueur : Le paramètre n’est pas un entier")

    if col not in const.COULEURS:
        raise ValueError(f"construireJoueur : L’entier donné {col} n’est pas une couleur.")

    return {const.COULEUR: col, const.PLATEAU: None, const.PLACER_PION: None}

def getCouleurJoueur(j:dict)->int:
    """
    Determine la couleur de pion d'un joueur

    :param j: joueur ciblé
    :return: couleur de pion du joueur
    """

    if type_joueur(j) == False:
        raise TypeError("getCouleurJoueur : Le paramètre ne correspond pas à un joueur")

    return j[const.COULEUR]

def getPlateauJoueur(j:dict)->dict:
    """
    Determine le plateau

    :param j: joueur ciblé
    :return: plateau du joueur
    """

    if type_joueur(j) == False:
        raise TypeError("getPlateauJoueur : Le paramètre ne correspond pas à un joueur")

    return j[const.PLATEAU]

def getPlacerPionJoueur(j:dict)->callable:
    """
    Determine la fonction qui permet de faire jouer le joueur

    :param j: joueur ciblé
    :return: fonction contenue dans ce dictionnaire
    """

    if type_joueur(j) == False:
        raise TypeError("getPlacerPionJoueur : Le paramètre ne correspond pas à un joueur")

    return j[const.PLACER_PION]

def getPionJoueur(j:dict)->dict:
    """
    Créé un pion de la couleur du joueur

    :param j: joueur choisi
    :return: un pion de la couleur du joueur
    """

    if type_joueur(j) == False:
        raise TypeError("getPionJoueur : Le paramètre ne correspond pas à un joueur")

    return construirePion(getCouleurJoueur(j))

def setPlateauJoueur(j:dict, p:dict)->None:
    """
    Affecte le plateau au joueur

    :param j: représente un joueur
    :param p: représente un plateau
    :return: rien
    """

    if type_joueur(j) == False:
        raise TypeError("setPlateauJoueur : Le premier paramètre ne correspond pas à un joueur")

    if type_plateau(p) == False:
        raise TypeError("setPlateauJoueur : Le second paramètre ne correspond pas à un plateau")

    j[const.PLATEAU] = p
    return None

def setPlacerPionJoueur(j:dict, fn:callable)->None:
    """
    Affecte la fonction au joueur

    :param j: représente un joueur
    :param fn: représente une fonction
    :return: rien
    """

    if type_joueur(j) == False:
        raise TypeError("setPlacerPionJoueur : Le premier paramètre ne correspond pas à un joueur")

    if callable(fn) == False:
        raise TypeError("setPlacerPionJoueur : Le second paramètre ne correspond pas à une fonction")

    j[const.PLACER_PION] = fn
    return None

def _placerPionJoueur(j:dict)->int:
    """
    Donne une colonne où un pion peut être dans une colonne disponible de façon aléatoire

    :param j: représente un joueur
    :return: un entier représentant la colonne
    """

    nb = 0
    p = getPlateauJoueur(j)

    if getModeEtenduJoueur(j) == False:
        nb = random.randint(0, const.NB_COLUMNS - 1)
        while p[0][nb] != None:
            nb = random.randint(0, const.NB_COLUMNS - 1)
    else:
        nb = random.randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES - 1)

        if nb >= 0 and nb < const.NB_COLUMNS:
            while p[0][nb] != None:
                nb = random.randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES - 1)

    return nb

def initialiserIAJoueur(j:dict, premier:bool)->None:
    """
    Affecte la fonction _placerPionJoueur au joueur passé en paramètre

    :param j: représente un joueur
    :param premier: indique si le joueur joue en premier (True) ou en second (False)
    :return: rien
    """

    if type_joueur(j) == False:
        raise TypeError("initialiserIAJoueur : Le premier paramètre n’est pas un joueur")

    if type(premier) != bool:
        raise TypeError("initialiserIAJoueur : Le second paramètre n’est pas un booléen")

    from Model.IAJoueur import _placerPionJoueur2
    setPlacerPionJoueur(j, _placerPionJoueur2)
    return None

def getModeEtenduJoueur(j:dict)->bool:
    """
    Determine si le mode de jeu est en normal ou en mode étendu

    :param j: un joueur
    :return:  True si on est en mode étendu, False sinon
    """

    if type_joueur(j) == False:
        raise TypeError("getModeEtenduJoueur : Le paramètre ne correspond pas à un joueur")

    return const.MODE_ETENDU in j

def setModeEtenduJoueur(j:dict, b = True)->None:
    """
    Ajoute ou supprime la clé const.MODE_ETENDU dans le dictionnaire représentant le joueur en fonction du booléen

    :param j: un joueur
    :param b: si le booléen est à False, on supprime la clé, sinon on l’ajoute
    :return: rien
    """
    if type_joueur(j) == False:
        raise TypeError("setModeEtenduJoueur : Le premier paramètre ne correspond pas à un joueur")

    if type(b) != bool:
        raise  TypeError("setModeEtenduJoueur : le second paramètre ne correspond pas à un booléen")

    if b:
        j[const.MODE_ETENDU] = True
    else:
        if getModeEtenduJoueur(j):
            del(j[const.MODE_ETENDU])

    return None