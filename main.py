import pygame
import sys
import bouncy_logo
from datetime import datetime

BASE_WIDTH = 1280
BASE_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
scale = screen.get_width() / BASE_WIDTH
running = True

import flashbang
import randomgifs

# Load fonts
font_path = "./fonts/"
font_size = 112
secret_font = pygame.freetype.Font(font_path + "SecretFont.ttf")
normal_font = pygame.freetype.Font(font_path + "LowEffortFont.ttf", font_size)

# Set the window title
pygame.display.set_caption("LAN")

colors = {
    "text": (255, 255, 255),  # White color for the clock text
    "background": (0, 0, 0),   # Black background
    "default": {
        "text": (255, 255, 255),  # White color for the clock text
        "background": (0, 0, 0)   # Black background
    }
}

def draw_clock(clockFont, position):
    # Draw current time
    now = datetime.now()
    text, rect = clockFont.render(now.strftime("%H:%M:%S"), fgcolor=colors["text"], size=112)
    centered_position = (position[0] - rect.width // 2, position[1] - rect.height // 2)
    screen.blit(text, centered_position)

def fps(dt, font):
    text, rect = font.render(f"{int(clock.get_fps())}",  fgcolor=colors["text"], size=24)
    pos = (screen.get_width() - rect.width, screen.get_height() - rect.height)
    screen.blit(text, pos)

while running:
    dt = clock.tick(120) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flashbang.flashbang()
            if event.key == pygame.K_g:
                randomgifs.start_random_gif()

    screen.fill(colors["background"])
    fps(dt, normal_font)
    bouncy_logo.update(screen)

    draw_clock(normal_font, (screen.get_size()[0] // 2, font_size * 1.5))
    flashbang.update(dt, screen, colors)

    # GIF
    randomgifs.timed(dt)
    randomgifs.draw_random_gif(screen, dt, position=(0, 0))

    pygame.display.flip()

pygame.quit()
