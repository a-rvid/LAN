import pygame

logo = pygame.image.load("images/logo.png")
logo = pygame.transform.smoothscale_by(logo, 0.2)
logo_width, logo_height = logo.get_size()

posX = 0
posY = 0
velocity = 2
velocityX = velocity
velocityY = velocity

def update(screen):
    global posX, posY, velocityX, velocityY
    posX += velocityX
    posY += velocityY
    screen.blit(logo, (posX, posY))
    if(posX + logo_width >= screen.get_width() or posX <= 0):
        velocityX *= -1
    if(posY + logo_height >= screen.get_height() or posY <= 0):
        velocityY *= -1
