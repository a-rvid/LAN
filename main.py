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
import stars

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

star_field = stars.StarField(num_stars=100)

def draw_clock(clockFont, position):
    # Draw current time
    now = datetime.now()
    text, rect = clockFont.render(now.strftime("%H:%M:%S"), fgcolor=colors["text"], size=112)
    centered_position = (position[0] - rect.width // 2, position[1] - rect.height // 2)
    screen.blit(text, centered_position)

def fps_display(dt, font):
    text, rect = font.render(f"{int(clock.get_fps())}",  fgcolor=colors["text"], size=24)
    pos = (screen.get_width() - rect.width, screen.get_height() - rect.height)
    screen.blit(text, pos)

clock.tick(60)

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flashbang.flashbang()
            if event.key == pygame.K_g:
                randomgifs.start_random_gif()

    # Update and draw everything
    # Clear the screen
    screen.fill(colors["background"])

    # Flashbang
    flashbang.update(dt, screen, colors)

    # Stars
    star_field.update(dt)
    star_field.draw(screen)

    # Draw the bouncy logo
    bouncy_logo.update(screen)

    # Text
    draw_clock(normal_font, (screen.get_size()[0] // 2, font_size * 1.5))
    fps_display(dt, normal_font)

    # GIF
    randomgifs.timed(dt)
    randomgifs.draw_random_gif(screen, dt, position=(0, 0))

    pygame.display.flip()

pygame.quit()
