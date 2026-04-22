import pygame


class Pere:
    def __init__(self, x, y_sol):
        self.largeur, self.hauteur = 45, 110
        self.rect = pygame.Rect(x, y_sol - self.hauteur, self.largeur, self.hauteur)

        # --- CHARGEMENT DE L'IMAGE ---
        self.image_originale = pygame.image.load("images/dad.png").convert_alpha()
        self.image_originale = pygame.transform.scale(self.image_originale, (self.largeur, self.hauteur))

        self.font = pygame.font.SysFont("Arial", 20, bold=True)

        # Dialogues
        self.repliques_debut = [
            " "
            "Allez, je file au boulot à l'usine...",
            "C'est ma dernière journée avant la retraite !",
            "Ce soir, tu prends les clés et tu deviens la PDG.",
            "En attendant, balade-toi bien. À ce soir !"
        ]

        self.repliques_fin = [
            "Te voilà enfin ! L'usine tourne à plein régime.",
            "Alors, es-tu prête à accepter ton héritage ?",
            "Deviendras-tu la nouvelle PDG ? (O: Accepter / N: Refuser)"
        ]

        self.index_replique = 0
        self.fini = False
        self.mode_final = False
        self.delai_replique = 4000
        self.dernier_update = pygame.time.get_ticks()

    def activer_mode_final(self, nouvelle_pos_x):
        self.rect.x = nouvelle_pos_x
        self.index_replique = 0
        self.fini = False
        self.mode_final = True
        self.dernier_update = pygame.time.get_ticks()

    def update(self):
        if not self.fini:
            liste_actuelle = self.repliques_fin if self.mode_final else self.repliques_debut
            if self.mode_final and self.index_replique == len(liste_actuelle) - 1:
                return

            maintenant = pygame.time.get_ticks()
            if maintenant - self.dernier_update > self.delai_replique:
                self.index_replique += 1
                self.dernier_update = maintenant
                if self.index_replique >= len(liste_actuelle):
                    self.fini = True

    def draw(self, screen, camera_x, player_x):
        if not self.fini or self.mode_final:
            # --- LOGIQUE D'ORIENTATION ---
            # Si le joueur est à gauche du père, on flippe l'image
            if player_x < self.rect.centerx:
                img_a_afficher = pygame.transform.flip(self.image_originale, True, False)
            else:
                img_a_afficher = self.image_originale

            # Dessin de l'image
            screen.blit(img_a_afficher, (self.rect.x - camera_x, self.rect.y))

            # Dessin du texte
            liste_actuelle = self.repliques_fin if self.mode_final else self.repliques_debut
            if self.index_replique < len(liste_actuelle):
                txt_surf = self.font.render(liste_actuelle[self.index_replique], True, (255, 255, 255))
                txt_rect = txt_surf.get_rect(center=(self.rect.centerx - camera_x, self.rect.y - 40))
                pygame.draw.rect(screen, (0, 0, 0), txt_rect.inflate(20, 10), border_radius=8)
                screen.blit(txt_surf, txt_rect)