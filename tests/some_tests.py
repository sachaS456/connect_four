from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from random import randint, choice

p = construirePlateau()
for _ in range(35):
    placerPionPlateau(p, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
print(toStringPlateau(p))

print(detecter4diagonaleIndirectePlateau(p, const.ROUGE))
print(detecter4diagonaleIndirectePlateau(p, const.JAUNE))