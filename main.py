import pygame
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True

# Load fonts
font_path = "./fonts/"
font_size = 112
secretFont = pygame.font.Font(font_path + "SecretFont.ttf", font_size)
normalFont = pygame.font.Font(font_path + "LowEffortFont.ttf", font_size)

# Set the window title
pygame.display.set_caption("Digital Clock")

def draw_clock(clockFont, position):
    # Draw current time
    now = datetime.now()
    text = clockFont.render(now.strftime("%H:%M:%S"), True, (255, 255, 255))
    centered_position = (position[0] - text.get_width() // 2, position[1] - text.get_height() // 2)
    screen.blit(text, centered_position)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    draw_clock(normalFont, (screen.get_size()[0] // 2, font_size * 1.5))

    pygame.display.flip()

pygame.quit()
