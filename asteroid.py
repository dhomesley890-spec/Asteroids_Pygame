import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
           return
        else:
           log_event("asteroid_split")
           ang = random.uniform(20, 50)
           vec1 = self.velocity.rotate(ang)
           vec2 = self.velocity.rotate(-ang)
           new_rad = self.radius - ASTEROID_MIN_RADIUS
           aster1 = Asteroid(self.position.x, self.position.y, new_rad)
           aster2 = Asteroid(self.position.x, self.position.y, new_rad)
           aster1.velocity = vec1 * 1.2
           aster2.velocity = vec2 * 1.2
