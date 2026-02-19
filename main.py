import pygame
import sys

pygame.init()

# Fenêtre
LARGEUR, HAUTEUR = 918, 648
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Scrolling background + parallax")

clock = pygame.time.Clock()
FPS = 60

# Images
background = pygame.image.load("back.png").convert()
background = pygame.transform.scale(background, (LARGEUR, HAUTEUR))

foreground = pygame.image.load("back2.png").convert_alpha()
foreground = pygame.transform.scale(foreground, (LARGEUR, HAUTEUR))

# Offsets de scrolling
bg_x = 0
fg_x = 0

# Joueur
joueur_largeur = 40
joueur_hauteur = 40
joueur_x = LARGEUR // 2 - joueur_largeur // 2
sol_y = HAUTEUR - 15
joueur_y = sol_y - joueur_hauteur

vitesse = 6
vitesse_y = 0
gravite = 0.81
force_saut = -15
au_sol = True

# Boucle principaleAC
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    touches = pygame.key.get_pressed()

    # Mouvement → décor
    if touches[pygame.K_RIGHT]:
        bg_x += vitesse * 0.5   # fond lent
        fg_x += vitesse * 0.5   # avant-plan plus rapide
    if touches[pygame.K_LEFT]:
        bg_x -= vitesse * 0.5
        fg_x -= vitesse * 0.5

    # Boucle infinie
    bg_x %= LARGEUR
    fg_x %= LARGEUR

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
    # Background (2 fois pour boucle)
    fenetre.blit(background, (-bg_x, 0))
    fenetre.blit(background, (LARGEUR - bg_x, 0))

    # Joueur
    pygame.draw.rect(
        fenetre,
        (50, 80, 80),
        (joueur_x, joueur_y, joueur_largeur, joueur_hauteur)
    )

    # Foreground (parallax)
    fenetre.blit(foreground, (-fg_x, 0))
    fenetre.blit(foreground, (LARGEUR - fg_x, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()
