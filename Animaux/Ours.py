# librairie
import pygame
pygame.init()

class Ours(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # --- APPARENCE ---
        # Remplacer par self.image = pygame.image.load("chemin/vers/image.png") plus tard
        self.image = pygame.Surface((60, 60))
        self.image.fill((139, 69, 19))  # Marron par défaut
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # --- VARIABLES DE L'IA (Le "cerveau") ---
        self.etat_actuel = "neutre"
        self.quete_accomplie = False  # Passe à True si l'enfant l'aide
        self.vitesse = 2

    def etat_joie(self):
        """L'ours est content : il a été aidé ou la pollution est basse."""
        self.etat_actuel = "joie"
        self.image.fill((50, 200, 50))  # Devient vert/lumineux pour le test
        # Comportement : Il peut par exemple avancer vers le joueur pour lui donner un objet

    def etat_colere(self):
        """L'ours est en colère : le joueur pollue devant lui ou l'attaque."""
        self.etat_actuel = "colere"
        self.image.fill((200, 50, 50))  # Devient rouge pour le test
        # Comportement : Il bloque le passage (le joueur ne peut pas le traverser)

    def etat_peur(self):
        """L'ours a peur : une grosse machine approche ou pollution extrême."""
        self.etat_actuel = "peur"
        self.image.fill((150, 150, 150))  # Devient gris
        # Comportement : Il fuit dans la direction opposée

    def etat_amour(self):
        """L'allié ultime pour la fin du jeu."""
        self.etat_actuel = "amour"
        self.image.fill((255, 105, 180))  # Rose pour le test
        # Comportement : Il suit le joueur pour l'aider à détruire l'usine

    def analyser_environnement(self, joueur, empreinte_carbone):
        """C'est ici qu'est l'intelligence artificielle. L'ours observe et réagit."""
        distance_joueur = abs(self.rect.x - joueur.rect.x)

        # Condition 1 : Si la quête de l'ours est finie, il est l'allié du joueur
        if self.quete_accomplie:
            self.etat_amour()

        # Condition 2 : Si le joueur est très polluant (lié à ton fichier Empreinte_carbonne.py)
        elif empreinte_carbone > 80:
            if distance_joueur < 200:  # Si le joueur s'approche trop
                self.etat_colere()
            else:
                self.etat_peur()

        # Condition 3 : Si la forêt est propre et le joueur approche calmement
        elif empreinte_carbone < 30 and distance_joueur < 150:
            self.etat_joie()

        # Condition par défaut
        else:
            self.etat_actuel = "neutre"
            self.image.fill((139, 69, 19))  # Retour à la normale

    def update(self, joueur, empreinte_carbone):
        """Mise à jour à appeler à chaque frame dans le main.py"""
        # 1. L'ours réfléchit
        self.analyser_environnement(joueur, empreinte_carbone)

        # 2. L'ours agit en fonction de son humeur
        if self.etat_actuel == "peur":
            # Il fuit le joueur
            if self.rect.x < joueur.rect.x:
                self.rect.x -= self.vitesse
            else:
                self.rect.x += self.vitesse
