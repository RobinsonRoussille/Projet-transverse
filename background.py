import pygame
import random


class Element:
    def __init__(self, x, horizon_y, width, h_range, color, has_border=False):
        self.width = width
        self.height = random.randint(h_range[0], h_range[1])
        self.x = x
        self.y = horizon_y - self.height
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(color)
        if has_border:
            pygame.draw.rect(self.surface, (30, 60, 30), (0, 0, self.width, self.height), 2)
        self.surface = self.surface.convert()


class Background:
    def __init__(self, screen_width, screen_height, world_dist):
        self.sw = screen_width
        self.sh = screen_height
        self.world_dist = world_dist
        self.ground_top = int(screen_height * (2 / 3))
        self.horizon_far = self.ground_top - 80

        # Couleurs du ciel : Matin (Bleu clair) -> Soir (Bleu nuit/Grisâtre)
        self.color_start = (140, 190, 230)
        self.color_end = (30, 40, 70)

        self.layers = [
            {
                "elements": self._generate_layer(world_dist, self.horizon_far, 350, (200, 300), (-100, -50),
                                                 (90, 95, 110)),
                "speed": 0.2,
                "floor_color": (40, 70, 40),
                "floor_y": self.horizon_far,
                "floor_h": self.ground_top - self.horizon_far
            },
            {
                "elements": self._generate_layer(world_dist, self.horizon_far, 40, (50, 100), (-10, 5), (45, 85, 45)),
                "speed": 0.5,
                "floor_color": None
            },
            {
                "elements": self._generate_layer(world_dist, self.ground_top, 70, (120, 220), (10, 60), (60, 140, 60),
                                                 True),
                "speed": 1.0,
                "floor_color": (50, 100, 50),
                "floor_y": self.ground_top,
                "floor_h": self.sh - self.ground_top
            }
        ]

    def _generate_layer(self, dist, horiz, w, h_range, gap, color, border=False):
        elems = []
        x = -w
        while x < dist:
            elems.append(Element(x, horiz, w, h_range, color, border))
            x += w + random.randint(gap[0], gap[1])
        return elems

    def _get_sky_color(self, camera_x):
        # Calcul du ratio de progression (0.0 au début, 1.0 à la fin)
        ratio = min(1.0, camera_x / (self.world_dist - self.sw))

        # Interpolation Linéaire (Lerp) entre les deux couleurs
        r = self.color_start[0] + (self.color_end[0] - self.color_start[0]) * ratio
        g = self.color_start[1] + (self.color_end[1] - self.color_start[1]) * ratio
        b = self.color_start[2] + (self.color_end[2] - self.color_start[2]) * ratio
        return (int(r), int(g), int(b))

    def draw(self, screen, camera_x):
        # Remplissage du ciel avec la couleur calculée
        screen.fill(self._get_sky_color(camera_x))

        for layer in self.layers:
            for e in layer["elements"]:
                dx = e.x - (camera_x * layer["speed"])
                if -e.width < dx < self.sw:
                    screen.blit(e.surface, (dx, e.y))

            if layer["floor_color"]:
                pygame.draw.rect(screen, layer["floor_color"], (0, layer["floor_y"], self.sw, layer["floor_h"]))
                if layer["speed"] == 1.0:
                    pygame.draw.line(screen, (30, 50, 30), (0, self.ground_top), (self.sw, self.ground_top), 3)