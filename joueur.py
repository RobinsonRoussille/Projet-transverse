import pygame


class Joueur:
    def __init__(self, x, y_sol):
        self.largeur = 62
        self.hauteur = 90
        self.rect = pygame.Rect(x - self.largeur // 2, y_sol - self.hauteur, self.largeur, self.hauteur)

        # --- CHARGEMENT DES IMAGES ---
        def load_img(name):
            img = pygame.image.load(f"images/joueur/{name}.png").convert_alpha()
            return pygame.transform.scale(img, (self.largeur, self.hauteur))

        self.img_idle = load_img("idle")
        self.anim_marche = [load_img("marche1"), load_img("marche2")]
        self.anim_course = [load_img("cours1"), load_img("cours2")]
        self.img_corde = load_img("corde")

        # --- VARIABLES D'ANIMATION ---
        self.image_actuelle = self.img_idle
        self.index_anim = 0
        self.compteur_anim = 0
        self.direction_droite = True

        self.couleur_marche = (50, 80, 80)
        self.couleur_course = (80, 120, 120)
        self.couleur = self.couleur_marche

        self.vitesse_marche = 2
        self.vitesse_course = 5
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
        self.vitesse_enfoncement = 10

    def sauter(self):
        if self.au_sol and not self.dans_la_boue:
            self.vitesse_y = self.force_saut
            self.au_sol = False

    def update(self, veut_courir, en_train_de_pousser=False):
        # Détection de la direction pour l'image
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_RIGHT]:
            self.direction_droite = True
            moving = True
        elif keys[pygame.K_LEFT]:
            self.direction_droite = False
            moving = True

        # 1. GESTION DES VITESSES ET ANIMATIONS
        if veut_courir:
            self.vitesse_actuelle = self.vitesse_course
            self.couleur = self.couleur_course
            liste_images = self.anim_course
        else:
            self.vitesse_actuelle = self.vitesse_marche
            self.couleur = self.couleur_marche
            liste_images = self.anim_marche

        if en_train_de_pousser:
            self.vitesse_actuelle = 1

        # Sélection de l'image
        if self.liane_actuelle:
            self.image_actuelle = self.img_corde
        elif not moving or not self.au_sol:
            self.image_actuelle = self.img_idle
        else:
            # Cycle d'animation
            self.compteur_anim += 1
            vitesse_anim = 10 if veut_courir else 15
            if self.compteur_anim >= vitesse_anim:
                self.index_anim = (self.index_anim + 1) % len(liste_images)
                self.compteur_anim = 0
            self.image_actuelle = liste_images[self.index_anim]

        # 2. PHYSIQUE
        if self.liane_actuelle:
            self.vitesse_y = 0
            self.au_sol = False
            self.rect.centerx = self.liane_actuelle.pos_bout[0]
            self.rect.top = self.liane_actuelle.pos_bout[1] - 10
        else:
            self.vitesse_y += self.gravite
            self.rect.y += self.vitesse_y

            if self.rect.y >= self.y_sol - self.hauteur:
                if not self.dans_la_boue:
                    self.rect.y = self.y_sol - self.hauteur
                    self.vitesse_y = 0
                    self.au_sol = True
                else:
                    self.vitesse_y = 0
                    self.au_sol = False

    def draw(self, surface, camera_x, debut, fin, debut_boue, fin_boue):
        # Gestion du miroir selon la direction
        img_finale = self.image_actuelle
        if not self.direction_droite:
            img_finale = pygame.transform.flip(self.image_actuelle, True, False)

        pos_affichage = self.rect.copy()
        pos_affichage.x -= camera_x

        # Dessin du personnage (image au lieu du rectangle)
        surface.blit(img_finale, pos_affichage)

        # Dessin des zones (optionnel si tu as des décors, sinon on les laisse)
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
            self.vitesse_course = 5
            self.force_saut = -16

    def s_enfoncer(self):
        if self.rect.y >= self.y_sol - self.hauteur:
            self.dans_la_boue = True
            self.vitesse_course = 0.5
            self.vitesse_marche = 0.5
            self.couleur = (60, 40, 20)

            self.compteur_boue += 1
            if self.compteur_boue >= self.vitesse_enfoncement:
                self.rect.y += 1
                self.compteur_boue = 0

    def reset_position(self, x_destination):
        self.rect.x = x_destination
        self.rect.y = 400 - self.hauteur
        self.vitesse_y = 0
        self.vitesse_course = 5
        self.vitesse_marche = 2
        self.au_sol = True
        self.dans_la_boue = False
        self.compteur_boue = 0