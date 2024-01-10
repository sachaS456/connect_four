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