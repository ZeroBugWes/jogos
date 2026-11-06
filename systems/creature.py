
import pygame
import random

WORLD_WIDTH = 3000
WORLD_HEIGHT = 3000


class Creature:

    def __init__(self):

        self.position = pygame.Vector2(
            random.randint(50, WORLD_WIDTH - 50),
            random.randint(50, WORLD_HEIGHT - 50)
        )

        self.radius = random.randint(8, 15)
        self.speed = random.randint(25, 65)

        self.direction = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        self.change_direction_timer = 0

        self.color = random.choice([
            (100, 220, 180),
            (120, 180, 255),
            (180, 130, 230),
            (230, 190, 100)
        ])

    def update(self, delta_time):

        self.change_direction_timer -= delta_time

        if self.change_direction_timer <= 0:

            self.direction = pygame.Vector2(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            )

            if self.direction.length() > 0:
                self.direction = self.direction.normalize()

            self.change_direction_timer = random.uniform(1, 3)

        self.position += self.direction * self.speed * delta_time

        if self.position.x < self.radius:
            self.position.x = self.radius
            self.direction.x *= -1

        elif self.position.x > WORLD_WIDTH - self.radius:
            self.position.x = WORLD_WIDTH - self.radius
            self.direction.x *= -1

        if self.position.y < self.radius:
            self.position.y = self.radius
            self.direction.y *= -1

        elif self.position.y > WORLD_HEIGHT - self.radius:
            self.position.y = WORLD_HEIGHT - self.radius
            self.direction.y *= -1

    def draw(self, screen, camera_offset):

        x = int(self.position.x - camera_offset.x)
        y = int(self.position.y - camera_offset.y)

        if (
            -self.radius <= x <= screen.get_width() + self.radius
            and -self.radius <= y <= screen.get_height() + self.radius
        ):

            pygame.draw.circle(
                screen,
                self.color,
                (x, y),
                self.radius
            )

            pygame.draw.circle(
                screen,
                (230, 255, 245),
                (x, y),
                self.radius,
                2
            )

            pygame.draw.circle(
                screen,
                (35, 70, 100),
                (x + 3, y - 2),
                max(2, self.radius // 3)
            )
