import pygame
import time


class Dechet:
    def __init__(self, x, y_sol):
        # On garde ton rect identique pour les collisions et la physique
        self.rect = pygame.Rect(x, y_sol - 60, 42, 64)

        # Ajout de l'image (redimensionnée à la taille du rect)
        try:
            self.image = pygame.image.load("images/castor/dechet.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (42, 63))
            self.image = pygame.transform.flip(self.image, True, False)
        except:
            # Simple surface vide si l'image n'est pas trouvée
            self.image = pygame.Surface((60, 60), pygame.SRCALPHA)

        self.vitesse_x = 0
        self.vitesse_y = 0
        self.friction = 0.8
        self.dans_eau = False

    def update(self, player, eau_debut, eau_fin):
        pousse = False

        self.dans_eau = eau_debut <= self.rect.x <= eau_fin

        y_sol_actuel = 470 if self.dans_eau else 400

        if self.rect.colliderect(player.rect):
            pousse = True
            if player.rect.centerx < self.rect.centerx:
                self.vitesse_x += 0.2
                player.rect.right = self.rect.left
            else:
                self.vitesse_x -= 0.2
                player.rect.left = self.rect.right

        self.rect.x += self.vitesse_x
        self.vitesse_x *= self.friction
        self.vitesse_y += 0.8
        self.rect.y += self.vitesse_y

        if self.rect.bottom >= y_sol_actuel:
            self.rect.bottom = y_sol_actuel
            self.vitesse_y = 0

        return pousse

    def draw(self, screen, camera_x):
        # On affiche l'image à la position du rect (le rect devient "invisible")
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))


class Castor:
    def __init__(self, x, y_sol):
        self.rect = pygame.Rect(x, y_sol - 50, 50, 50)

        # --- CHARGEMENT DES ANIMATIONS ---
        taille = (50, 50)

        self.animations = {
            "ATTENTE": [
                pygame.transform.scale(pygame.image.load("images/castor/attente1.png").convert_alpha(), taille),
                pygame.transform.scale(pygame.image.load("images/castor/attente2.png").convert_alpha(), taille)
            ],
            "CONTENT": [
                pygame.transform.scale(pygame.image.load("images/castor/content1.png").convert_alpha(), taille),
                pygame.transform.scale(pygame.image.load("images/castor/content2.png").convert_alpha(), taille)
            ],
            "POUSSE": [
                pygame.transform.scale(pygame.image.load("images/castor/pousse1.png").convert_alpha(), taille),
                pygame.transform.scale(pygame.image.load("images/castor/pousse2.png").convert_alpha(), taille)
            ],
            "CONSTRUIT": [
                pygame.transform.scale(pygame.image.load("images/castor/travail1.png").convert_alpha(), taille),
                pygame.transform.scale(pygame.image.load("images/castor/travail2.png").convert_alpha(), taille)
            ]
        }

        self.index_anim = 0
        self.vitesse_anim = 0.1
        self.image = self.animations["ATTENTE"][0]

        self.vitesse = 2
        self.etat = "ATTENTE"
        self.timer_debut = 0
        self.plateformes = []

    def animer(self, type_anim):
        self.index_anim += self.vitesse_anim
        if self.index_anim >= len(self.animations[type_anim]):
            self.index_anim = 0
        self.image = self.animations[type_anim][int(self.index_anim)]

    def update(self, dechet, eau_debut, eau_fin, largeur_joueur=70):
        dechet_rect = dechet.rect
        en_contact = self.rect.colliderect(dechet_rect)

        # --- ANIMATION (Modifiée pour attendre le bord de l'eau) ---
        if self.etat == "ATTENTE" or self.etat == "TIMER":
            if en_contact:
                self.animer("POUSSE")
            else:
                self.animer("ATTENTE")
        elif self.etat == "FINI":
            self.animer("CONTENT")
        elif self.etat == "TRAVAIL":
            # NOUVEAU : On n'anime "CONSTRUIT" que s'il est vraiment au bord de l'eau
            if self.rect.right < eau_debut:
                if en_contact:
                    self.animer("POUSSE")
                else:
                    self.animer("ATTENTE")
            else:
                self.animer("CONSTRUIT")

        # --- RÉSOLUTION DE COLLISION ---
        if self.etat != "TRAVAIL" and en_contact:
            if dechet_rect.left < self.rect.right - 5:
                dechet_rect.left = self.rect.right - 5
                if dechet.vitesse_x < 0:
                    dechet.vitesse_x = 0

        # --- LOGIQUE D'ÉTAT ---
        if self.etat == "ATTENTE" and dechet_rect.centerx > eau_debut:
            self.etat = "TIMER"
            self.timer_debut = time.time()

        if self.etat == "TIMER":
            if time.time() - self.timer_debut >= 2.0:
                self.etat = "TRAVAIL"

        if self.etat == "TRAVAIL":
            self.rect.x += self.vitesse

            # On ne commence à poser des planches que s'il a atteint l'eau
            if self.rect.right >= eau_debut and self.rect.left <= (eau_fin + largeur_joueur):
                if len(self.plateformes) == 0 or self.rect.x > self.plateformes[-1].right:
                    x_pose = max(self.rect.x, eau_debut)
                    # Création du Rect de la plateforme
                    nouveau_morceau = pygame.Rect(x_pose, 400, 20, 10)
                    self.plateformes.append(nouveau_morceau)

            if self.rect.left >= (eau_fin + largeur_joueur):
                self.etat = "FINI"

    def draw(self, screen, camera_x):
        for p in self.plateformes:
            # Dessin des planches en marron
            pygame.draw.rect(screen, (100, 60, 30), (p.x - camera_x, p.y, p.width, p.height))
        # Dessin du castor
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))