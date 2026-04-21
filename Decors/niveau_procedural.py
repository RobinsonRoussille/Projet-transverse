import random
from .plateforme import Plateforme

class NiveauProcedural:
    def __init__(self, screen_width, ground_y):
        self.screen_width = screen_width
        self.ground_y = ground_y
        self.plateformes = []
        self.dernier_x = 0  # Jusqu'où le niveau est généré

        # On génère un premier segment au départ
        self.generer_segment(0, screen_width * 2)

    def generer_segment(self, debut_x, fin_x):
        x = debut_x
        while x < fin_x:
            largeur = random.randint(200, 500)
            # Supprime ou commente la ligne hauteur_p = 40

            # Position Y : au sol (0), ou en l'air (100 ou 200)
            y = self.ground_y - random.choice([0, 100, 200])

            # ICI : Retire le 4ème argument (hauteur_p)
            self.plateformes.append(Plateforme(x, y, largeur))

            x += largeur + random.randint(50, 150)

        self.dernier_x = fin_x

    def update(self, camera_x):
        # Si la caméra approche de la fin de ce qu'on a généré, on en crée plus
        if camera_x + self.screen_width * 2 > self.dernier_x:
            self.generer_segment(self.dernier_x, self.dernier_x + self.screen_width)

        # Optionnel : Supprimer les plateformes loin derrière pour optimiser
        self.plateformes = [p for p in self.plateformes if p.rect.right > camera_x - 500]

    def draw(self, screen, camera_x):
        for p in self.plateformes:
            p.draw(screen, camera_x)