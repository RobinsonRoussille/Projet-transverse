import pygame
import random


class Marcassin:
    def __init__(self, x, y_sol):
        self.largeur = 35
        self.hauteur = 25
        self.couleur = (139, 69, 19)
        self.rect = pygame.Rect(x, y_sol - self.hauteur, self.largeur, self.hauteur)

        self.start_x = x
        self.y_sol = y_sol
        self.vitesse_marche = 1.5
        self.vitesse_fuite = 4
        self.cote_suivi = -1

        # Paramètres de quête
        self.distance_fuite_max = 700
        self.zone_detection = 350
        self.zone_caresse = 60
        self.distance_stop_approche = 50

        # États et Timers
        self.etat = "WANDER"
        self.timer_IA = 0
        self.direction_x = 0

        # NOUVEAU : Timer pour éviter les changements d'état trop brusques
        self.timer_recuperation = 0

        self.afficher_bulle = False
        self.font = pygame.font.SysFont(None, 26)

    def update(self, joueur_x, joueur_en_mouvement, touche_caresse, keys):
        if self.etat == "LOST":
            return

        dist_joueur = abs(self.rect.x - joueur_x)
        dist_depart = abs(self.rect.x - self.start_x)
        self.afficher_bulle = False

        # On décrémente le timer de récupération (environ 60 ticks = 1 seconde)
        if self.timer_recuperation > 0:
            self.timer_recuperation -= 1

        # --- MACHINE À ÉTATS ---
        if self.etat != "FOLLOW":
            # 1. Échec de la quête
            if dist_depart > self.distance_fuite_max:
                self.etat = "LOST"

            # 2. Fuite (prioritaire si le joueur bouge et est proche)
            elif dist_joueur < self.zone_detection and joueur_en_mouvement:
                if self.etat != "FLEE":
                    self.etat = "FLEE"
                    # On réinitialise le temps de récupération à chaque fois qu'il fuit
                    self.timer_recuperation = 100  # ~1.5 seconde de "choc"

            # 3. Caresse (si proche et joueur immobile)
            elif dist_joueur <= self.zone_caresse and not joueur_en_mouvement:
                self.afficher_bulle = True
                if touche_caresse:
                    self.etat = "FOLLOW"

            # 4. Approche (Uniquement si le temps de récupération est fini)
            elif dist_joueur < self.zone_detection and not joueur_en_mouvement and self.timer_recuperation <= 0:
                self.etat = "APPROACH"

            # 5. Par défaut : Flânerie
            else:
                # Si on n'est pas en train de fuir, on flâne
                if self.etat != "FLEE":
                    self.etat = "WANDER"

                # Si on était en train de fuir mais que le joueur s'est arrêté/éloigné,
                # on repasse en WANDER pour un moment de calme
                if self.etat == "FLEE" and (not joueur_en_mouvement or dist_joueur > self.zone_detection):
                    self.etat = "WANDER"

        # --- ACTIONS ---
        if self.etat == "WANDER":
            self.timer_IA -= 1
            if self.timer_IA <= 0:
                self.timer_IA = random.randint(40, 100)
                if self.rect.x < self.start_x - 100:
                    self.direction_x = random.choices([-1, 0, 1], [1, 2, 7])[0]
                elif self.rect.x > self.start_x + 100:
                    self.direction_x = random.choices([-1, 0, 1], [7, 2, 1])[0]
                else:
                    self.direction_x = random.choice([-1, 0, 1])
            self.rect.x += self.direction_x * self.vitesse_marche

        elif self.etat == "APPROACH":
            if dist_joueur > self.distance_stop_approche:
                if self.rect.x < joueur_x:
                    self.rect.x += self.vitesse_marche
                else:
                    self.rect.x -= self.vitesse_marche

        elif self.etat == "FLEE":
            # Si le marcassin est hors écran, il court moins vite pour laisser une chance au joueur
            vitesse_actuelle = self.vitesse_fuite
            x_sur_ecran = self.rect.x - (joueur_x - 400)  # Approximation de la caméra

            if x_sur_ecran < 0 or x_sur_ecran > 1200:
                vitesse_actuelle = self.vitesse_marche  # Il ralentit car il ne voit plus le danger

            if self.rect.x < joueur_x:
                self.rect.x -= vitesse_actuelle - 1
            else:
                self.rect.x += vitesse_actuelle + 1

        elif self.etat == "FOLLOW":
            if keys[pygame.K_RIGHT]:
                self.cote_suivi = -1
            elif keys[pygame.K_LEFT]:
                self.cote_suivi = 1

            cible_x = joueur_x + (self.cote_suivi * 70)
            if abs(self.rect.x - cible_x) > 5:
                direction = 1 if self.rect.x < cible_x else -1
                self.rect.x += direction * self.vitesse_fuite

    def draw(self, surface, camera_x):
        if self.etat == "LOST":
            return
        pos_ecran = self.rect.copy()
        pos_ecran.x -= camera_x
        pygame.draw.rect(surface, self.couleur, pos_ecran, border_radius=3)
        if self.afficher_bulle:
            bulle_rect = pygame.Rect(pos_ecran.centerx - 15, pos_ecran.y - 35, 30, 25)
            pygame.draw.rect(surface, (255, 255, 255), bulle_rect, border_radius=5)
            txt = self.font.render("E", True, (0, 0, 0))
            surface.blit(txt, (bulle_rect.x + 8, bulle_rect.y + 3))