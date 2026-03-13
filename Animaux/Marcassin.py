# librairie
import pygame

pygame.init()


# variables
# class
class Marcassin:
    def __init__(self):
        # fenêtre de l'animal marcassin
        LARGEUR, HAUTEUR = 918, 648
        fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Scrolling background + parallax")

        clock = pygame.time.Clock()
        FPS = 60
        m_largeur = 40
        m_hauteur = 40
        m_x = LARGEUR // 2 - m_largeur // 2
        sol_y = HAUTEUR - 15
        m_y = sol_y - m_hauteur

    def etat_joie(self):
        pass

    def etat_colere(self):
        pass

    def etat_peur(self):
        pass

    def etat_amour(self):
        pass


# fonction


# main
""""if __name__=="__main__":"""""
