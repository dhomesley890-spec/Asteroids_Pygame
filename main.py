import pygame
from player import Player
from logger import log_state
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

    Player.containers = (updatable, drawable)

    ship = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
    
    while(True):
      log_state()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return
      
      screen.fill("black")
      dt = (clo.tick(60) / 1000)
      
      updatable.update(dt)
      
      for sprite in drawable:
          sprite.draw(screen)
      
      pygame.display.flip()



if __name__ == "__main__":
    main()
