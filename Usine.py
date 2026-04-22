import pygame

class Usine:
    def __init__(self, y_sol, fin = 0):
        try:
            # On charge ton image usine.png
            self.image = pygame.image.load("usine.png").convert_alpha()
            # On adapte la taille pour qu'elle soit imposante
            self.image = pygame.transform.scale(self.image, (800, 800))
        except:
            # Sécurité si le fichier est manquant
            self.image = pygame.Surface((600, 700))
            self.image.fill((50, 50, 55))

        self.rect = self.image.get_rect()
        # Positionnée à l'extrême gauche
        # On laisse 150px de l'image dépasser dans le monde pour le visuel
        self.rect.x = -self.rect.width + 400 + fin
        self.rect.bottom = y_sol + 80

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))