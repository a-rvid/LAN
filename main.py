import pygame
import time
import threading
import math
from pygame import mixer
from datetime import datetime

pygame.init()
mixer.init()
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

class EasingBase:
    limit = (0, 1)

    def __init__(self, start=0, end=1, duration=1):
        self.start = start
        self.end = end
        self.duration = duration

    def func(self, t):
        raise NotImplementedError

    def ease(self, alpha):
        t = self.limit[0] * (1 - alpha) + self.limit[1] * alpha
        a = self.func(t)
        return self.end * a + self.start * (1 - a)

    def __call__(self, alpha):
        return self.ease(alpha)

class QuadEaseInOut(EasingBase):
    def func(self, t: float) -> float:
        if t < 0.5:
            return 2 * t * t
        return (-2 * t * t) + (4 * t) - 1


class QuadEaseIn(EasingBase):
    def func(self, t: float) -> float:
        return t * t


class QuadEaseOut(EasingBase):
    def func(self, t: float) -> float:
        return -(t * (t - 2))

def draw_clock(clockFont, position):
    # Draw current time
    now = datetime.now()
    text = clockFont.render(now.strftime("%H:%M:%S"), True, (255, 255, 255))
    centered_position = (position[0] - text.get_width() // 2, position[1] - text.get_height() // 2)
    screen.blit(text, centered_position)

flashbang_duration = 2.5  # Duration of the flashbang effect in seconds
easeTime = 0.2  # Duration of the easing effect in seconds
time_since_flashbang = 0.0  # Time since the flashbang effect started
percentage = 0.0  # Percentage of inversion effect applied
is_flashing = False  # Flag to indicate if the flashbang effect is active
def flashbang():
    global time_since_flashbang, is_flashing
    is_flashing = True
    print("flash")
    mixer.music.set_volume(2.0)
    mixer.music.load("flashbang.mp3")
    mixer.music.play()
    time_since_flashbang = 0.0

def update_flashbang(dt):
    global time_since_flashbang, percentage, is_flashing

    time_since_flashbang += dt

    if time_since_flashbang < easeTime:
        ease = QuadEaseInOut(0, 1, easeTime)
        percentage = ease(time_since_flashbang / easeTime)

    elif time_since_flashbang < flashbang_duration - easeTime:
        percentage = 1.0

    elif time_since_flashbang < flashbang_duration:
        ease = QuadEaseInOut(1, 0, easeTime)
        alpha = (time_since_flashbang -
                 (flashbang_duration - easeTime)) / easeTime
        percentage = ease(alpha)

    else:
        percentage = 0.0
        is_flashing = False


while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flashbang()

    screen.fill((0, 0, 0))

    draw_clock(normalFont, (screen.get_size()[0] // 2, font_size * 1.5))

    if is_flashing:
        update_flashbang(dt)
        pixels = pygame.surfarray.pixels3d(screen)
        #print(percentage)
        pixels[:] = pixels * (1 - percentage) + (255 - pixels) * percentage
        del pixels

    pygame.display.flip()

pygame.quit()
