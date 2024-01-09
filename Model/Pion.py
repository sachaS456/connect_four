# Model/Pion.py

from Model.Constantes import *

#
# Ce fichier implémente les données/fonctions concernant le pion
# dans le jeu du Puissance 4
#
# Un pion est caractérisé par :
# - sa couleur (const.ROUGE ou const.JAUNE)
# - un identifiant de type int (pour l'interface graphique)
#
# L'identifiant sera initialisé par défaut à None
#

def type_pion(pion: dict) -> bool:
    """
    Détermine si le paramètre peut être ou non un Pion

    :param pion: Paramètre dont on veut savoir si c'est un Pion ou non
    :return: True si le paramètre correspond à un Pion, False sinon.
    """
    return type(pion) == dict and len(pion) == 2 and const.COULEUR in pion.keys() \
        and const.ID in pion.keys() \
        and pion[const.COULEUR] in const.COULEURS \
        and (pion[const.ID] is None or type(pion[const.ID]) == int)

def construirePion(couleur:int)->dict:
    """
    Créé un pion

    :param couleur: determine la couleur de ce pion
    :return: un dictionnaire qui symbolise le pion
    """
    if type(couleur) != int:
        raise TypeError("construirePion : Le paramètre n’est pas de type entier")

    if couleur != const.ROUGE and couleur != const.JAUNE:
        raise TypeError(f"construirePion : la couleur {couleur} n’est pas correcte")

    return {const.COULEUR : couleur, const.ID: None}

def getCouleurPion(pion:dict)->int:
    """
    Determine la couleur du pion

    :param pion: un pion sous forme de dictionnaire
    :return: la couleur du pion
    """

    if type_pion(pion) == False:
        raise TypeError("getCouleurPion : Le paramètre n’est pas un pion")
    return pion[const.COULEUR]

def setCouleurPion(pion:dict, couleur:int)->None:
    """
    Définit la coulour du pion

    :param pion: le pion dont on veut définir sa couleur
    :return: ne retourne rien
    """

    if type_pion(pion) == False:
        raise TypeError(" setCouleurPion : Le premier paramètre n’est pas un pion")

    if type(couleur) != int:
        raise TypeError("setCouleurPion : Le second paramètre n’est pas un entier")

    if couleur != const.ROUGE and couleur != const.JAUNE:
        raise TypeError(f"setCouleurPion : Le second paramètre {couleur} n’est pas une couleur")

    pion[const.COULEUR] = couleur
    return None

def getIdPion(pion:dict)->int:
    """
    Détermine l'identifiant du pion

    :param pion: un pion
    :return: identifiant du pion
    """
    if type_pion(pion) == False:
        raise TypeError(" getIdPion : Le premier paramètre n’est pas un pion")

    return pion[const.ID]

def setIdPion(pion:dict, id:int)->int:
    """
    Définit l'identifiant du pion
    :param pion: pion à définit l'identifiant
    :param id: identifiant à définit au pion choisi
    :return: None
    """

    if type_pion(pion) == False:
        raise TypeError(" setIdPion : Le premier paramètre n’est pas un pion")

    if type(id) != int:
        raise TypeError("setIdPion : Le second paramètre n’est pas un entier")

    pion[const.ID] = id
    return None
