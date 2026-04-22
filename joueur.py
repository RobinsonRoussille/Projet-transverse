import pygame


class Joueur:
    def __init__(self, x, y_sol):
        self.largeur = 50
        self.hauteur = 90
        self.couleur_marche = (50, 80, 80)
        self.couleur_course = (80, 120, 120)
        self.couleur = self.couleur_marche

        self.rect = pygame.Rect(x - self.largeur // 2, y_sol - self.hauteur, self.largeur, self.hauteur)

        self.vitesse_marche = 2
        self.vitesse_course = 4
        self.vitesse_actuelle = self.vitesse_marche

        self.vitesse_y = 0
        self.gravite = 0.8
        self.force_saut = -16
        self.au_sol = True
        self.y_sol = y_sol

        self.liane_actuelle = None

        # --- GESTION DE LA BOUE ---
        self.dans_la_boue = False
        self.compteur_boue = 0
        self.vitesse_enfoncement = 10  # 1 pixel toutes les 10 frames

    def sauter(self):
        # On ne peut sauter que si on est au sol et PAS déjà en train de couler
        if self.au_sol and not self.dans_la_boue:
            self.vitesse_y = self.force_saut
            self.au_sol = False

    def update(self, veut_courir, en_train_de_pousser=False):
        # 1. GESTION DES COULEURS ET VITESSES
        if veut_courir:
            self.vitesse_actuelle = self.vitesse_course
            self.couleur = self.couleur_course
        else:
            self.vitesse_actuelle = self.vitesse_marche
            self.couleur = self.couleur_marche

        if en_train_de_pousser:
            self.vitesse_actuelle = 1

        # 2. PHYSIQUE : SOIT LIANE, SOIT GRAVITÉ NORMALE
        if self.liane_actuelle:
            # On stoppe toute vitesse physique
            self.vitesse_y = 0
            self.au_sol = False

            # On colle le joueur à la liane
            self.rect.centerx = self.liane_actuelle.pos_bout[0]
            self.rect.top = self.liane_actuelle.pos_bout[1] - 10
        else:
            # PHYSIQUE NORMALE : seulement si on n'est PAS sur une liane
            self.vitesse_y += self.gravite
            self.rect.y += self.vitesse_y

            # Gestion du sol (collision classique)
            if self.rect.y >= self.y_sol - self.hauteur:
                if not self.dans_la_boue:
                    self.rect.y = self.y_sol - self.hauteur
                    self.vitesse_y = 0
                    self.au_sol = True
                else:
                    self.vitesse_y = 0
                    self.au_sol = False

    def draw(self, surface, camera_x, debut, fin, debut_boue, fin_boue):
        pos_affichage = self.rect.copy()
        pos_affichage.x -= camera_x
        pygame.draw.rect(surface, self.couleur, pos_affichage)

        # Dessin des zones
        pygame.draw.rect(surface, (0, 100, 200), (debut - camera_x, 400, (fin - debut) + self.largeur, 70))
        pygame.draw.rect(surface, (90, 70, 50),
                         (debut_boue - camera_x, 400, (fin_boue - debut_boue) + self.largeur, 200))

    def dansEau(self, etat, sur_plateforme):
        if sur_plateforme:
            etat = False
        if etat:
            self.y_sol = 470
            if self.rect.y >= self.y_sol - self.hauteur:
                self.vitesse_marche = 1
                self.vitesse_course = 1
                self.force_saut = -12
                self.couleur = (100, 150, 200)
        else:
            self.y_sol = 400
            self.vitesse_marche = 2
            self.vitesse_course = 4
            self.force_saut = -16

    def s_enfoncer(self):
        # Cette méthode est appelée par le MAIN quand on est dans la zone X de la boue
        # Mais on ne commence à couler que si on a touché le sol
        if self.rect.y >= self.y_sol - self.hauteur:
            self.dans_la_boue = True
            self.vitesse_course = 0.5
            self.vitesse_marche = 0.5
            self.couleur = (60, 40, 20)

            # Aspiration lente
            self.compteur_boue += 1
            if self.compteur_boue >= self.vitesse_enfoncement:
                self.rect.y += 1
                self.compteur_boue = 0

    def reset_position(self, x_destination):
        self.rect.x = x_destination
        self.rect.y = 400 - self.hauteur
        self.vitesse_y = 0
        self.vitesse_course = 4
        self.vitesse_marche = 2
        self.au_sol = True
        self.dans_la_boue = False
        self.compteur_boue = 0