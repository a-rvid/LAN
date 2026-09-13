import re
import random
import string
import pygame

from fonts import secret_font, normal_font

def render(text, color, size=32, obfuscate=True):
    parts = re.split(r"\[(.*?)\]", text)

    surfs = []
    rects = []

    x = 0
    for i, part in enumerate(parts):
        if not part:
            continue  # skip empty segments

        if i % 2 == 0 or not obfuscate:
            surf, rect = normal_font.render(part, color, size=size)
        else:
            fake = ''.join(random.choices(string.ascii_letters, k=len(part)))
            surf, rect = secret_font.render(fake, color, size=size)

        rect.topleft = (x, 0)
        surfs.append(surf)
        rects.append(rect)
        x += rect.width

    if not rects:
        return pygame.Surface((0, 0), pygame.SRCALPHA), (0, 0)

    total_width = sum(r.width for r in rects)
    max_height = max(r.height for r in rects)

    combined = pygame.Surface((total_width, max_height), pygame.SRCALPHA)

    x = 0
    for surf, rect in zip(surfs, rects):
        y_off = max_height - rect.height
        combined.blit(surf, (x, y_off))
        x += rect.width

    return combined, (total_width, max_height)
