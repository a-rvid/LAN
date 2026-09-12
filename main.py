import pygame
import sys
from datetime import datetime

import flashbang
import randomgifs

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
running = True

# Load fonts
font_path = "./fonts/"
font_size = 112
secret_font = pygame.font.Font(font_path + "SecretFont.ttf", font_size)
normal_font = pygame.font.Font(font_path + "LowEffortFont.ttf", font_size)

# Set the window title
pygame.display.set_caption("Digital Clock")

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
    text = clockFont.render(now.strftime("%H:%M:%S"), True, colors["text"])
    centered_position = (position[0] - text.get_width() // 2, position[1] - text.get_height() // 2)
    screen.blit(text, centered_position)

fps_timer = 0.0
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flashbang.flashbang()
            elif event.key == pygame.K_g:
                randomgifs.start_random_gif()

    screen.fill(colors["background"])
    flashbang.video(dt)
    draw_clock(normal_font, (screen.get_size()[0] // 2, font_size * 1.5))

    # Flashbang
    flashbang.update(dt, colors)

    # GIF
    

    # FPS
    fps_timer += dt
    if fps_timer >= 0.5:
        sys.stdout.write(f"\rFPS: {clock.get_fps():.1f}   ")
        sys.stdout.flush()
        fps_timer = 0.0

    pygame.display.flip()

pygame.quit()
