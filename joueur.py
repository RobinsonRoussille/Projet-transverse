import pygame

class Joueur:
    def __init__(self, x, y_sol):
        # Dimensions et apparence
        self.largeur = 50
        self.hauteur = 90
        self.couleur = (50, 80, 80)

        # Positionnement (le bas du rectangle touche le sol)
        self.rect = pygame.Rect(x - self.largeur // 2, y_sol - self.hauteur, self.largeur, self.hauteur)

        # Physique du saut
        self.vitesse_y = 0
        self.gravite = 0.8
        self.force_saut = -14
        self.au_sol = True
        self.y_sol = y_sol

    def sauter(self):
        if self.au_sol:
            self.vitesse_y = self.force_saut
            self.au_sol = False

    def update(self):
        # Appliquer la gravité
        self.vitesse_y += self.gravite
        self.rect.y += self.vitesse_y

        # Collision avec le sol (empêche de tomber à l'infini)
        if self.rect.y >= self.y_sol - self.hauteur:
            self.rect.y = self.y_sol - self.hauteur
            self.vitesse_y = 0
            self.au_sol = True

    def draw(self, surface):
        # Dessine le joueur sur la fenêtre passée en argument
        pygame.draw.rect(surface, self.couleur, self.rect)