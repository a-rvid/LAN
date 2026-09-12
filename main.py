import pygame
import sys
import time
import threading
import math
import cv2
import flashbang
from pygame import mixer
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.mouse.set_visible(False)
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

fps_timer = 0.0
while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flashbang.flashbang()

    screen.fill((0, 0, 0))
    flashbang.video(dt)
    draw_clock(normalFont, (screen.get_size()[0] // 2, font_size * 1.5))

    flashbang.update(dt, screen)

    fps_timer += dt
    if fps_timer >= 0.5:
        sys.stdout.write(f"\rFPS: {clock.get_fps():.1f}   ")
        sys.stdout.flush()
        fps_timer = 0.0

    pygame.display.flip()

pygame.quit()
