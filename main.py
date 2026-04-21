import pygame
import background
from joueur import Joueur
from Animaux.Marcassin import Marcassin
from Animaux.MereSanglier import MereSanglier
from Animaux.Mouette import Mouette
from Animaux.Castor import Castor, Dechet


def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Héritage")
    clock = pygame.time.Clock()

    # --- INITIALISATION ---
    WORLD_SIZE = 10000
    bg = background.Background(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_SIZE)
    player = Joueur(200, bg.ground_top)

    mouette = Mouette(1200, bg.ground_top)
    petit_marcassin = Marcassin(2500, bg.ground_top)
    maman_sanglier = MereSanglier(4000, bg.ground_top)

    eau_debut = 2000
    eau_fin = 3500
    castor = Castor(1850, bg.ground_top)
    baril = Dechet(1950, bg.ground_top)

    camera_x = 0
    camera_smoothing = 0.04

    running = True
    while running:
        touche_caresse = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: touche_caresse = True
                if event.key in [pygame.K_SPACE, pygame.K_UP]: player.sauter()

        keys = pygame.key.get_pressed()
        veut_courir = keys[pygame.K_LSHIFT]

        # --- DÉPLACEMENT DU JOUEUR ---
        en_mouvement = False
        if keys[pygame.K_RIGHT]:
            player.rect.x += player.vitesse_actuelle
            en_mouvement = True
        elif keys[pygame.K_LEFT]:
            player.rect.x -= player.vitesse_actuelle
            en_mouvement = True
            if player.rect.x < 0: player.rect.x = 0

        # --- LOGIQUE DE COLLISION & ÉTATS (ORDRE RÉPARÉ) ---

        # 1. On définit d'abord la zone d'eau pour que la variable existe
        dans_zone_x_eau = (player.rect.x >= eau_debut) and (player.rect.x <= eau_fin)

        # 2. On vérifie si le joueur est sur le pont
        sur_le_pont = False
        for planche in castor.plateformes:
            if player.rect.right > planche.left and player.rect.left < planche.right:
                if player.rect.bottom <= planche.top + 20:
                    sur_le_pont = True
                    if player.vitesse_y >= 0 and player.rect.colliderect(planche):
                        player.rect.bottom = planche.top
                        player.vitesse_y = 0
                        player.au_sol = True

        # 3. On met à jour les stats du joueur (vitesse, saut) en fonction de l'eau
        player.dansEau(dans_zone_x_eau, eau_debut, eau_fin, screen, camera_x, sur_le_pont)

        # 4. Update du déchet
        baril_au_fond = baril.rect.x > eau_debut
        est_en_train_de_pousser = False

        if not baril_au_fond:
            est_en_train_de_pousser = baril.update(player, eau_debut, eau_fin)
        else:
            # Update physique seule quand le baril est au fond
            baril.vitesse_y += 0.8
            baril.rect.y += baril.vitesse_y
            if baril.rect.bottom > 470:
                baril.rect.bottom = 470
                baril.vitesse_y = 0

        # 5. Update finale du joueur et du castor
        player.update(veut_courir, est_en_train_de_pousser)
        castor.update(baril.rect, eau_debut, eau_fin, player.largeur)

        # --- ANIMAUX & CAMÉRA ---
        joueur_court = (en_mouvement and veut_courir)
        petit_marcassin.update(player.rect.x, en_mouvement, touche_caresse, keys, maman_sanglier.rect)
        mouette.update(player.rect.x, joueur_court, touche_caresse)

        target_camera_x = player.rect.centerx - SCREEN_WIDTH // 2
        camera_x += (target_camera_x - camera_x) * camera_smoothing
        camera_x = max(0, min(camera_x, WORLD_SIZE - SCREEN_WIDTH))

        # --- RENDU (ORDRE DES COUCHES) ---
        bg.draw(screen, camera_x)

        # On dessine l'eau en premier dans la zone


        baril.draw(screen, camera_x)
        mouette.draw(screen, camera_x)
        petit_marcassin.draw(screen, camera_x)

        if petit_marcassin.etat in ["FOLLOW", "RETURN_TO_MOTHER"]:
            maman_sanglier.draw(screen, camera_x, petit_marcassin.etat)

        player.draw(screen, camera_x)
        player.dansEau(dans_zone_x_eau, eau_debut, eau_fin, screen, camera_x, sur_le_pont)
        castor.draw(screen, camera_x)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()