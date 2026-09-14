import pygame

def loading_bar(screen, x, y, size, progress):
    # Draw the loading bar
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, size[0], size[1]), width=2)
    pygame.draw.rect(screen, (255, 255, 255), (x, y, size[0] * progress, size[1]))

class loading:
    def __init__(self):
        self.loading = True
        
