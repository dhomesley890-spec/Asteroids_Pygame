import pygame
import sys
from player import Player
from logger import log_state, log_event
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import constants



def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")
    
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clo = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)

    field = AsteroidField()

    ship = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
    
    while(True):
      log_state()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return
      
      screen.fill("black")
      dt = (clo.tick(60) / 1000)
      
      updatable.update(dt)

      for aster in asteroids:
          if aster.collides_with(ship):
             log_event("player_hit")
             print("Game over!")
             sys.exit()
          for shot in shots:
              if aster.collides_with(shot):
                 log_event("asteroid_shot")
                 aster.split()
                 shot.kill()

      for sprite in drawable:
          sprite.draw(screen)
      
      pygame.display.flip()



if __name__ == "__main__":
    main()
