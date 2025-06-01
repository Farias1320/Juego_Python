import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, laser_img):
        super().__init__()
        self.image = laser_img  # Cambia surf por image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -35  # Velocidad hacia arriba

    def update(self, delta_time):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom < 0:
            self.kill()