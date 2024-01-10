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


def toStringPlateau(p: list) -> str:
    """
    Converti le plateau de tableau en chaîne de caractère affichable
    :param p: plateau
    :return: chaîne de caractère représentant le plateau
    """
    r = ""
    for i in range(const.NB_LINES):
        r += "|"
        for j in range(const.NB_COLUMNS):
            case = p[i][j]
            if case == None:
                case = " "
            elif case[const.COULEUR] == const.ROUGE:
                case = "\x1B[41m \x1B[0m"
            elif case[const.COULEUR] == const.JAUNE:
                case = "\x1B[43m \x1B[0m"

            r += f"{case}|"
        r+="\n"
    return r

def detecter4horizontalPlateau(p:list, col:int)->list:
    """
    Détecte s'il y a 4 pions alignés horizontalements

    :param p: plateau à vérifier
    :param col: couleur à vérifier
    :return: la list est vide il n’y a aucune série de 4 pions alignés horizontalement, sinon une liste de pions de la couleur donnée en paramètre qui sont alignés par 4
    """
    if type_plateau(p) == False:
        raise TypeError("detecter4horizontalPlateau : Le premier paramètre ne correspond pas à un plateau")

    if type(col) != int:
        raise TypeError("detecter4horizontalPlateau : le second paramètre n’est pas un entier")

    if col not in const.COULEURS:
        raise ValueError(f"détecter4horizontalPlateau : La valeur de la couleur {col} n’est pas correcte")

    lst = []
    for l in range(const.NB_LINES):
        c = 0
        a = 0
        while a < 4 and c < const.NB_COLUMNS:
            if p[l][c] == None:
                a = 0
            elif p[l][c][const.COULEUR] == col:
                a+= 1
            else:
                a = 0
            c += 1

        if a >= 4:
            for i in range(c-a, c):
                lst.append(p[l][i])
    return lst

def detecter4verticalPlateau(p:list, col:int)->list:
    """
    Détecte s'il y a 4 pions alignés verticalements

    :param p: plateau à vérifier
    :param col: couleur à vérifier
    :return: la list est vide il n’y a aucune série de 4 pions alignés verticalement, sinon une liste de pions de la couleur donnée en paramètre qui sont alignés par 4
    """

    if type_plateau(p) == False:
        raise TypeError("detecter4verticalPlateau : Le premier paramètre ne correspond pas à un plateau")

    if type(col) != int:
        raise TypeError("detecter4verticalPlateau : le second paramètre n’est pas un entier")

    if col not in const.COULEURS:
        raise ValueError(f"detecter4verticalPlateau : La valeur de la couleur {col} n’est pas correcte")

    lst = []

    for c in range(const.NB_COLUMNS):
        l = 0
        a = 0
        while l < const.NB_LINES and a < 4:
            if p[l][c] == None:
                a = 0
            elif p[l][c][const.COULEUR] == col:
                a+= 1
            else:
                a = 0
            l += 1

        if a >= 4:
            for i in range(l-a, l):
                lst.append(p[i][c])
    return lst

def detecter4diagonaleDirectePlateau(p:dict, col:int)->list:
    """
    Détecte s'il y a 4 pions alignés en diagonale Directe

    :param p: plateau à vérifier
    :param col: couleur à vérifier
    :return: la list est vide il n’y a aucune série de 4 pions alignés en diagonale Directe, sinon une liste de pions de la couleur donnée en paramètre qui sont alignés par 4
    """

    if type_plateau(p) == False:
        raise TypeError("detecter4diagonaleDirectePlateau : Le premier paramètre ne correspond pas à un plateau")

    if type(col) != int:
        raise TypeError("detecter4diagonaleDirectePlateau : le second paramètre n’est pas un entier")

    if col not in const.COULEURS:
        raise ValueError(f"detecter4diagonaleDirectePlateau : La valeur de la couleur {col} n’est pas correcte")

    lst = []
    for diago in range(1, 4):
        #print()
        loc = 0
        a = 0
        while loc < const.NB_LINES - (diago-1) and a < 4:

            if p[loc][loc+diago] == None:
                a = 0
            elif p[loc][loc + diago][const.COULEUR] == col:
                a += 1
            else:
                a = 0
            #print(loc, loc + diago, a)
            loc+=1

        if a >= 4:
            for i in range(loc-a, loc):
                lst.append(p[i][i + diago])

    for diago in range(0, 3):
        #print()
        loc = 0
        a = 0
        while loc < const.NB_LINES - diago and a < 4:

            if p[loc + diago][loc] == None:
                a = 0
            elif p[loc + diago][loc][const.COULEUR] == col:
                a += 1
            else:
                a = 0
            #print(loc + diago, loc, a)
            loc += 1

        if a >= 4:
            for i in range(loc-a, loc):
                lst.append(p[i+diago][i])
    return lst

def detecter4diagonaleIndirectePlateau(p:dict, col:int)->list:
    """
    Détecte s'il y a 4 pions alignés en diagonale Indirecte

    :param p: plateau à vérifier
    :param col: couleur à vérifier
    :return: la list est vide il n’y a aucune série de 4 pions alignés en diagonale Indirecte, sinon une liste de pions de la couleur donnée en paramètre qui sont alignés par 4
    """

    if type_plateau(p) == False:
        raise TypeError("detecter4diagonaleIndirectePlateau : Le premier paramètre ne correspond pas à un plateau")

    if type(col) != int:
        raise TypeError("detecter4diagonaleIndirectePlateau : le second paramètre n’est pas un entier")

    if col not in const.COULEURS:
        raise ValueError(f"detecter4diagonaleIndirectePlateau : La valeur de la couleur {col} n’est pas correcte")

    lst = []
    for diago in range(1, 4):
        #print()
        loc = 0
        a = 0
        while loc < const.NB_LINES - (diago-1) and a < 4:

            if p[const.NB_LINES-loc-1][loc+diago] == None:
                a = 0
            elif p[const.NB_LINES-loc-1][loc + diago][const.COULEUR] == col:
                a += 1
            else:
                a = 0
            #print((const.NB_LINES-loc-1), loc + diago, a)
            loc+=1

        if a >= 4:
            for i in range(loc-a, loc):
                lst.append(p[(const.NB_LINES-1)-i][i + diago])

    for diago in range(0, 3):
        #print()
        loc = 0
        a = 0
        while loc < const.NB_LINES - diago and a < 4:

            if p[const.NB_LINES-loc-1 - diago][loc] == None:
                a = 0
            elif p[const.NB_LINES-loc-1 - diago][loc][const.COULEUR] == col:
                a += 1
            else:
                a = 0
            #print(const.NB_LINES-loc-1 - diago, loc, a)
            loc += 1

        if a >= 4:
            for i in range(loc-a, loc):
                lst.append(p[const.NB_LINES-i-1-diago][i])
    return lst

def getPionsGagnantsPlateau(p:dict)->list:
    """
    recherche les pions alignés pour les deux couleurs

    :param p: plateau où la recherche est faite
    :return: liste de toutes les séries de 4 pions alignés trouvées
    """
    if type_plateau(p) == False:
        raise TypeError("getPionsGagnantsPlateau : Le paramètre n’est pas un plateau")

    lst = []
    lst += detecter4horizontalPlateau(p, const.ROUGE) + detecter4verticalPlateau(p, const.ROUGE) + detecter4diagonaleDirectePlateau(p, const.ROUGE) + detecter4diagonaleIndirectePlateau(p, const.ROUGE)
    lst += detecter4horizontalPlateau(p, const.JAUNE) + detecter4verticalPlateau(p, const.JAUNE) + detecter4diagonaleDirectePlateau(p, const.JAUNE) + detecter4diagonaleIndirectePlateau(p, const.JAUNE)
    return lst

def placerPionLignePlateau(p:list, pion:dict, nbL:int, left:bool)->tuple:
    """
    Place le pion sur la ligne indiquée par la gauche si le booléen left vaut True ou par la droite sinon, en poussant les éventuels pions existants sur la ligne

    :param p: un plateau (liste)
    :param pion: un pion (dictionnaire)
    :param nbL: un numéro de ligne (entre 0 et 5)
    :param left: True si le pion est poussé par la gauche, False s’il est poussé par la droite du plateau
    :return: un tuple constitué de la liste des pions poussés (commençant par le pion ajouté) et un entier correspondant au numéro de ligne où se retrouve le dernier pion de la liste ou None si le dernier pion ne change pas de ligne
    """

    if type_plateau(p) == False:
        raise TypeError("placerPionLignePlateau : Le premier paramètre n’est pas un plateau")

    if type_pion(pion) == False:
        raise TypeError("placerPionLignePlateau : Le deuxième paramètre n’est pas un pion")

    if type(nbL) != int:
        raise TypeError("placerPionLignePlateau : Le troisième paramètre n’est pas un entier")

    if nbL < 0 and nbL > const.NB_LINES - 1:
        raise ValueError(f"placerPionLignePlateau : Le troisième paramètre {nbL} ne désigne pas une ligne")

    if type(left) != bool:
        raise TypeError("placerPionLignePlateau : le quatrième paramètre n’est pas un booléen")

    lst = []
    i = None
    if left:
        c = 0
        temp = pion
        while c <= const.NB_COLUMNS and temp != None:
            if c < const.NB_COLUMNS:
                temp2 = p[nbL][c]
                p[nbL][c] = temp
            else:
                i = const.NB_LINES

            lst.append(temp)
            temp = temp2

            c += 1
        c -= 1
    else:
        c = const.NB_COLUMNS-1
        temp = pion
        while c >= -1 and temp != None:
            if c > -1:
                temp2 = p[nbL][c]
                p[nbL][c] = temp
            else:
                i = const.NB_LINES

            lst.append(temp)
            temp = temp2

            c -= 1
        c += 1

    if temp==None:
        i = nbL
        while i < const.NB_LINES - 1 and p[i + 1][c] == None:
            i += 1

        if i != nbL:
            p[i][c] = p[nbL][c]
            p[nbL][c] = None
        else:
            i = None

    return (lst, i)

def encoderPlateau(p:dict)->str:
    """
    Encode le tableau sous cette forme:
        -Une case contenant None sera représentée par le caractère « souligné » "_".
        -Une case contenant un pion rouge sera représentée par le caractère "R".
        -Une case contenant un pion jaune sera représentée par le caractère "J".

    :param p: un plateau
    :return: une chaîne de caractères correspondant à l’encodage
    """

    enc = ""
    for l in range(const.NB_LINES):
        for c in range(const.NB_COLUMNS):
            if p[l][c] == None:
                enc += "_"
            elif getCouleurPion(p[l][c]) == const.ROUGE:
                enc += "R"
            else:
                enc += "J"
    return enc



