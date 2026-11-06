import math
import pygame

from settings import (
    ORGANISM_SPEED,
    ORGANISM_RADIUS,
    WORLD_WIDTH,
    WORLD_HEIGHT
)


class Organism:
    def __init__(self, x, y):
        self.animation_time = 0.0
        self.facing_direction = pygame.Vector2(1, 0)

        self.evolution_stage = 1
        self.growth = 0
        self.growth_required = 20
        self.stage_name = "Célula primitiva"
        self.evolution_points = 0

        self.defense = 1
        self.perception = 1
        self.energy_efficiency = 1

        self.energy = 100
        self.max_energy = 100
        self.energy_consumption = 2

        self.position = pygame.Vector2(x, y)
        self.speed = ORGANISM_SPEED
        self.radius = ORGANISM_RADIUS

    def grow(self, amount):
        self.growth += amount

        while self.growth >= self.growth_required:
            if self.evolution_stage >= 4:
                self.growth = self.growth_required - 1
                break

            self.growth -= self.growth_required
            self.evolution_stage += 1
            self.radius += 5
            self.max_energy += 20
            self.energy = self.max_energy
            self.growth_required += 20

            if self.evolution_stage == 2:
                self.stage_name = "Organismo multicelular"
            elif self.evolution_stage == 3:
                self.stage_name = "Organismo aquático"
                self.speed += 15
            elif self.evolution_stage == 4:
                self.stage_name = "Peixe primitivo"
                self.speed += 25

    def update(self, keys, delta_time):
        self.animation_time += delta_time
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.facing_direction = direction.copy()

        self.position += direction * self.speed * delta_time
        self.position.x = max(
            self.radius,
            min(WORLD_WIDTH - self.radius, self.position.x)
        )
        self.position.y = max(
            self.radius,
            min(WORLD_HEIGHT - self.radius, self.position.y)
        )

    def consume_energy(self, delta_time):
        consumption = self.energy_consumption / max(1, self.energy_efficiency)
        self.energy = max(0, self.energy - consumption * delta_time)

    def eat(self, food):
        self.energy = min(self.max_energy, self.energy + food.energy_value)

    def gain_evolution_points(self, amount):
        self.evolution_points += amount

    def evolve(self, trait):
        if trait == "fins":
            self.speed += 40
        elif trait == "membrane":
            self.defense += 1
        elif trait == "perception":
            self.perception += 1
        elif trait == "efficiency":
            self.energy_efficiency += 1

    @staticmethod
    def _pixel_outline(surface, rect, color=(12, 35, 55), width=2):
        pygame.draw.rect(surface, color, rect, width)

    def _draw_cell(self, sprite, body, light, dark):
        # Célula em camadas, com núcleo e pequenas estruturas internas.
        pygame.draw.circle(sprite, dark, (32, 32), 20)
        pygame.draw.circle(sprite, body, (32, 30), 18)
        pygame.draw.circle(sprite, light, (27, 24), 7)
        pygame.draw.rect(sprite, (35, 116, 139), (26, 29, 13, 10))
        pygame.draw.rect(sprite, (18, 74, 104), (29, 32, 7, 5))
        pygame.draw.rect(sprite, (190, 255, 229), (18, 17, 5, 3))
        pygame.draw.rect(sprite, (190, 255, 229), (40, 28, 4, 3))
        pygame.draw.rect(sprite, dark, (18, 43, 5, 3))
        self._pixel_outline(sprite, (12, 10, 40, 40), (14, 61, 83), 2)

    def _draw_multicellular(self, sprite, body, light, dark):
        # Pequenas células agrupadas, sem transformar o conjunto em um círculo liso.
        cells = [
            (23, 25, 12), (36, 23, 12), (26, 38, 12),
            (39, 37, 11), (32, 31, 13)
        ]
        for cx, cy, radius in cells:
            pygame.draw.circle(sprite, dark, (cx, cy + 2), radius)
            pygame.draw.circle(sprite, body, (cx, cy), radius - 1)
            pygame.draw.rect(sprite, light, (cx - 4, cy - 5, 5, 3))
            pygame.draw.rect(sprite, (28, 91, 119), (cx + 1, cy + 1, 4, 4))
        pygame.draw.rect(sprite, (19, 67, 91), (29, 28, 8, 8))
        pygame.draw.rect(sprite, (125, 235, 202), (30, 29, 5, 5))

    def _draw_swimmer(self, sprite, body, light, dark, advanced=False):
        # O sprite é desenhado apontando para a direita e rotacionado no final.
        t = self.animation_time
        tail_wave = int(round(math.sin(t * 9.0) * (4 if advanced else 3)))
        fin_wave = int(round(math.sin(t * 7.0 + 1.0) * 2))

        tail_color = (36, 105, 151) if advanced else (43, 125, 158)
        fin_color = (69, 157, 190) if advanced else (63, 151, 177)

        # Cauda articulada com movimento em blocos.
        pygame.draw.polygon(
            sprite, dark,
            [(17, 29), (5, 20 + tail_wave), (8, 32 + tail_wave),
             (5, 44 + tail_wave), (18, 36)]
        )
        pygame.draw.polygon(
            sprite, tail_color,
            [(17, 30), (7, 22 + tail_wave), (10, 32 + tail_wave),
             (7, 41 + tail_wave), (18, 35)]
        )
        pygame.draw.rect(sprite, (116, 194, 205), (8, 27 + tail_wave, 4, 3))

        # Nadadeiras laterais e dorsal.
        pygame.draw.polygon(
            sprite, dark,
            [(31, 29), (26, 17 - fin_wave), (39, 25), (38, 31)]
        )
        pygame.draw.polygon(
            sprite, fin_color,
            [(32, 28), (28, 19 - fin_wave), (38, 25), (37, 29)]
        )
        pygame.draw.polygon(
            sprite, dark,
            [(31, 36), (27, 47 + fin_wave), (40, 39), (38, 34)]
        )
        pygame.draw.polygon(
            sprite, fin_color,
            [(32, 36), (29, 45 + fin_wave), (38, 39), (37, 35)]
        )

        if advanced:
            pygame.draw.polygon(
                sprite, dark,
                [(34, 24), (39, 14 - fin_wave), (46, 25)]
            )
            pygame.draw.polygon(
                sprite, (91, 180, 214),
                [(35, 24), (40, 16 - fin_wave), (44, 24)]
            )

        # Corpo principal com contorno em degraus para aspecto pixel art.
        pygame.draw.ellipse(sprite, dark, (13, 20, 43, 25))
        pygame.draw.ellipse(sprite, body, (15, 20, 40, 22))
        pygame.draw.rect(sprite, body, (23, 18, 25, 26))
        pygame.draw.rect(sprite, light, (27, 21, 15, 4))
        pygame.draw.rect(sprite, (147, 211, 218), (39, 26, 10, 3))
        pygame.draw.rect(sprite, (37, 100, 137), (25, 38, 18, 3))

        # Escamas e linha lateral discretas.
        if advanced:
            for sx, sy in [(27, 29), (33, 32), (39, 29), (33, 37), (44, 34)]:
                pygame.draw.rect(sprite, (155, 211, 219), (sx, sy, 3, 2))
            pygame.draw.rect(sprite, (28, 79, 117), (24, 34, 25, 2))
        else:
            pygame.draw.rect(sprite, (150, 220, 211), (30, 33, 3, 2))
            pygame.draw.rect(sprite, (150, 220, 211), (38, 35, 3, 2))

        # Olho, brilho e boca.
        pygame.draw.rect(sprite, (11, 35, 58), (47, 25, 5, 7))
        pygame.draw.rect(sprite, (245, 250, 225), (48, 25, 3, 4))
        pygame.draw.rect(sprite, (10, 25, 42), (49, 27, 2, 3))
        pygame.draw.rect(sprite, (20, 61, 84), (52, 36, 4, 2))

        if advanced:
            # Brânquias em pequenas linhas.
            pygame.draw.rect(sprite, (34, 104, 139), (25, 27, 2, 8))
            pygame.draw.rect(sprite, (34, 104, 139), (29, 28, 2, 7))

    def draw(self, screen, camera_offset):
        # Desenho em baixa resolução e ampliação nearest-neighbor:
        # isso cria bordas de pixel sem depender de imagens externas.
        sprite = pygame.Surface((64, 64), pygame.SRCALPHA)

        palette = {
            1: ((66, 194, 174), (174, 255, 222), (23, 91, 111)),
            2: ((91, 185, 143), (190, 245, 185), (27, 91, 79)),
            3: ((68, 151, 184), (174, 231, 220), (22, 75, 112)),
            4: ((63, 119, 190), (174, 220, 245), (20, 57, 111))
        }
        body, light, dark = palette.get(self.evolution_stage, palette[4])

        if self.evolution_stage == 1:
            self._draw_cell(sprite, body, light, dark)
        elif self.evolution_stage == 2:
            self._draw_multicellular(sprite, body, light, dark)
        else:
            self._draw_swimmer(
                sprite, body, light, dark,
                advanced=(self.evolution_stage >= 4)
            )

        # Bônus de defesa: placas externas douradas.
        if self.defense > 1:
            pygame.draw.rect(sprite, (255, 213, 105), (15, 13, 8, 3))
            pygame.draw.rect(sprite, (255, 213, 105), (42, 47, 8, 3))

        # Núcleo/energia mais brilhante quando a eficiência evolui.
        if self.energy_efficiency > 1 and self.evolution_stage <= 2:
            pygame.draw.rect(sprite, (111, 255, 145), (29, 29, 7, 7))

        # Percepção avançada: pequenos marcadores ao redor do organismo.
        if self.perception > 1:
            pulse = int((math.sin(self.animation_time * 3) + 1) * 2)
            pygame.draw.rect(sprite, (105, 225, 255), (29, 5 - pulse, 6, 2))
            pygame.draw.rect(sprite, (105, 225, 255), (29, 57 + pulse, 6, 2))

        # Rotaciona para acompanhar a última direção de movimento.
        angle = math.degrees(math.atan2(
            self.facing_direction.y, self.facing_direction.x
        ))
        rotated = pygame.transform.rotate(sprite, -angle)

        # Ampliação sem suavização para preservar os pixels.
        scaled = pygame.transform.scale(
            rotated, (rotated.get_width() * 2, rotated.get_height() * 2)
        )

        screen_x = int(self.position.x - camera_offset.x)
        screen_y = int(self.position.y - camera_offset.y)
        rect = scaled.get_rect(center=(screen_x, screen_y))
        screen.blit(scaled, rect)
