import pygame


class Joueur:
    def __init__(self, x, y_sol):
        self.largeur = 50
        self.hauteur = 90
        self.couleur_marche = (50, 80, 80)
        self.couleur_course = (80, 120, 120)
        self.couleur = self.couleur_marche

        self.rect = pygame.Rect(x - self.largeur // 2, y_sol - self.hauteur, self.largeur, self.hauteur)

        self.vitesse_marche = 10
        self.vitesse_course = 3
        self.vitesse_actuelle = self.vitesse_marche

        self.vitesse_y = 0
        self.gravite = 0.8
        self.force_saut = -16
        self.au_sol = True
        self.y_sol = y_sol

    def sauter(self):
        if self.au_sol:
            self.vitesse_y = self.force_saut
            self.au_sol = False

    def update(self, veut_courir, en_train_de_pousser=False):
        if veut_courir:
            self.vitesse_actuelle = self.vitesse_course
            self.couleur = self.couleur_course
        else:
            self.vitesse_actuelle = self.vitesse_marche
            self.couleur = self.couleur_marche

        # Ralentissement extrême si on pousse le déchet lourd
        if en_train_de_pousser:
            self.vitesse_actuelle = 1

        self.vitesse_y += self.gravite
        self.rect.y += self.vitesse_y

        if self.rect.y >= self.y_sol - self.hauteur:
            self.rect.y = self.y_sol - self.hauteur
            self.vitesse_y = 0
            self.au_sol = True

    def draw(self, surface, camera_x):
        pos_affichage = self.rect.copy()
        pos_affichage.x -= camera_x
        pygame.draw.rect(surface, self.couleur, pos_affichage)

    def dansEau(self, etat, debut, fin, screen, camera, sur_plateforme):
        # Si on est sur une plateforme, on force l'état à False
        if sur_plateforme:
            etat = False

        if etat:
            self.y_sol = 470
            self.vitesse_marche = 1
            self.vitesse_course = 1
            self.force_saut = -12
            self.couleur = (100, 150, 200)  # Teinte bleutée dans l'eau
        else:
            self.y_sol = 400
            self.vitesse_marche = 10
            self.vitesse_course = 3
            self.force_saut = -16
            # On remet la couleur normale selon la course
            # (Géré dans update, mais on peut forcer ici aussi)

        # Dessin de l'eau
        pygame.draw.rect(screen, (0, 100, 200), (debut - camera, 400, (fin - debut) + self.largeur, 70))