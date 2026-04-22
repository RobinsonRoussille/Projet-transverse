import random
import pygame
from plateforme import Plateforme, Liane

class NiveauBoue:
    def __init__(self, debut_boue, fin_boue, ground_y):
        self.debut_boue = debut_boue
        self.fin_boue = fin_boue
        self.ground_y = ground_y
        self.elements = []  # Contiendra plateformes ET lianes
        self.generer_zone_boue()

    def generer_zone_boue(self):
        x = self.debut_boue + 100
        while x < self.fin_boue - 100:
            choix = random.choice(["PLATEFORME", "LIANE"])

            if choix == "PLATEFORME":
                largeur = random.randint(100, 200)
                # On place la plateforme en hauteur
                y = self.ground_y - random.randint(60, 120)
                self.elements.append(Plateforme(x, y, largeur))
                x += largeur + random.randint(100, 200)

            else:  # LIANE
                # Les lianes pendent du "ciel" (y=0 ou y=50)
                longueur = random.randint(200, 300)
                self.elements.append(Liane(x, 50, longueur))
                x += random.randint(150, 200)

    def update(self):
        for e in self.elements:
            if isinstance(e, Liane):
                e.update()

    def draw(self, screen, camera_x):
        for e in self.elements:
            e.draw(screen, camera_x)