
import pygame

from systems.evolution import EVOLUTIONS


def draw_evolution_menu(screen, organism):

    overlay = pygame.Surface(
        screen.get_size(),
        pygame.SRCALPHA
    )

    overlay.fill((0, 10, 25, 220))

    screen.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 52)
    font = pygame.font.Font(None, 29)
    small_font = pygame.font.Font(None, 23)

    title = title_font.render(
        "EVOLUCAO",
        True,
        (100, 255, 220)
    )

    screen.blit(
        title,
        title.get_rect(center=(500, 100))
    )

    points = font.render(
        f"Pontos evolutivos: {organism.evolution_points}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        points,
        points.get_rect(center=(500, 155))
    )

    y = 225

    for key, evolution in EVOLUTIONS.items():

        name = font.render(
            f"[{key}] {evolution['name']} - {evolution['cost']} pontos",
            True,
            (255, 255, 255)
        )

        description = small_font.render(
            evolution["description"],
            True,
            (160, 195, 210)
        )

        screen.blit(name, (180, y))
        screen.blit(description, (200, y + 30))

        y += 85

    instruction = small_font.render(
        "Pressione 1, 2, 3 ou 4 para evoluir | TAB para fechar",
        True,
        (100, 255, 220)
    )

    screen.blit(
        instruction,
        instruction.get_rect(center=(500, 610))
    )
