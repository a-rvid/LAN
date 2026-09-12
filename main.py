import pygame
import sys
import flashbang
from datetime import datetime

BASE_WIDTH = 1280
BASE_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
scale = screen.get_width() / BASE_WIDTH
running = True

# Load fonts
font_path = "./fonts/"
font_size = 112
secret_font = pygame.font.Font(font_path + "SecretFont.ttf", font_size)
normal_font = pygame.font.Font(font_path + "LowEffortFont.ttf", font_size)
logo = pygame.image.load("images/logo.png")

# Resize logo
logo_width = int(300 * scale)
logo_height = int(200 * scale)

logo = pygame.transform.smoothscale(logo, (logo_width, logo_height))

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

    screen.fill(colors["background"])
    screen.blit(logo, (500, 500))
    flashbang.video(dt)
    draw_clock(normal_font, (screen.get_size()[0] // 2, font_size * 1.5))

    flashbang.update(dt, colors)

    screen.blit(logo, (500, 500))
    # GIF
    randomgifs.draw_random_gif(screen, dt, position=(0, 0))


    # FPS
    fps_timer += dt
    if fps_timer >= 0.5:
        sys.stdout.write(f"\rFPS: {clock.get_fps():.1f}   ")
        sys.stdout.flush()
        fps_timer = 0.0

    pygame.display.flip()

pygame.quit()
