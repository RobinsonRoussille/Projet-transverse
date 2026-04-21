import pygame


class MereSanglier:
    def __init__(self, x, y_sol):
        # On charge les deux images
        self.img1 = pygame.transform.scale(pygame.image.load("images/marcassin/mere.png").convert_alpha(), (120, 85))
        self.img2 = pygame.transform.scale(pygame.image.load("images/marcassin/mere1.png").convert_alpha(), (120, 85))
        self.idle = pygame.transform.scale(pygame.image.load("images/marcassin/mere2.png").convert_alpha(), (120, 85))
        # On garde un rect pour la logique (indispensable pour le petit_marcassin.update)
        self.rect = self.img1.get_rect()
        self.rect.x = x
        self.rect.bottom = y_sol

        # Compteur pour l'alternance
        self.timer = 0

    def draw(self, surface, camera_x, etat):
        self.timer += 0.05
        if etat == "RETURN_TO_MOTHER":
            image_mere = self.img1 if int(self.timer) % 2 == 0 else self.img2
        else:
            image_mere = self.idle

        surface.blit(image_mere, (self.rect.x - camera_x, self.rect.y))