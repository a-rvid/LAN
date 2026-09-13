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
        self.y += dt * 20  # Move down at a constant speed

        # Reset position if it goes off screen
        if self.y > 720:
            self.y = 0
            self.x = random.randint(0, 1280)

        return True

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (self.color[0], self.color[1], self.color[2], self.alpha),
            (self.x, self.y),
            self.size
        )

class shootingStar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(3, 7)
        self.color = (255, 255, 255)
        self.alpha = 255
        self.fire_particles = []

    def update(self, dt):
        # Update the star's position and alpha for twinkling effect
        self.alpha = 255 * (0.5 + 0.5 * random.random())
        self.y += dt * 300  # Move down at a constant speed
        self.x += dt * 300

        # Update fire particles
        for particle in self.fire_particles:
            if not particle.update(dt):
                self.fire_particles.remove(particle)

        #add fire particles
        if random.random() < 0.5:
            self.fire_particles.append(fireparticle(self.x, self.y))

        # kill the shooting star if it goes off screen
        if self.y > 720+self.size+400 or self.x > 1280+self.size+400:
            return False

        return True

    def draw(self, screen):
        for particle in self.fire_particles:
            particle.draw(screen)
        pygame.draw.circle(
            screen,
            (self.color[0], self.color[1], self.color[2], self.alpha),
            (self.x, self.y),
            self.size
        )

class fireparticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = random.uniform(-70, -50)
        self.velocity_y = random.uniform(-70, -50)
        self.size = random.randint(1, 3)
        self.color = pygame.Color(0, 0, 0)
        self.color.hsla = (0, 100, 100, 100)
        self.age = 0.0


    def update(self, dt):
        # Update the star's position and alpha for twinkling effect
        self.color.a = int(255 * (0.5 + 0.5 * random.random()))
        self.y += dt * self.velocity_y
        self.x += dt * self.velocity_x

        self.age += dt

        # kill the fireparticle if it is older than 1 second
        if self.age > 1.0:
            return False

        return True

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.size
        )
            

class StarField:
    def __init__(self, num_stars):
        self.stars = [Star(random.randint(0, 1280), random.randint(0, 720)) for _ in range(num_stars)]

    def add_shooting_star(self):
        length = random.randint(0, 1280+720)
        if length > 720:
            self.stars.append(shootingStar(length-720, -50))
        else:
            self.stars.append(shootingStar(-50, length))

    def update(self, dt):

        if random.random() < 0.01 and len([s for s in self.stars if isinstance(s, shootingStar)]) < 5:
            self.add_shooting_star()

        # Update all stars and remove any that are no longer active
        for star in self.stars:
            if not star.update(dt):
                self.stars.remove(star)


    def draw(self, screen):
        for star in self.stars:
            star.draw(screen)