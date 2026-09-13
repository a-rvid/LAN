import pygame
import pygame.freetype
pygame.freetype.init()
font_path = "./fonts/"
secret_font = pygame.freetype.Font(font_path + "SecretFont.ttf")
normal_font = pygame.freetype.Font(font_path + "LowEffortFont.ttf")
