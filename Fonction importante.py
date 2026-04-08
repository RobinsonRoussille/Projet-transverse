import pygame


def generate():
    pygame.init()
    # 4 images de 35x25 pixels
    sheet = pygame.Surface((140, 25), pygame.SRCALPHA)
    marron = (139, 69, 19)
    noir = (0, 0, 0)

    for i in range(4):
        x_off = i * 35
        # Corps
        pygame.draw.rect(sheet, marron, (x_off + 5, 10, 25, 15), border_radius=3)
        # Tête
        pygame.draw.rect(sheet, marron, (x_off + 22, 12, 10, 8), border_radius=2)
        # Œil
        pygame.draw.rect(sheet, noir, (x_off + 28, 14, 2, 2))

        # Jambes (différentes selon l'index pour l'animation)
        if i == 0:  # Repos
            pygame.draw.line(sheet, marron, (x_off + 10, 24), (x_off + 10, 25), 2)
            pygame.draw.line(sheet, marron, (x_off + 20, 24), (x_off + 20, 25), 2)
        elif i == 1:  # Marche 1
            pygame.draw.line(sheet, marron, (x_off + 8, 24), (x_off + 12, 25), 2)
        elif i == 2:  # Marche 2
            pygame.draw.line(sheet, marron, (x_off + 12, 24), (x_off + 8, 25), 2)
        elif i == 3:  # Peur (Yeux blancs)
            pygame.draw.rect(sheet, (255, 255, 255), (x_off + 27, 13, 4, 4))
            pygame.draw.rect(sheet, noir, (x_off + 28, 14, 2, 2))

    pygame.image.save(sheet, "marcassin_sprites.png")
    print("Sprite sheet 'marcassin_sprites.png' générée !")


if __name__ == "__main__":
    generate()