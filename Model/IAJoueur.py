from Model.Joueur import *
from Model.Plateau import *
from Model.Pion import *
from Model.Constantes import *
from random import randint, choice
from Model.Joueur import *

def _placerPionJoueur2(j:dict)->int:
    """
    Donne une colonne où un pion peut être dans une colonne disponible de façon intelligent

    :param j: représente un joueur
    :return: un entier représentant la colonne
    """

    nb = 0
    p = getPlateauJoueur(j)

    colAdv = const.ROUGE
    col = getCouleurJoueur(j)
    if col == const.ROUGE:
        colAdv = const.JAUNE

    if getModeEtenduJoueur(j) == False:
        # return = 0, const.NB_COLUMNS - 1
        nb = random.randint(0, const.NB_COLUMNS - 1)
        while p[0][nb] != None:
            nb = random.randint(0, const.NB_COLUMNS - 1)

        for i in range(4):
            pos = []
            if i == 0:
                pos += PropositionPos(p, col, 3)
            elif i == 1:
                pos += PropositionPos(p, colAdv, 3)
            elif i == 2:
                pos += PropositionPos(p, colAdv, 2)
            else:
                pos += PropositionPos(p, col, 2)

            if len(pos) > 0:
                # choisi aléatoirement une position qui fait gagné
                nb = pos[random.randint(0, len(pos)-1)][1]
    else:
        nb = random.randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES - 1)

        if nb >= 0 and nb < const.NB_COLUMNS:
            while p[0][nb] != None:
                nb = random.randint(-const.NB_LINES, const.NB_COLUMNS + const.NB_LINES - 1)

    return nb

def PropositionPos(p:list, col:int, n:int)->list:
    """
    propose des positions de pion pour poser des pions autour de l'alignement de n pion cela
    peut permettre soit d'empêcher l'adversaire de gagné soit gagné

    :param p: plateau
    :param col: couleur du joueur ia
    :param n: n pion alignée
    :return: une liste de position possible
    """

    # position possible  => (position pion possible = [ligne, colonne])
    pos = []
    n = 3

    lst = detecterNhorizontalPlateau(p, col, n)
    #print(lst)
    if len(lst) > 0:
        for i in range(0, len(lst) - n, n):
            pos.append(getPosPion(lst[i], p))
            pos[len(pos) - 1][1] += 1
        for i in range(n, len(lst), n):
            pos.append(getPosPion(lst[i], p))
            pos[len(pos) - 1][1] -= 1

    lst = detecterNverticalPlateau(p, col, n)
    #print(lst, len(lst))
    if len(lst) > 0:
        for i in range(0, len(lst)-2, n):
            pos.append(getPosPion(lst[i], p))
            pos[len(pos) - 1][0] -= 1

    lst = detecterNdiagonaleDirectePlateau(p, col, n)
    #print(lst)
    for i in range(0, len(lst) - n, n):
        pos.append(getPosPion(lst[i], p))
        pos[len(pos) - 1][1] += 1
        pos[len(pos) - 1][0] += 1
    for i in range(n, len(lst), n):
        pos.append(getPosPion(lst[i], p))
        pos[len(pos) - 1][1] -= 1
        pos[len(pos) - 1][0] -= 1

    lst = detecterNdiagonaleIndirectePlateau(p, col, n)
    #print(lst)
    for i in range(0, len(lst) - n, n):
        pos.append(getPosPion(lst[i], p))
        pos[len(pos) - 1][1] += 1
        pos[len(pos) - 1][0] -= 1
    for i in range(n, len(lst), n):
        pos.append(getPosPion(lst[i], p))
        pos[len(pos) - 1][1] -= 1
        pos[len(pos) - 1][0] += 1

    #print(pos)

    for i in range(len(pos)):
        if pos[i][0] > const.NB_LINES or pos[i][0] < 0 or pos[i][1] > const.NB_COLUMNS or pos[i][1] < 0 or p[pos[i][0]][pos[i][1]] != None:
            del (pos[i])

    #print(pos)
    #print()
    return pos

def getPosPion(pion:dict, p:list)->list:
    """
    Recherche la position d'un pion dans un plateau

    :param pion: le pion recherché
    :param p: le plateu où se trouve le pion
    :return: une liste où il est stocké la ligne du pion puis sa colonne, si il n'existe pas les deux valeurs de la liste sera à -1
    """

    if type_pion(pion) == False:
        raise TypeError("getPosPion : Le premier paramètre ne correspond pas à un pion")

    if type_plateau(p) == False:
        raise TypeError("getPosPion : Le second paramètre ne correspond pas à un plateau")

    l = 0
    c = 0
    trouvee = False
    while l < len(p) and trouvee == False:
        c = 0
        while c < len(p[l]) and trouvee == False:
            trouvee = p[l][c] == pion
            c+=1
        l+=1

    c-= 1
    l-=1

    if trouvee == False:
        c = -1
        l = -1

    return [l, c]

def detecterNhorizontalPlateau(p:list, col:int, n:int)->list:
    """
    Détecte s'il y a 4 pions alignés horizontalements

    :param p: plateau à vérifier
    :param col: couleur à vérifier
    :param n: nombre de pion alignée è retrouver
    :return: la list est vide il n’y a aucune série de 4 pions alignés horizontalement, sinon une liste de pions de la couleur donnée en paramètre qui sont alignés par 4
    """
    if type_plateau(p) == False:
        raise TypeError("detecterNhorizontalPlateau : Le premier paramètre ne correspond pas à un plateau")

    if type(col) != int:
        raise TypeError("detecterNhorizontalPlateau : le second paramètre n’est pas un entier")

    if col not in const.COULEURS:
        raise ValueError(f"detecterNhorizontalPlateau : La valeur de la couleur {col} n’est pas correcte")

    if type(n) != int:
        raise TypeError("detecterNhorizontalPlateau : le troisième paramètre n’est pas un entier")

    lst = []
    for l in range(const.NB_LINES):
        c = 0
        a = 0
        while a < n and c < const.NB_COLUMNS:
            if p[l][c] == None:
                a = 0
            elif getCouleurPion(p[l][c]) == col:
                a+= 1
            else:
                a = 0
            c += 1

        if a >= n:
            for i in range(c-a, c):
                lst.append(p[l][i])
    return lst

def detecterNverticalPlateau(p:list, col:int, n:int)->list:
    """
    Détecte s'il y a 4 pions alignés verticalements

    :param p: plateau à vérifier
    :param col: couleur à vérifier
    :param n: nombre de pion alignée è retrouver
    :return: la list est vide il n’y a aucune série de 4 pions alignés verticalement, sinon une liste de pions de la couleur donnée en paramètre qui sont alignés par 4
    """

    if type_plateau(p) == False:
        raise TypeError("detecterNverticalPlateau : Le premier paramètre ne correspond pas à un plateau")

    if type(col) != int:
        raise TypeError("detecterNverticalPlateau : le second paramètre n’est pas un entier")

    if col not in const.COULEURS:
        raise ValueError(f"detecterNverticalPlateau : La valeur de la couleur {col} n’est pas correcte")

    if type(n) != int:
        raise TypeError("detecterNverticalPlateau : le troisième paramètre n’est pas un entier")

    lst = []

    for c in range(const.NB_COLUMNS):
        l = 0
        a = 0
        while l < const.NB_LINES and a < n:
            if p[l][c] == None:
                a = 0
            elif getCouleurPion(p[l][c]) == col:
                a+= 1
            else:
                a = 0
            l += 1

        if a >= n:
            for i in range(l-a, l):
                lst.append(p[i][c])
    return lst

def detecterNdiagonaleDirectePlateau(p:list, col:int, n:int)->list:
    """
    Détecte s'il y a 4 pions alignés en diagonale Directe

    :param p: plateau à vérifier
    :param col: couleur à vérifier
    :param n: nombre de pion alignée è retrouver
    :return: la list est vide il n’y a aucune série de 4 pions alignés en diagonale Directe, sinon une liste de pions de la couleur donnée en paramètre qui sont alignés par 4
    """

    if type_plateau(p) == False:
        raise TypeError("detecterNdiagonaleDirectePlateau : Le premier paramètre ne correspond pas à un plateau")

    if type(col) != int:
        raise TypeError("detecterNdiagonaleDirectePlateau : le second paramètre n’est pas un entier")

    if col not in const.COULEURS:
        raise ValueError(f"detecterNdiagonaleDirectePlateau : La valeur de la couleur {col} n’est pas correcte")

    if type(n) != int:
        raise TypeError("detecterNdiagonaleDirectePlateau : le troisième paramètre n’est pas un entier")

    lst = []
    for diago in range(1, 4):
        #print()
        loc = 0
        a = 0
        while loc < const.NB_LINES - (diago-1) and a < n:

            if p[loc][loc+diago] == None:
                a = 0
            elif getCouleurPion(p[loc][loc + diago]) == col:
                a += 1
            else:
                a = 0
            #print(loc, loc + diago, a)
            loc+=1

        if a >= n:
            for i in range(loc-a, loc):
                lst.append(p[i][i + diago])

    for diago in range(0, 3):
        #print()
        loc = 0
        a = 0
        while loc < const.NB_LINES - diago and a < n:

            if p[loc + diago][loc] == None:
                a = 0
            elif getCouleurPion(p[loc + diago][loc]) == col:
                a += 1
            else:
                a = 0
            #print(loc + diago, loc, a)
            loc += 1

        if a >= n:
            for i in range(loc-a, loc):
                lst.append(p[i+diago][i])
    return lst

def detecterNdiagonaleIndirectePlateau(p:list, col:int, n:int)->list:
    """
    Détecte s'il y a 4 pions alignés en diagonale Indirecte

    :param p: plateau à vérifier
    :param col: couleur à vérifier
    :param n: nombre de pion alignée è retrouver
    :return: la list est vide il n’y a aucune série de 4 pions alignés en diagonale Indirecte, sinon une liste de pions de la couleur donnée en paramètre qui sont alignés par 4
    """

    if type_plateau(p) == False:
        raise TypeError("detecterNdiagonaleIndirectePlateau : Le premier paramètre ne correspond pas à un plateau")

    if type(col) != int:
        raise TypeError("detecterNdiagonaleIndirectePlateau : le second paramètre n’est pas un entier")

    if col not in const.COULEURS:
        raise ValueError(f"detecterNdiagonaleIndirectePlateau : La valeur de la couleur {col} n’est pas correcte")

    if type(n) != int:
        raise TypeError("detecterNdiagonaleIndirectePlateau : le troisième paramètre n’est pas un entier")

    lst = []
    for diago in range(1, 4):
        #print()
        loc = 0
        a = 0
        while loc < const.NB_LINES - (diago-1) and a < n:

            if p[const.NB_LINES-loc-1][loc+diago] == None:
                a = 0
            elif getCouleurPion(p[const.NB_LINES-loc-1][loc + diago]) == col:
                a += 1
            else:
                a = 0
            #print((const.NB_LINES-loc-1), loc + diago, a)
            loc+=1

        if a >= n:
            for i in range(loc-a, loc):
                lst.append(p[(const.NB_LINES-1)-i][i + diago])

    for diago in range(0, 3):
        #print()
        loc = 0
        a = 0
        while loc < const.NB_LINES - diago and a < n:

            if p[const.NB_LINES-loc-1 - diago][loc] == None:
                a = 0
            elif getCouleurPion(p[const.NB_LINES-loc-1 - diago][loc]) == col:
                a += 1
            else:
                a = 0
            #print(const.NB_LINES-loc-1 - diago, loc, a)
            loc += 1

        if a >= n:
            for i in range(loc-a, loc):
                lst.append(p[const.NB_LINES-i-1-diago][i])
    return lst