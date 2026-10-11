import random
import pygame
import constants

STAR_COUNT = 120

_cached = None


def _make_starfield() -> pygame.Surface:
    surface = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    surface.fill("black")
    for _ in range(STAR_COUNT):
        x = random.randrange(constants.SCREEN_WIDTH)
        y = random.randrange(constants.SCREEN_HEIGHT)
        brightness = random.randint(60, 200)  # dim, so the asteroids still stand out
        color = (brightness, brightness, brightness)
        size = 2 if random.random() < 0.15 else 1  # a few slightly bigger stars
        surface.fill(color, pygame.Rect(x, y, size, size))
    return surface


def draw_starfield(screen) -> None:
    global _cached
    if _cached is None:
        _cached = _make_starfield()
    screen.blit(_cached, (0, 0))
