import pygame
import sys
from menu import run_menu
from starfield import draw_starfield
from player import Player
from logger import log_state, log_event
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from scoreboard import load_scores, add_score, points_for, draw_scoreboard
import constants

def run_game(screen, clock) -> bool:
    """Plays one round. Returns True to go back to the menu, False to quit."""
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)

    ship = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
    AsteroidField()

    score = 0
    scores = load_scores()
    high_score = scores[0] if scores else 0
    score_font = pygame.font.Font(None, 36)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                add_score(score)
                return False

        draw_starfield(screen)
        dt = clock.tick(60) / 1000

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(ship):
                log_event("player_hit")
                add_score(score)
                return True

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += points_for(asteroid.radius)
                    high_score = max(high_score, score)
                    shot.kill()
                    asteroid.split()

        for sprite in drawable:
            sprite.draw(screen)

        draw_scoreboard(screen, score_font, score, high_score)
        pygame.display.flip()


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    while run_menu(screen, clock):
        if not run_game(screen, clock):
            break

    pygame.quit()


if __name__ == "__main__":
    main()

