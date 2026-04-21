import pygame
import math


class Mouette:
    def __init__(self, x, y_sol):
        self.largeur = 60
        self.hauteur = 60
        # --- CHARGEMENT DES ANIMATIONS ---
        self.animations = {
            "REPOS": self.charger_images(["repos1.png", "repos2.png"]),
            "FUITE": self.charger_images(["vole_fuite1.png", "vole_fuite2.png"]),
            "CONTENT": self.charger_images(["vole_content1.png", "vole_content2.png"])
        }

        self.index_anim = 0
        self.vitesse_anim = 0.1
        self.image = self.animations["REPOS"][0]

        self.rect = self.image.get_rect(midbottom=(x, y_sol))
        self.y_sol = y_sol
        self.vitesse_fuite_x = 7
        self.etat = "AU_SOL"
        self.direction_x = 0

        self.timer_saut = 0
        self.duree_saut = 45
        self.apogee_saut = 130

        self.compteur_sauts = 0
        self.max_sauts = 20
        self.afficher_bulle = False
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

    def charger_images(self, noms):
        """Charge, redimensionne et flip initialement si nécessaire."""
        images = []
        for nom in noms:
            img = pygame.image.load(f"images/mouette/{nom}").convert_alpha()
            img = pygame.transform.scale(img, (self.largeur, self.hauteur))
            img = pygame.transform.flip(img, True, False)
            # On part du principe que tes images de base regardent vers la DROITE
            images.append(img)
        return images

    def animer(self, type_anim, force_direction=None):
        """Gère l'animation et le sens du regard."""
        self.index_anim += self.vitesse_anim
        if self.index_anim >= len(self.animations[type_anim]):
            self.index_anim = 0

        img = self.animations[type_anim][int(self.index_anim)]

        # Déterminer la direction : soit imposée (cercle), soit naturelle (vol)
        direction = force_direction if force_direction is not None else self.direction_x

        # Si la direction est négative, on flip l'image pour regarder à gauche
        if direction < 0:
            self.image = pygame.transform.flip(img, True, False)
        else:
            self.image = img

    def update(self, joueur_x, joueur_court, touche_caresse):
        if self.etat == "DISPARUE": return

        dist_joueur = abs(self.rect.centerx - joueur_x)
        self.afficher_bulle = False

        if self.etat == "AU_SOL":
            self.animer("REPOS", force_direction=1)  # Regarde à droite par défaut
            if joueur_court and dist_joueur < 280:
                self.compteur_sauts += 1
                if self.compteur_sauts >= self.max_sauts:
                    self.etat = "S_ENVOLE"
                    return
                self.etat = "EN_VOL"
                self.timer_saut = 0
                self.direction_x = 1 if self.rect.centerx > joueur_x else -1

            elif dist_joueur <= 70:
                self.afficher_bulle = True
                if touche_caresse:
                    self.etat = "CARESSEE"
                    self.timer_saut = 0

        elif self.etat == "EN_VOL":
            self.animer("FUITE")
            self.timer_saut += 1
            prog = self.timer_saut / self.duree_saut
            hauteur = self.apogee_saut * (math.sin(math.pi * prog) ** 2)
            self.rect.bottom = self.y_sol - hauteur
            self.rect.x += self.direction_x * self.vitesse_fuite_x

            if self.timer_saut >= self.duree_saut:
                self.etat = "AU_SOL"
                self.rect.bottom = self.y_sol

        elif self.etat == "CARESSEE":
            self.timer_saut += 1
            angle = self.timer_saut * 0.05

            # Calcul du sens du regard sur le cercle (dérivée du cosinus)
            vitesse_x_visuelle = -math.sin(angle)
            self.animer("CONTENT", force_direction=vitesse_x_visuelle)

            cible_x = joueur_x
            cible_y = self.y_sol - 250
            rayon_x, rayon_y = 250, 100

            position_ideale_x = cible_x + math.cos(angle) * rayon_x
            position_ideale_y = cible_y + math.sin(angle) * rayon_y

            self.rect.centerx += (position_ideale_x - self.rect.centerx) * 0.05
            self.rect.centery += (position_ideale_y - self.rect.centery) * 0.05

            if self.timer_saut >= 400:
                self.etat = "S_ENVOLE"

        elif self.etat == "S_ENVOLE":
            # Regarde vers la droite pendant qu'elle s'enfuit
            self.animer("FUITE", force_direction=1)
            self.rect.y -= 8
            self.rect.x += 4
            if self.rect.bottom < -100: self.etat = "DISPARUE"

    def draw(self, surface, camera_x):
        if self.etat == "DISPARUE": return
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

        if self.afficher_bulle:
            txt = self.font.render("E", True, (0, 0, 0))
            surface.blit(txt, (self.rect.centerx - camera_x - 5, self.rect.y - 25))