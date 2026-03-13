import pygame
import sys

pygame.init()

# Fenêtre
LARGEUR, HAUTEUR = 1000, 500
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Scrolling background + parallax")

clock = pygame.time.Clock()
FPS = 60


# Images
background = pygame.image.load("back1.png").convert()
background = pygame.transform.scale(background, (LARGEUR, HAUTEUR))

foreground = pygame.image.load("back3.png").convert_alpha()
foreground = pygame.transform.scale(foreground, (LARGEUR, HAUTEUR))

# ===== IMAGE USINE =====
usine_img = pygame.image.load("usine.png").convert_alpha()
usine_largeur = 1200
usine_hauteur = 1200
usine_img = pygame.transform.scale(usine_img, (usine_largeur, usine_hauteur))


# Offsets de scrolling
bg_x = 0
fg_x = 0


# Joueur
joueur_largeur = 50
joueur_hauteur = 90
joueur_x = LARGEUR // 2 - joueur_largeur // 2

sol_y = HAUTEUR - 60
joueur_y = sol_y - joueur_hauteur

vitesse = 2
vitesse_y = 5
gravite = 0.81
force_saut = -13
au_sol = True


# ===== USINE =====
usine_x = -600
usine_y = sol_y - usine_hauteur + 100

# Élément interne fixé en (0,0)
element_x = 0
element_y = 0

cpt = 0


# Boucle principale
running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    touches = pygame.key.get_pressed()

    # Mouvement → décor
    if touches[pygame.K_RIGHT]:
        bg_x += vitesse
        fg_x += vitesse
        usine_x -= vitesse

    if touches[pygame.K_LEFT] and bg_x == 0:
        bg_x -= vitesse
        fg_x -= vitesse
        usine_x += vitesse
    elif touches[pygame.K_LEFT]:
        bg_x -= vitesse
        fg_x -= vitesse
        usine_x += vitesse
        if cpt >= 5:
            bg_x += vitesse
            fg_x += vitesse
            usine_x -= vitesse
            cpt = 0
    # Boucle infinie background
    bg_x %= LARGEUR
    fg_x %= LARGEUR
    cpt +=1
    print(cpt)
    # Saut
    if (touches[pygame.K_SPACE] or touches[pygame.K_UP]) and au_sol:
        vitesse_y = force_saut
        au_sol = False

    vitesse_y += gravite
    joueur_y += vitesse_y

    if joueur_y >= sol_y - joueur_hauteur:
        joueur_y = sol_y - joueur_hauteur
        vitesse_y = 0
        au_sol = True


    # ===== DESSIN =====

    # Background
    fenetre.blit(background, (-bg_x, 0))
    fenetre.blit(background, (LARGEUR - bg_x, 0))


    # ===== USINE IMAGE =====
    fenetre.blit(
        usine_img,
        (usine_x, usine_y)
    )


    # Élément fixé en (0,0) dans l'usine
    pygame.draw.circle(
        fenetre,
        (255, 0, 0),
        (usine_x + element_x, usine_y + element_y),
        6
    )


    # Joueur
    pygame.draw.rect(
        fenetre,
        (50, 80, 80),
        (joueur_x, joueur_y, joueur_largeur, joueur_hauteur)
    )


    # Foreground
    fenetre.blit(foreground, (-fg_x, 0))
    fenetre.blit(foreground, (LARGEUR - fg_x, 0))


    pygame.display.flip()


pygame.quit()
sys.exit()