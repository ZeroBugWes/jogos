
import pygame
import random

from settings import WORLD_WIDTH, WORLD_HEIGHT


class Food:

    def __init__(self, x, y):

        self.position = pygame.Vector2(x, y)
        self.radius = 6
        self.energy_value = 20

    def draw(self, screen, camera_offset):

        x = int(self.position.x - camera_offset.x)
        y = int(self.position.y - camera_offset.y)

        # Desenhar somente se estiver na tela
        if (-self.radius <= x <= screen.get_width() + self.radius
                and -self.radius <= y <= screen.get_height() + self.radius):

            pygame.draw.circle(
                screen,
                (100, 255, 130),
                (x, y),
                self.radius
            )

            pygame.draw.circle(
                screen,
                (210, 255, 210),
                (x, y),
                2
            )


def create_food():

    x = random.randint(30, WORLD_WIDTH - 30)
    y = random.randint(30, WORLD_HEIGHT - 30)

    return Food(x, y)
