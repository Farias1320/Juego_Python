import pygame
from constants import *
import random
import globals

# Tamaño del sprite original del meteorito (ajusta si tus imágenes tienen otro tamaño)
ORIGINAL_SIZE = (60, 60)
MIN_WIDTH = 25
MAX_WIDTH = 50

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()

        # Selecciona aleatoriamente una imagen de meteorito
        meteor_images = [
            'sprites/meteorito03.png',
            'sprites/meteorito04.png',
            'sprites/meteorito18.png'
        ]
        image_path = random.choice(meteor_images)

        # Tamaño aleatorio
        self.width = random.randint(MIN_WIDTH, MAX_WIDTH)
        self.height = int((self.width / ORIGINAL_SIZE[0]) * ORIGINAL_SIZE[1])

        self.surf = pygame.image.load(image_path).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.surf)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(-120, -40)
            )
        )

        # Velocidad más alta y aleatoria
        self.speed = random.uniform(0.007, 0.01) * SCREEN_HEIGHT / 60  # Entre ~14 y ~30 px/frame a 60 FPS

    def update(self, delta_time):
        self.rect.move_ip(0, self.speed * delta_time)
        self.mask = pygame.mask.from_surface(self.surf)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()