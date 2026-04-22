import pygame
import background
from joueur import Joueur
from Animaux.Marcassin import Marcassin
from Animaux.MereSanglier import MereSanglier
from Animaux.Mouette import Mouette
from Animaux.Castor import Castor, Dechet
from Animaux.Pere import Pere
from niveau_procedural import NiveauBoue
from plateforme import Plateforme, Liane
from Usine import Usine


def main():
    pygame.init()
    pygame.mixer.init()

    # --- AUDIO ---
    son_calme = pygame.mixer.Sound("sons/calme.mp3")
    son_aventure = pygame.mixer.Sound("sons/aventure.mp3")
    son_usine = pygame.mixer.Sound("sons/usine.mp3")

    canal_calme = son_calme.play(-1)
    canal_aventure = son_aventure.play(-1)
    canal_usine = son_usine.play(-1)

    # Volumes initiaux (on commence à l'usine)
    canal_calme.set_volume(0.0)
    canal_aventure.set_volume(0.0)
    canal_usine.set_volume(0.4)

    zone_actuelle = "usine"

    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Héritage")
    clock = pygame.time.Clock()

    # --- INITIALISATION MONDE ---
    WORLD_SIZE = 20000  # Remis à 20000 pour une vraie aventure
    bg = background.Background(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_SIZE)

    # Objets et Joueur
    player = Joueur(350, bg.ground_top)
    papa = Pere(200, bg.ground_top)
    usine_depart = Usine(bg.ground_top)
    # On positionne l'usine de fin tout au bout
    usine_fin = Usine(bg.ground_top, WORLD_SIZE)
    # Animaux
    mouette = Mouette(4500, bg.ground_top)
    petit_marcassin = Marcassin(3000, bg.ground_top)
    maman_sanglier = MereSanglier(6000, bg.ground_top)

    # Zones et obstacles
    eau_debut, eau_fin = 8000, 10000
    boue_debut, boue_fin = 12000, 15000
    castor = Castor(7500, bg.ground_top)
    baril = Dechet(7545, bg.ground_top)
    generateur_boue = NiveauBoue(boue_debut, boue_fin, bg.ground_top)

    camera_x = 0
    camera_smoothing = 0.04
    etat_jeu = "DIALOGUE"
    cinematique_finale = False

    running = True
    while running:
        touche_caresse = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if etat_jeu == "JEU":
                    if event.key == pygame.K_e: touche_caresse = True
                    if event.key in [pygame.K_SPACE, pygame.K_UP]:
                        if player.liane_actuelle:
                            player.liane_actuelle = None
                            player.vitesse_y = -15
                            player.au_sol = False
                        else:
                            player.sauter()

        keys = pygame.key.get_pressed()

        # --- LOGIQUE UPDATE ---
        en_mouvement = False
        veut_courir = False

        if etat_jeu == "DIALOGUE":
            papa.update()
            if papa.fini:
                etat_jeu = "JEU"
        else:
            # Mouvements actifs
            veut_courir = keys[pygame.K_LSHIFT]
            if keys[pygame.K_RIGHT]:
                if player.liane_actuelle:
                    player.liane_actuelle.w1 += 0.001
                else:
                    player.rect.x += player.vitesse_actuelle
                en_mouvement = True
            elif keys[pygame.K_LEFT]:
                if player.liane_actuelle:
                    player.liane_actuelle.w1 -= 0.001
                else:
                    player.rect.x -= player.vitesse_actuelle
                en_mouvement = True

        # --- GESTION DE LA FIN (Père réapparaît) ---
        dist_usine_fin = usine_fin.rect.left - player.rect.right

        if dist_usine_fin < 1000 and not cinematique_finale:
            # On téléporte le père à l'usine de fin
            papa.activer_mode_final(usine_fin.rect.left - 150)
            cinematique_finale = True

        if cinematique_finale:
            dist_pere = papa.rect.centerx - player.rect.centerx
            # Si on est assez proche (200px), le père parle
            if dist_pere < 200:
                papa.update()

            # Choix final : Touche O pour finir
            if papa.mode_final and papa.index_replique == len(papa.repliques_fin) - 1:
                if keys[pygame.K_o, pygame.K_n]:
                    running = False

        # Collisions Usines
        if player.rect.left < usine_depart.rect.right:
            player.rect.left = usine_depart.rect.right
        if player.rect.right > usine_fin.rect.left:
            player.rect.right = usine_fin.rect.left

        # --- ENVIRONNEMENT & COLLISIONS ---
        dans_zone_x_eau = (player.rect.x >= eau_debut) and (player.rect.x <= eau_fin)
        dans_boue = (player.rect.x >= boue_debut) and (player.rect.x <= boue_fin)
        sur_objet_sec = False

        # Plateformes castor & boue
        for planche in castor.plateformes:
            if player.rect.right > planche.left and player.rect.left < planche.right:
                if player.rect.bottom <= planche.top + 20:
                    if player.vitesse_y >= 0 and player.rect.colliderect(planche):
                        player.rect.bottom = planche.top
                        player.vitesse_y = 0
                        player.au_sol = True
                        sur_objet_sec = True

        generateur_boue.update()
        for element in generateur_boue.elements:
            if isinstance(element, Plateforme):
                if player.rect.right > element.rect.left and player.rect.left < element.rect.right:
                    if player.rect.bottom <= element.rect.top + 20:
                        if player.vitesse_y >= 0 and player.rect.colliderect(element.rect):
                            player.rect.bottom = element.rect.top
                            player.vitesse_y = 0
                            player.au_sol = True
                            sur_objet_sec = True
            elif isinstance(element, Liane):
                if player.rect.colliderect(element.rect) and not player.au_sol and player.vitesse_y > 0:
                    if player.liane_actuelle is None: player.liane_actuelle = element

        # --- MUSIQUE DYNAMIQUE ---
        if player.rect.x >= boue_debut - 150 and zone_actuelle != "aventure":
            canal_calme.set_volume(0.0);
            canal_aventure.set_volume(0.4);
            canal_usine.set_volume(0.0)
            zone_actuelle = "aventure"
        elif (player.rect.x < boue_debut - 150 and player.rect.x > 950) and zone_actuelle != "calme":
            canal_calme.set_volume(0.4);
            canal_aventure.set_volume(0.0);
            canal_usine.set_volume(0.0)
            zone_actuelle = "calme"
        elif (player.rect.x <= 950 or player.rect.x >= WORLD_SIZE - 1000) and zone_actuelle != "usine":
            canal_calme.set_volume(0.0);
            canal_aventure.set_volume(0.0);
            canal_usine.set_volume(0.4)
            zone_actuelle = "usine"

        # Update Joueur / Boue / Baril
        if dans_boue and not sur_objet_sec and not player.liane_actuelle:
            player.s_enfoncer()
            if player.rect.top > 500: player.reset_position(boue_debut - 100)
        else:
            if not player.liane_actuelle:
                player.dans_la_boue = False
                player.dansEau(dans_zone_x_eau, sur_objet_sec)

        baril_au_fond = baril.rect.x > eau_debut
        est_en_train_de_pousser = False
        if not baril_au_fond:
            est_en_train_de_pousser = baril.update(player, eau_debut, eau_fin)
        else:
            baril.vitesse_y += 0.5;
            baril.rect.y += baril.vitesse_y
            if baril.rect.bottom > 470: baril.rect.bottom = 470; baril.vitesse_y = 0

        player.update(veut_courir, est_en_train_de_pousser)
        castor.update(baril, eau_debut, eau_fin, player.largeur)
        petit_marcassin.update(player.rect.x, en_mouvement, touche_caresse, keys, maman_sanglier.rect)
        mouette.update(player.rect.x, (en_mouvement and veut_courir), touche_caresse)

        # Caméra
        target_camera_x = player.rect.centerx - SCREEN_WIDTH // 2
        camera_x += (target_camera_x - camera_x) * camera_smoothing
        camera_x = max(0, min(camera_x, WORLD_SIZE - SCREEN_WIDTH))

        # --- RENDU ---
        bg.draw(screen, camera_x)
        usine_depart.draw(screen, camera_x)
        usine_fin.draw(screen, camera_x)

        # Le père est dessiné soit au début (DIALOGUE), soit à la fin (cinematique_finale)
        if etat_jeu == "DIALOGUE" or cinematique_finale:
            papa.draw(screen, camera_x)

        baril.draw(screen, camera_x)
        mouette.draw(screen, camera_x)
        petit_marcassin.draw(screen, camera_x)
        if petit_marcassin.etat in ["FOLLOW", "RETURN_TO_MOTHER"]:
            maman_sanglier.draw(screen, camera_x, petit_marcassin.etat)
        generateur_boue.draw(screen, camera_x)
        player.draw(screen, camera_x, eau_debut, eau_fin, boue_debut, boue_fin)
        castor.draw(screen, camera_x)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()