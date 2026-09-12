import pygame
from PIL import Image


class Gif:
    def __init__(self, filename, size=None):
        self.image = Image.open(filename)

        self.frames = []
        self.durations = []

        for frame in range(self.image.n_frames):
            self.image.seek(frame)

            frame_image = self.image.convert("RGBA")

            if size is not None:
                frame_image = frame_image.resize(
                    size,
                    Image.Resampling.BILINEAR
                )

            surface = pygame.image.frombytes(
                frame_image.tobytes(),
                frame_image.size,
                "RGBA"
            ).convert_alpha()

            self.frames.append(surface)

            duration = self.image.info.get("duration", 100)
            self.durations.append(duration / 1000.0)

        self.current_frame = 0
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt

        while self.timer >= self.durations[self.current_frame]:
            self.timer -= self.durations[self.current_frame]

            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                self.current_frame = 0

    def draw(self, screen, position):
        screen.blit(
            self.frames[self.current_frame],
            position
        )
