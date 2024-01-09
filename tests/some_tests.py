from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from random import randint, choice

p = construirePlateau()
for _ in range(20):
    placerPionPlateau(p, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
print(toStringPlateau(p))

print(detecter4verticalPlateau(p, const.ROUGE))
print(detecter4verticalPlateau(p, const.JAUNE))