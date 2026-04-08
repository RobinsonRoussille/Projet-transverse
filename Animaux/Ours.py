import pygame


class Ours(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # --- APPARENCE ---
        self.image = pygame.Surface((60, 60))
        self.image.fill((139, 69, 19))  # Marron par défaut
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # --- VARIABLES DE L'IA ---
        self.etat_actuel = "neutre"
        self.quete_accomplie = False
        self.vitesse = 2

        # --- MÉCANIQUE DE FAIM ---
        self.faim = 100.0  # 100 = Ventre plein
        self.perte_faim = 0.02  # Vitesse à laquelle il a faim

    def etat_joie(self):
        self.etat_actuel = "joie"
        self.image.fill((50, 200, 50))  # Vert

    def etat_colere(self):
        self.etat_actuel = "colere"
        self.image.fill((200, 50, 50))  # Rouge

    def etat_peur(self):
        self.etat_actuel = "peur"
        self.image.fill((150, 150, 150))  # Gris

    def etat_amour(self):
        self.etat_actuel = "amour"
        self.image.fill((255, 105, 180))  # Rose

    def analyser_environnement(self, joueur, empreinte_carbone):
        distance_joueur = abs(self.rect.x - joueur.rect.x)

        # 1. Si sauvé
        if self.quete_accomplie:
            self.etat_amour()

        # 2. Si affamé (Priorité haute pour l'histoire)
        elif self.faim < 30:
            self.etat_actuel = "affame"
            self.image.fill((255, 165, 0))  # Orange

        # 3. Pollution
        elif empreinte_carbone > 80:
            if distance_joueur < 200:
                self.etat_colere()
            else:
                self.etat_peur()

        # 4. Forêt propre
        elif empreinte_carbone < 30 and distance_joueur < 150:
            self.etat_joie()

        # 5. Neutre
        else:
            self.etat_actuel = "neutre"
            self.image.fill((139, 69, 19))

    def update(self, joueur, empreinte_carbone):
        # L'ours a de plus en plus faim
        if self.faim > 0:
            self.faim -= self.perte_faim

        # L'IA réfléchit
        self.analyser_environnement(joueur, empreinte_carbone)

        # Mouvement si peur
        if self.etat_actuel == "peur":
            if self.rect.x < joueur.rect.x:
                self.rect.x -= self.vitesse
            else:
                self.rect.x += self.vitesse