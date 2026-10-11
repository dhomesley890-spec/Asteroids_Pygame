import random
import sys
import pygame
import constants
from asteroid import Asteroid
from scoreboard import load_scores
from starfield import draw_starfield
from settings import toggle_fullscreen, is_fullscreen

# 5x5 pixel-style letters for the block title
LETTERS = {
    "A": ["01110", "10001", "11111", "10001", "10001"],
    "S": ["01111", "10000", "01110", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100"],
    "E": ["11111", "10000", "11110", "10000", "11111"],
    "R": ["11110", "10001", "11110", "10100", "10011"],
    "O": ["01110", "10001", "10001", "10001", "01110"],
    "I": ["11111", "00100", "00100", "00100", "11111"],
    "D": ["11110", "10001", "10001", "10001", "11110"],
}


def draw_block_text(screen, text, center_x, top, cell=18, gap=3):
    letter_width = 5 * cell
    total_width = len(text) * letter_width + (len(text) - 1) * cell
    x = center_x - total_width // 2
    for ch in text:
        for row, line in enumerate(LETTERS[ch]):
            for col, bit in enumerate(line):
                if bit == "1":
                    rect = pygame.Rect(
                        x + col * cell, top + row * cell, cell - gap, cell - gap
                    )
                    pygame.draw.rect(screen, "white", rect)
        x += letter_width + cell


def draw_button(screen, font, rect, label, hovered):
    if hovered:
        pygame.draw.rect(screen, "white", rect)
        color = "black"
    else:
        pygame.draw.rect(screen, "white", rect, constants.LINE_WIDTH)
        color = "white"
    text = font.render(label, True, color)
    screen.blit(text, text.get_rect(center=rect.center))


def spawn_background_asteroid(randomize_position=False):
    radius = constants.ASTEROID_MIN_RADIUS * random.randint(1, constants.ASTEROID_KINDS)
    w, h = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT

    if randomize_position:
        pos = pygame.Vector2(random.uniform(0, w), random.uniform(0, h))
    else:
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            pos = pygame.Vector2(-radius, random.uniform(0, h))
        elif side == "right":
            pos = pygame.Vector2(w + radius, random.uniform(0, h))
        elif side == "top":
            pos = pygame.Vector2(random.uniform(0, w), -radius)
        else:
            pos = pygame.Vector2(random.uniform(0, w), h + radius)

    # aim loosely at the middle of the screen so they drift across it
    target = pygame.Vector2(
        w / 2 + random.uniform(-300, 300), h / 2 + random.uniform(-200, 200)
    )
    direction = target - pos
    if direction.length() == 0:
        direction = pygame.Vector2(1, 0)

    asteroid = Asteroid(pos.x, pos.y, radius)
    asteroid.velocity = direction.normalize() * random.uniform(40, 110)


CX = constants.SCREEN_WIDTH // 2
MARGIN = 200
BOUNDS = pygame.Rect(
    -MARGIN, -MARGIN,
    constants.SCREEN_WIDTH + 2 * MARGIN,
    constants.SCREEN_HEIGHT + 2 * MARGIN,
)


def tick_background(background, dt, spawn_timer) -> float:
    """Moves, spawns and culls the menu asteroids. Returns the new spawn timer."""
    background.update(dt)
    spawn_timer += dt
    if spawn_timer >= constants.ASTEROID_SPAWN_RATE_SECONDS:
        spawn_timer = 0.0
        spawn_background_asteroid()
    for asteroid in background:
        if not BOUNDS.collidepoint(asteroid.position):
            asteroid.kill()
    return spawn_timer


def run_scoreboard(screen, clock, background) -> bool:
    """Returns True to go back to the menu, False if the window was closed."""
    title_font = pygame.font.Font(None, 80)
    row_font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 40)

    back_rect = pygame.Rect(20, 20, 140, 50)
    panel = pygame.Rect(0, 0, 640, 600)
    panel.center = (CX, constants.SCREEN_HEIGHT // 2)

    scores = load_scores()
    spawn_timer = 0.0

    while True:
        dt = clock.tick(60) / 1000
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                toggle_fullscreen()

        spawn_timer = tick_background(background, dt, spawn_timer)

        draw_starfield(screen)
        for asteroid in background:
            asteroid.draw(screen)

        # solid panel so the asteroids don't clutter the text
        pygame.draw.rect(screen, "black", panel)
        pygame.draw.rect(screen, "white", panel, constants.LINE_WIDTH)

        title = title_font.render("HIGH SCORES", True, "white")
        screen.blit(title, title.get_rect(center=(CX, panel.top + 55)))

        for i in range(10):
            y = panel.top + 125 + i * 44
            value = str(scores[i]) if i < len(scores) else "---"
            rank = row_font.render(f"{i + 1}.", True, "white")
            score = row_font.render(value, True, "white")
            screen.blit(rank, rank.get_rect(midleft=(panel.left + 80, y)))
            screen.blit(score, score.get_rect(midright=(panel.right - 80, y)))

        draw_button(screen, button_font, back_rect, "BACK", back_rect.collidepoint(mouse))
        pygame.display.flip()


def run_menu(screen, clock) -> bool:
    """Returns True to start the game, False to quit."""
    background = pygame.sprite.Group()
    # Menu asteroids go in their own group, separate from the game's groups
    Asteroid.containers = (background,)

    for _ in range(10):
        spawn_background_asteroid(randomize_position=True)

    button_font = pygame.font.Font(None, 48)
    hint_font = pygame.font.Font(None, 28)

    start_rect = pygame.Rect(0, 0, 320, 64)
    scores_rect = pygame.Rect(0, 0, 320, 64)
    fs_rect = pygame.Rect(0, 0, 320, 64)
    quit_rect = pygame.Rect(0, 0, 320, 64)
    start_rect.center = (CX, 360)
    scores_rect.center = (CX, 430)
    fs_rect.center = (CX, 500)
    quit_rect.center = (CX, 570)

    spawn_timer = 0.0

    while True:
        dt = clock.tick(60) / 1000
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(event.pos):
                    return True
                if scores_rect.collidepoint(event.pos):
                    if not run_scoreboard(screen, clock, background):
                        return False
                if fs_rect.collidepoint(event.pos):
                    toggle_fullscreen()
                if quit_rect.collidepoint(event.pos):
                    return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                toggle_fullscreen()

        spawn_timer = tick_background(background, dt, spawn_timer)

        draw_starfield(screen)
        for asteroid in background:
            asteroid.draw(screen)

        draw_block_text(screen, "ASTEROIDS", CX, 140)
        draw_button(screen, button_font, start_rect, "START GAME", start_rect.collidepoint(mouse))
        draw_button(screen, button_font, scores_rect, "SCOREBOARD", scores_rect.collidepoint(mouse))
        label = f"FULLSCREEN: {'ON' if is_fullscreen() else 'OFF'}"
        draw_button(screen, button_font, fs_rect, label, fs_rect.collidepoint(mouse))
        draw_button(screen, button_font, quit_rect, "QUIT GAME", quit_rect.collidepoint(mouse))

        hint = hint_font.render("Enter to start  |  Esc to quit", True, "white")
        screen.blit(hint, hint.get_rect(center=(CX, constants.SCREEN_HEIGHT - 40)))

        pygame.display.flip()
