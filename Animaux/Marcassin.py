import pygame
import random
import os


class Marcassin:
    def __init__(self, x, y_sol):
        self.chemin = os.path.join("images", "marcassin")

        self.images = {
            "WANDER": self.charger_images("peur1.png", "peur2.png"),
            "APPROACH": self.charger_images("peur1.png", "peur2.png"),
            "FLEE": self.charger_images("colere1.png", "colere2.png"),
            "FOLLOW": self.charger_images("coeur1.png", "coeur2.png"),
            "RETURN_TO_MOTHER": self.charger_images("coeur1.png", "coeur2.png")
        }

        self.image_actuelle = self.images["WANDER"][0]
        self.rect = self.image_actuelle.get_rect()
        self.rect.x = x
        self.rect.bottom = y_sol

        self.index_anim = 0
        self.vitesse_anim = 0.12

        self.start_x = x
        self.y_sol = y_sol
        self.vitesse_marche = 2
        self.vitesse_fuite = 5
        self.direction_wander = 0
        self.timer_ia = 0

        self.zone_detection = 350
        self.zone_caresse = 70
        self.timer_hesitation = 0

        self.etat = "WANDER"
        self.cote_suivi = 1
        self.flip = False
        self.afficher_bulle = False
        self.moving = False  # Nouveau : pour savoir si on anime ou pas
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.loin = False

    def charger_images(self, nom1, nom2):
        img1 = pygame.image.load(os.path.join(self.chemin, nom1)).convert_alpha()
        img2 = pygame.image.load(os.path.join(self.chemin, nom2)).convert_alpha()
        return [pygame.transform.scale(img1, (65, 45)), pygame.transform.scale(img2, (65, 45))]

    def update(self, joueur_x, joueur_en_mouvement, touche_caresse, keys, mere_rect):
        dist_joueur = abs(self.rect.centerx - joueur_x)
        self.afficher_bulle = False
        self.moving = False  # Par défaut, immobile

        if self.timer_hesitation > 0:
            self.timer_hesitation -= 1

        # --- 1. LOGIQUE DES ÉTATS ---
        if self.etat == "RETURN_TO_MOTHER":
            pass
        elif abs(self.start_x - self.rect.x) > 2000 and (self.etat != "FOLLOW" and self.etat != "RETURN_TO_MOTHER"):
            self.loin = True
        elif self.etat == "FOLLOW":
            if abs(self.rect.centerx - mere_rect.centerx) < 450:
                self.etat = "RETURN_TO_MOTHER"
        else:
            # Détection du danger
            if dist_joueur < self.zone_detection and joueur_en_mouvement:
                self.etat = "FLEE"
                self.timer_hesitation = 80  # Temps d'hésitation (un peu plus d'une seconde)

            # Retour au calme uniquement si le timer est fini
            elif self.timer_hesitation <= 0:
                if dist_joueur <= self.zone_caresse and not joueur_en_mouvement:
                    self.afficher_bulle = True
                    if touche_caresse: self.etat = "FOLLOW"
                elif dist_joueur < self.zone_detection and not joueur_en_mouvement:
                    self.etat = "APPROACH"
                else:
                    self.etat = "WANDER"

        # --- 2. MOUVEMENTS ET FLIP ---
        if self.etat == "WANDER":
            self.timer_ia -= 1
            if self.timer_ia <= 0:
                self.timer_ia = random.randint(60, 180)
                self.direction_wander = random.choice([-1, 0, 1])

            if self.direction_wander != 0:
                self.rect.x += self.direction_wander * self.vitesse_marche
                self.flip = (self.direction_wander < 0)
                self.moving = True

            # Limites
            if self.rect.x < self.start_x - 200: self.direction_wander = 1
            if self.rect.x > self.start_x + 200: self.direction_wander = -1

        elif self.etat == "FLEE":
            direction = 1 if self.rect.centerx > joueur_x else -1
            self.rect.x += direction * self.vitesse_fuite
            self.flip = (direction < 0)
            self.moving = True

        elif self.etat == "APPROACH":
            direction = 1 if self.rect.centerx < joueur_x else -1
            if dist_joueur > 60:
                self.rect.x += direction * self.vitesse_marche
                self.moving = True
            self.flip = (direction < 0)

        elif self.etat == "FOLLOW":
            if keys[pygame.K_RIGHT]:
                self.cote_suivi = -1
            elif keys[pygame.K_LEFT]:
                self.cote_suivi = 1

            cible_x = joueur_x + (self.cote_suivi * 85)
            if abs(self.rect.centerx - cible_x) > 15:
                direction = 1 if self.rect.centerx < cible_x else -1
                self.rect.x += direction * self.vitesse_fuite
                self.flip = (direction < 0)
                self.moving = True

        elif self.etat == "RETURN_TO_MOTHER":
            direction = 1 if self.rect.centerx < mere_rect.centerx else -1
            if abs(self.rect.centerx - mere_rect.centerx) > 25:
                self.rect.x += direction * self.vitesse_fuite
                self.flip = (direction < 0)
                self.moving = True
            else:
                self.rect.midbottom = (mere_rect.centerx, mere_rect.bottom)

        # --- 3. ANIMATION ---
        if self.moving:
            self.index_anim += self.vitesse_anim
            if self.index_anim >= 2: self.index_anim = 0
        else:
            self.index_anim = 0  # Image 1 fixe quand immobile

        paire = self.images.get(self.etat, self.images["WANDER"])
        self.image_actuelle = paire[int(self.index_anim)]

        if self.flip:
            self.image_actuelle = pygame.transform.flip(self.image_actuelle, True, False)

    def draw(self, surface, camera_x):
        pos_x = self.rect.x - camera_x
        if not self.loin:
            surface.blit(self.image_actuelle, (pos_x, self.rect.y))

        if self.afficher_bulle:
            pygame.draw.rect(surface, (255, 255, 255), (pos_x + 20, self.rect.y - 30, 25, 25), border_radius=5)
            surface.blit(self.font.render("E", True, (0, 0, 0)), (pos_x + 26, self.rect.y - 30))