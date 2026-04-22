import pygame
import math  # Obligatoire pour le mouvement de la liane

class Plateforme:
    def __init__(self, x, y, largeur):
        # On fixe la hauteur à 20 directement ici
        self.rect = pygame.Rect(x, y, largeur, 20)
        self.couleur = (100, 60, 30)

    def draw(self, screen, camera_x):
        affichage_rect = self.rect.copy()
        affichage_rect.x -= camera_x
        pygame.draw.rect(screen, self.couleur, affichage_rect)


class Liane:
    def __init__(self, x, y_ancrage, longueur_totale=300):
        self.x_ancrage = x
        self.y_ancrage = y_ancrage

        # Division en 3 segments
        self.l = longueur_totale / 3
        self.g = 0.5  # Gravité légèrement réduite pour la stabilité

        # Angles initiaux
        self.th1, self.th2, self.th3 = 0.2, 0.1, 0.0
        self.w1, self.w2, self.w3 = 0.0, 0.0, 0.0

        self.pos_bout = [x, y_ancrage + longueur_totale]
        self.rect = pygame.Rect(x - 20, y_ancrage + longueur_totale - 20, 40, 40)

    def update(self):
        # 1. CALCUL DES ACCÉLÉRATIONS
        a1 = (-self.g / self.l) * math.sin(self.th1)
        a2 = (-self.g / self.l) * math.sin(self.th2)
        a3 = (-self.g / self.l) * math.sin(self.th3)

        # 2. AMORTISSEMENT PLUS FORT (Damping)
        # 0.98 au lieu de 0.99 pour absorber l'énergie excédentaire
        damping = 0.96

        self.w1 = (self.w1 + a1) * damping
        self.w2 = (self.w2 + a2 + (self.w1 * 0.1)) * damping  # Le parent entraîne l'enfant
        self.w3 = (self.w3 + a3 + (self.w2 * 0.1)) * damping

        # 3. MISE À JOUR DES ANGLES ET LIMITATION
        self.th1 += self.w1
        self.th2 += self.w2
        self.th3 += self.w3

        # --- SÉCURITÉ : On limite les angles pour éviter le "foutoir" ---
        # Empêche les segments de faire des tours complets
        limite = math.pi / 3  # 90 degrés max par rapport au parent
        self.th1 = max(-limite, min(limite, self.th1))
        self.th2 = max(-limite, min(limite, self.th2))
        self.th3 = max(-limite, min(limite, self.th3))

        # 4. CALCUL DES POSITIONS (Chaînage)
        self.x1 = self.x_ancrage + self.l * math.sin(self.th1)
        self.y1 = self.y_ancrage + self.l * math.cos(self.th1)

        self.x2 = self.x1 + self.l * math.sin(self.th2)
        self.y2 = self.y1 + self.l * math.cos(self.th2)

        self.x3 = self.x2 + self.l * math.sin(self.th3)
        self.y3 = self.y2 + self.l * math.cos(self.th3)

        self.pos_bout = [self.x3, self.y3]
        self.rect.center = (int(self.x3), int(self.y3))

    def draw(self, screen, camera_x):
        # ... (le code de dessin reste le même que précédemment) ...
        p0 = (self.x_ancrage - camera_x, self.y_ancrage)
        p1 = (self.x1 - camera_x, self.y1)
        p2 = (self.x2 - camera_x, self.y2)
        p3 = (self.x3 - camera_x, self.y3)

        pygame.draw.lines(screen, (34, 139, 34), False, [p0, p1, p2, p3], 5)
        pygame.draw.circle(screen, (50, 200, 50), (int(p3[0]), int(p3[1])), 10)
