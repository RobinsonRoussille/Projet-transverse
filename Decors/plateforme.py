import pygame

class Plateforme:
    def __init__(self, x, y, largeur):
        # On fixe la hauteur à 20 directement ici
        self.rect = pygame.Rect(x, y, largeur, 20)
        self.couleur = (100, 60, 30)

    def draw(self, screen, camera_x):
        affichage_rect = self.rect.copy()
        affichage_rect.x -= camera_x
        pygame.draw.rect(screen, self.couleur, affichage_rect)