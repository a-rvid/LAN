import pygame
import time
import threading
import numpy
from pygame import mixer
from datetime import datetime

pygame.init()
mixer.init()
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

invert = False
def flashbang():
    global invert
    print("flash")
    size_multiplier = 1.0
    mixer.music.set_volume(2.0)
    mixer.music.load("flashbang.mp3")
    mixer.music.play()
    time.sleep(2.5)
    invert = True
    time.sleep(1)
    invert = False


threading.Thread(target=flashbang, daemon=True).start()


while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                threading.Thread(
                    target=flashbang,
                    daemon=True
                ).start()

    screen.fill((0, 0, 0))

    draw_clock(font, screen.get_size())

    if invert:
        pixels = pygame.surfarray.pixels3d(screen)
        pixels[:] = 255 - pixels
        del pixels

    pygame.display.flip()

pygame.quit()
