import pygame

class Joueur:
    def __init__(self, x, y_sol):
        # Dimensions et apparence
        self.largeur = 50
        self.hauteur = 90
        self.couleur = (50, 80, 80)

        # Positionnement (le bas du rectangle touche le sol)
        self.rect = pygame.Rect(x - self.largeur // 2, y_sol - self.hauteur, self.largeur, self.hauteur)

        # Physique du saut
        self.vitesse_y = 0
        self.gravite = 0.8
        self.force_saut = -14
        self.au_sol = True
        self.y_sol = y_sol

    def sauter(self):
        if self.au_sol:
            self.vitesse_y = self.force_saut
            self.au_sol = False


    def update(self, plateformes):  # On ajoute l'argument plateformes
        # Appliquer la gravité
        self.vitesse_y += self.gravite
        self.rect.y += self.vitesse_y

        # On part du principe qu'on est en l'air, sauf si collision trouvée
        c_est_le_sol = False

        # 1. Collision avec le sol de base
        if self.rect.bottom >= self.y_sol:
            self.rect.bottom = self.y_sol
            self.vitesse_y = 0
            c_est_le_sol = True

        # 2. Collision avec les plateformes (seulement si on tombe)
        if self.vitesse_y > 0:  # On ne check la collision que si on descend
            for p in plateformes:
                if self.rect.colliderect(p.rect):
                    # On vérifie si les pieds du joueur sont au-dessus du haut de la plateforme
                    # (avec une marge de tolérance de la vitesse_y)
                    if self.rect.bottom <= p.rect.top + self.vitesse_y + 1:
                        self.rect.bottom = p.rect.top
                        self.vitesse_y = 0
                        c_est_le_sol = True

        self.au_sol = c_est_le_sol

    def draw(self, surface, camera_x):
        # On crée une copie du rectangle pour le décalage d'affichage
        rect_affichage = self.rect.copy()
        # On soustrait la position de la caméra pour le rendu à l'écran
        rect_affichage.x -= camera_x
        # Dessine le joueur avec sa position relative à la caméra
        pygame.draw.rect(surface, self.couleur, rect_affichage)