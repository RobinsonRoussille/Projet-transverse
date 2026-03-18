import pygame
import background

def main():
    pygame.init()

    # Configuration
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Parallax Smooth Scrolling")

    clock = pygame.time.Clock()
    bg = background.Background(SCREEN_WIDTH, SCREEN_HEIGHT, 10000)

    camera_x = 0
    scroll_speed = 8
    running = True

    while running:
        # 1. Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Logique (Inputs)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            camera_x += scroll_speed
        if keys[pygame.K_LEFT]:
            camera_x -= scroll_speed

        # 3. Rendu
        bg.draw(screen, camera_x)

        pygame.display.flip()
        clock.tick(60) # 60 FPS constants

    pygame.quit()

if __name__ == "__main__":
    main()