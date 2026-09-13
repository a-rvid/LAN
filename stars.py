import pygame
import random


class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 3)
        self.color = (255, 255, 255)
        self.alpha = 255

    def update(self, dt):
        # Update the star's position and alpha for twinkling effect
        self.alpha = 255 * (0.5 + 0.5 * random.random())
        self.y += dt * 50  # Move down at a constant speed

        # Reset position if it goes off screen
        if self.y > 720:
            self.y = 0
            self.x = random.randint(0, 1280)

        return True

class meteorite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(30, 50)
        self.color = (255, 255, 255)
        self.alpha = 255

    def update(self, dt):
        # Update the star's position and alpha for twinkling effect
        self.alpha = 255 * (0.5 + 0.5 * random.random())
        self.y += dt * 50  # Move down at a constant speed
        self.x += dt * 50

        # kill the meteorite if it goes off screen
        if self.y > 720+self.size or self.x > 1280+self.size:
            return False

        return True
            

class StarField:
    def __init__(self, num_stars):
        self.stars = [Star(random.randint(0, 1280), random.randint(0, 720)) for _ in range(num_stars)]

    def add_meteorite(self):
        length = random.randint(0, 1280+720)
        if length > 720:
            self.stars.append(meteorite(random.randint(0, 1280), -30))
        else:
            self.stars.append(meteorite(-20, random.randint(0, 720)))

    def update(self, dt):

        if random.random() < 0.01 and len([s for s in self.stars if isinstance(s, meteorite)]) < 5:
            self.add_meteorite()

        # Update all stars and remove any that are no longer active
        for star in self.stars:
            if not star.update(dt):
                self.stars.remove(star)


    def draw(self, screen):
        for star in self.stars:
            pygame.draw.circle(
                screen,
                (star.color[0], star.color[1], star.color[2], star.alpha),
                (star.x, star.y),
                star.size
            )