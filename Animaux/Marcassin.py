# librairie
import pygame

pygame.init()

# variables
LARGEUR = 1000
HAUTEUR = 750

# création fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Marcassin")


# class
class Marcassin:
    def __init__(self):
        self.m_largeur = 40
        self.m_hauteur = 40
        self.m_x = LARGEUR // 2 - self.m_largeur // 2
        sol_y = HAUTEUR - 15
        self.m_y = sol_y - self.m_hauteur
        self.nourri = False
        self.etat = "peur"

    def afficher(self, surface):
        pygame.draw.rect(surface, (139, 69, 19),
                         (self.m_x, self.m_y, self.m_largeur, self.m_hauteur))

    def mouvement_animal(self):
        pass

    def etat_joie(self,joueur):
        if joueur
        pass

    def etat_colere(self):
        pass

    def etat_peur(self,joueur):
        if joueur.x < self.x:
            self.x += 3
        else:
            self.x -= 3

    def etat_amour(self,joueur):
       """ def follow(target (joueur), follower(self), speed):"""
        if joueur.x > self.x:
            self.x += min(joueur.x - self.x)
        elif joueur.x < self.x:
            self.x -= min(self.x - joueur.x)

    def update(self, joueur):

        if self.etat == "peur":
            self.etat_peur(joueur)
        elif self.etat == "amour":
            self.etat_amour(joueur)

class Joueur:
    def __init__(self):
        self.m_largeur = 40
        self.m_hauteur = 40
        self.m_x = LARGEUR // 2 - self.m_largeur // 2
        sol_y = HAUTEUR - 15
        self.m_y = sol_y - self.m_hauteur
        sol_y = HAUTEUR - 60
        self.y = sol_y - self._hauteur

        self.vitesse = 2
        self.vitesse_y = 5
        self.gravite = 0.81
        self.force_saut = -13
        self.au_sol = True


# main
if __name__ == "__main__":
    joueur = Joueur()
    marcassin = Marcassin()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fenetre.fill((135, 206, 235))  # fond bleu
        marcassin.afficher(fenetre)

        pygame.display.flip()

    pygame.quit()
