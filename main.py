import pygame
import sys
import random
import string
import bouncy_logo
from datetime import datetime
from fonts import secret_font, normal_font
import formatting

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
import events

font_size = 112
font_path = "fonts/"
secret_font = pygame.freetype.Font(font_path + "SecretFont.ttf")
normal_font = pygame.freetype.Font(font_path + "LowEffortFont.ttf", font_size)
event_font = pygame.freetype.Font(font_path + "LowEffortFont.ttf", 24)

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

event_manager = events.LanEventManager("events.json")
print("Loaded events:")
for event in event_manager.get_events():
    print(event)

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

show = False
def server(frames):
    ip = "123.456.789.101"
    bedrock = "19132"
    text, (w, h) = formatting.render(f"PORT: [{bedrock}]", colors["text"], size=64, obfuscate=not show)
    screen.blit(text, (0, screen.get_height() - (h * 2 + 10)))
    text, (w, h) = formatting.render(f"IP: [{ip}]", colors["text"], size=64, obfuscate=not show)
    screen.blit(text, (0, screen.get_height() - h))

frames = 0
while running:
    dt = clock.tick(30) / 1000.0
    frames += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flashbang.flashbang()
            if event.key == pygame.K_g:
                randomgifs.start_random_gif()
            if event.key == pygame.K_s:
                show = not show

    # Update and draw everything
    # Clear the screen
    screen.fill(colors["background"])

    # Stars
    star_field.update(dt)
    star_field.draw(screen)

    # Events
    event_manager.display_events(
        screen,
        event_font,
            (
            (screen.get_size()[0] - 24*19) + 30,
            (screen.get_size()[1] - 24*13) - 30
            ),
        size=(24*19 - 30,
              24*13 + 30),
        border=10
)

    # Draw the bouncy logo
    bouncy_logo.update(screen)

    # Text
    draw_clock(normal_font, (screen.get_size()[0] // 2, font_size * 1.5))
    fps_display(dt, normal_font)
    server(frames)
    flashbang.update(dt, screen, colors)

    # GIF
    randomgifs.timed(dt)
    randomgifs.draw_random_gif(screen, dt, position=(0, 0))

    pygame.display.flip()

pygame.quit()
