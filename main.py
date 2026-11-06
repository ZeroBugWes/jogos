
import pygame
import random

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GAME_TITLE,
    FPS,
    WORLD_WIDTH,
    WORLD_HEIGHT
)

from entities.organism import Organism
from entities.food import create_food
from entities.creature import Creature

from interface.hud import draw_energy_bar
from interface.evolution_menu import draw_evolution_menu

from systems.evolution import purchase_evolution
from systems.biomes import get_biome


pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(GAME_TITLE)

clock = pygame.time.Clock()

organism = Organism(
    WORLD_WIDTH // 2,
    WORLD_HEIGHT // 2
)

foods = [create_food() for _ in range(250)]

creatures = [Creature() for _ in range(60)]

particles = []

for i in range(1200):
    particles.append((
        random.randint(0, WORLD_WIDTH),
        random.randint(0, WORLD_HEIGHT)
    ))

evolution_menu_open = False
running = True
game_over = False

font = pygame.font.Font(None, 32)


def draw_ocean(camera_offset, biome):

    screen.fill(biome["color"])

    for particle in particles:

        x = int(particle[0] - camera_offset.x)
        y = int(particle[1] - camera_offset.y)

        if 0 <= x <= SCREEN_WIDTH and 0 <= y <= SCREEN_HEIGHT:

            pygame.draw.circle(
                screen,
                (70, 120, 145),
                (x, y),
                2
            )


while running:

    delta_time = clock.tick(FPS) / 1000

    # Eventos
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_TAB and not game_over:
                evolution_menu_open = not evolution_menu_open

            elif evolution_menu_open and event.unicode in ["1", "2", "3", "4"]:
                purchase_evolution(organism, event.unicode)

    keys = pygame.key.get_pressed()

    # Atualização do jogo
    if not game_over and not evolution_menu_open:

        organism.update(keys, delta_time)

        organism.consume_energy(delta_time)

        # Atualizar criaturas e verificar ataques
        for creature in creatures:

            creature.update(delta_time, organism.position)

            if creature.behavior == "predador":

                distance = organism.position.distance_to(
                    creature.position
                )

                if distance < organism.radius + creature.radius:

                    organism.energy -= 20 * delta_time

                    organism.energy = max(
                        0,
                        organism.energy
                    )

        # Alimentação
        for food in foods[:]:

            distance = organism.position.distance_to(
                food.position
            )

            if distance < organism.radius + food.radius:

                organism.eat(food)

                organism.gain_evolution_points(1)

                # Crescimento e evolução biológica
                organism.grow(1)

                foods.remove(food)

                foods.append(create_food())

        # Verificar energia
        if organism.energy <= 0:
            game_over = True

    # Câmera
    camera_offset = pygame.Vector2(
        organism.position.x - SCREEN_WIDTH // 2,
        organism.position.y - SCREEN_HEIGHT // 2
    )

    camera_offset.x = max(
        0,
        min(WORLD_WIDTH - SCREEN_WIDTH, camera_offset.x)
    )

    camera_offset.y = max(
        0,
        min(WORLD_HEIGHT - SCREEN_HEIGHT, camera_offset.y)
    )

    # Bioma
    current_biome = get_biome(
        organism.position.x,
        organism.position.y
    )

    # Desenhar mundo
    draw_ocean(camera_offset, current_biome)

    for food in foods:
        food.draw(screen, camera_offset)

    for creature in creatures:
        creature.draw(screen, camera_offset)

    organism.draw(screen, camera_offset)

    # Interface
    draw_energy_bar(
        screen,
        organism.energy,
        organism.max_energy
    )

    biome_text = font.render(
        current_biome["name"],
        True,
        (230, 245, 255)
    )

    screen.blit(
        biome_text,
        (SCREEN_WIDTH - biome_text.get_width() - 25, 25)
    )

    if evolution_menu_open:
        draw_evolution_menu(screen, organism)

    if game_over:

        game_over_text = pygame.font.Font(None, 65).render(
            "GAME OVER",
            True,
            (255, 100, 100)
        )

        screen.blit(
            game_over_text,
            game_over_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
        )

    # Atualizar tela
    pygame.display.flip()


pygame.quit()

