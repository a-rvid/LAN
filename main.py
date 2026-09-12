import pygame
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 36)

# Set the window title
pygame.display.set_caption("Digital Clock")

def draw_clock(clockFont, screen_size=(1080, 720)):
    # Draw current time
    now = datetime.now()
    text = clockFont.render(now.strftime("%H:%M:%S"), True, (255, 255, 255))
    screen.blit(text, (screen_size[0] // 2 - text.get_width() // 2, screen_size[1] // 2 - text.get_height() // 2))

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    draw_clock(font, screen.get_size())

    pygame.display.flip()

pygame.quit()
