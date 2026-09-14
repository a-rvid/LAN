import pygame
import json


class LanEvent:
    def __init__(self, time, name):
        self.time = time
        self.name = name
        self.is_done = False

    def __str__(self):
        return f"{self.time} - {self.name}"

class LanEventManager:
    def __init__(self, event_file):
        self.events = []
        self.load_events(event_file)

    def load_events(self, event_file):
        with open(event_file, 'r') as f:
            data = json.load(f)
            for event in data:
                lan_event = LanEvent(event['time'], event['name'])
                self.events.append(lan_event)

    def get_events(self):
        return self.events

    def display_events(self, screen, font, position, size=(300, 500), border=10, colors=None):

        # Draw a semi-transparent background for the event list
        pygame.draw.rect(
            screen,
            (128, 128, 128, 150) if colors is None else colors["background"],
            pygame.Rect(position[0], position[1], size[0], size[1]),
            border_radius=border
        )

        # Draw the event list
        y_offset = border
        for event in self.events:
            # Render the event text
            text_surface, _ = font.render(str(event), fgcolor=(255, 255, 255) if colors is None else colors["text"])

            screen.blit(text_surface, (position[0] + border, position[1] + y_offset))

            # Increment the y_offset for the next event
            y_offset += text_surface.get_height() + border