import pygame
from start_screen import show_start_screen
from level_select import select_level
from game import Game
from levels import save_progress

pygame.init()
pygame.mixer.init()

# Música de fondo para el menú y selección de nivel
pygame.mixer.music.load("sprites/fondo01.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((800, 600))

show_start_screen(screen)

while True:
    level = select_level(screen)
    
    # Cambia la música al iniciar el juego
    pygame.mixer.music.load("sprites/fondo04.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    result = Game(level).loop()
    
    # Cuando termina el juego, vuelve a poner la música del menú
    pygame.mixer.music.load("sprites/fondo01.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    if result == "win" and level < 5:
        save_progress(level + 1)