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
                self.vitesse_x += 0.4
                player.rect.right = self.rect.left
            else:
                self.vitesse_x -= 0.4
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
        self.rect = pygame.Rect(x, y_sol - 40, 60, 40)

        # --- AJOUT DU CHARGEMENT DES ANIMATIONS ---
        # Taille pour redimensionner les images
        taille = (60, 40)

        # Dictionnaire pour stocker les listes d'images par état
        self.animations = {
            "CONTENT": [
                pygame.transform.scale(pygame.image.load("images/castor/pousse1.png").convert_alpha(), taille),
                pygame.transform.scale(pygame.image.load("images/castor/pousse2.png").convert_alpha(), taille)
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

        # Variables pour gérer l'animation
        self.index_anim = 0
        self.vitesse_anim = 0.3  # Vitesse d'alternance (plus petit = plus lent)
        self.image = self.animations["POUSSE"][0]  # Image par défaut

        self.vitesse = 2
        self.etat = "ATTENTE"
        self.timer_debut = 0
        self.plateformes = []

    def animer(self, type_anim):
        """Gère l'alternance des images pour une animation donnée."""
        self.index_anim += self.vitesse_anim
        # Si on dépasse la fin de la liste, on recommence
        if self.index_anim >= len(self.animations[type_anim]):
            self.index_anim = 0

        # On met à jour l'image courante (en convertissant l'index en entier)
        self.image = self.animations[type_anim][int(self.index_anim)]

    def update(self, dechet_rect, eau_debut, eau_fin, largeur_joueur=50):
        # Gestion de l'image d'animation selon l'état
        if self.etat == "ATTENTE":
            self.animer("POUSSE")
        elif self.etat == "FINI":
            self.animer("CONTENT")
        elif self.etat == "TRAVAIL":
            self.animer("CONSTRUIT")
        # Note: L'état "POUSSE" n'est pas utilisé dans ton code Castor actuel,
        # mais les images sont chargées.

        # Le castor s'active quand le baril commence à tomber (centerx > eau_debut)
        if self.etat == "ATTENTE" and dechet_rect.centerx > eau_debut:
            self.etat = "TIMER"
            self.timer_debut = time.time()

        if self.etat == "TIMER":
            if time.time() - self.timer_debut >= 1.0:
                self.etat = "TRAVAIL"

        if self.etat == "TRAVAIL":
            self.rect.x += self.vitesse

            # MODIFICATION : Construction SEULEMENT entre eau_debut et eau_fin + largeur joueur
            if self.rect.right >= eau_debut and self.rect.left <= (eau_fin + largeur_joueur):
                if len(self.plateformes) == 0 or self.rect.x > self.plateformes[-1].right:
                    # On s'assure que la première planche commence pile à eau_debut
                    x_pose = max(self.rect.x, eau_debut)
                    nouveau_morceau = pygame.Rect(x_pose, 400, 20, 10)
                    self.plateformes.append(nouveau_morceau)

            # Il s'arrête quand il a fini de construire toute la zone
            if self.rect.left >= (eau_fin + largeur_joueur):
                self.etat = "FINI"

    def draw(self, screen, camera_x):
        # On garde ton dessin de plateformes identique
        for p in self.plateformes:
            pygame.draw.rect(screen, (100, 60, 30), (p.x - camera_x, p.y, p.width, p.height))

        # --- REMPLACEMENT DU RECTANGLE PAR L'IMAGE ---
        # On affiche l'image d'animation à la position du rect
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))