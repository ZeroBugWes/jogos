
import pygame


def draw_energy_bar(screen, energy, max_energy):

    x = 25
    y = 25

    width = 220
    height = 20

    # Fundo da barra
    pygame.draw.rect(
        screen,
        (35, 45, 60),
        (x, y, width, height),
        border_radius=8
    )

    # Quantidade de energia
    percentage = energy / max_energy

    current_width = int(width * percentage)

    if percentage > 0.5:
        color = (65, 220, 130)
    elif percentage > 0.25:
        color = (255, 190, 65)
    else:
        color = (235, 75, 75)

    pygame.draw.rect(
        screen,
        color,
        (x, y, current_width, height),
        border_radius=8
    )

    # Texto
    font = pygame.font.Font(None, 25)

    text = font.render(
        f"ENERGIA: {int(energy)}",
        True,
        (255, 255, 255)
    )

    screen.blit(text, (x, y + 27))
