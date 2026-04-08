import pygame
import background
from joueur import Joueur
from Animaux.Marcassin import Marcassin


def main():
    pygame.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Héritage - La Quête du Marcassin")

    clock = pygame.time.Clock()

    bg = background.Background(SCREEN_WIDTH, SCREEN_HEIGHT, 10000)
    player = Joueur(200, bg.ground_top)

    # On place le marcassin à 800px du début
    petit_marcassin = Marcassin(800, bg.ground_top)

    camera_x = 0
    vitesse_joueur = 4
    vitesse_max_camera = vitesse_joueur + 6
    MARGE_CAMERA = 400
    PUISSANCE_COURBE = 2.0

    running = True
    while running:
        touche_caresse = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_UP]:
                    player.sauter()
                if event.key == pygame.K_e:
                    touche_caresse = True

        keys = pygame.key.get_pressed()
        joueur_en_mouvement = False

        # Mouvements Joueur
        if keys[pygame.K_RIGHT]:
            player.rect.x += vitesse_joueur
            joueur_en_mouvement = True
        elif keys[pygame.K_LEFT]:
            player.rect.x -= vitesse_joueur
            joueur_en_mouvement = True
            if player.rect.x < 0: player.rect.x = 0

        # Updates
        player.update()
        petit_marcassin.update(player.rect.x, joueur_en_mouvement, touche_caresse, keys)

        # Calcul Caméra
        player_screen_x = player.rect.x - camera_x
        if player_screen_x > SCREEN_WIDTH - MARGE_CAMERA:
            ratio = min(1.0, (player_screen_x - (SCREEN_WIDTH - MARGE_CAMERA)) / MARGE_CAMERA)
            camera_x += vitesse_max_camera * (ratio ** PUISSANCE_COURBE)
        elif player_screen_x < MARGE_CAMERA:
            ratio = min(1.0, (MARGE_CAMERA - player_screen_x) / MARGE_CAMERA)
            camera_x -= vitesse_max_camera * (ratio ** PUISSANCE_COURBE)
            if camera_x < 0: camera_x = 0

        # Affichage
        bg.draw(screen, camera_x)
        petit_marcassin.draw(screen, camera_x)

        # Dessin Joueur (avec caméra)
        rect_player_cam = player.rect.copy()
        rect_player_cam.x -= camera_x
        pygame.draw.rect(screen, player.couleur, rect_player_cam)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()