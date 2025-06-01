import pygame
from levels import load_progress

def select_level(screen):
    unlocked_level = load_progress()
    font = pygame.font.SysFont(None, 48)
    selected = 1
    while True:
        screen.fill((0, 0, 0))
        for i in range(1, 6):
            color = (255, 255, 255) if i <= unlocked_level else (100, 100, 100)
            text = font.render(f"Nivel {i}", True, color)
            rect = text.get_rect(center=(screen.get_width() // 2, 100 + i * 80))
            screen.blit(text, rect)
            if i == selected:
                pygame.draw.rect(screen, (0, 255, 0), rect, 2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = max(1, selected - 1)
                if event.key == pygame.K_DOWN:
                    selected = min(5, selected + 1)
                if event.key == pygame.K_RETURN and selected <= unlocked_level:
                    return selected