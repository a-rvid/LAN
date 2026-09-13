import pygame
import gifplayer
from easing import ease_in_quad, ease_out_quad
from pygame import mixer

# Load gif for flashbang effect
flashbang_video = gifplayer.Gif(
    './images/flashbang.gif',
    size=(1280, 720)
)

flashbang_duration = 3.5  # Duration of the flashbang effect in seconds
ease_in_time = 0.1  # Duration of the easing effect in seconds
ease_out_time = 2  # Duration of the easing effect in seconds

time_since_flashbang = 0.0  # Time since the flashbang effect started
percentage = 0.0  # Percentage of inversion effect applied

is_flashing = False  # Flag to indicate if the flashbang effect is active
flash_delay = 1.75 # delay before flash comes (helps sound)

flash_video = False # starts the video

def flashbang():
    global flash_video, time_since_flashbang, is_flashing

    is_flashing = True
    flash_video = True

    # Reset GIF
    flashbang_video.current_frame = 0
    flashbang_video.timer = 0

    # Start before the actual flash
    time_since_flashbang = -flash_delay

    mixer.music.set_volume(2.0)
    mixer.music.load("flashbang.mp3")
    mixer.music.play()


def update(dt, screen, colors):
    global flash_video, time_since_flashbang, percentage, is_flashing

    if not is_flashing:
        return

    time_since_flashbang += dt

    if time_since_flashbang > 0:

        # Fade in
        if time_since_flashbang < ease_in_time:

            percentage = ease_in_quad(
                time_since_flashbang / ease_in_time
            )

        # Full flash
        elif time_since_flashbang < flashbang_duration - ease_out_time:

            percentage = 1.0

        # Fade out
        elif time_since_flashbang < flashbang_duration:

            percentage = 1 - ease_out_quad(
                (
                    time_since_flashbang -
                    (flashbang_duration - ease_out_time)
                ) / ease_out_time
            )

        # Finished
        else:
            percentage = 0.0
            is_flashing = False

    # Apply color inversion
    default_text = colors["default"]["text"]
    default_background = colors["default"]["background"]

    colors["text"] = tuple(
        int(c * (1 - percentage) + (255 - c) * percentage)
        for c in default_text
    )

    colors["background"] = tuple(
        int(c * (1 - percentage) + (255 - c) * percentage)
        for c in default_background
    )

    if not flash_video:
        return

    previous_frame = flashbang_video.current_frame

    flashbang_video.update(dt)

    # Detect GIF looping back to frame 0
    if flashbang_video.current_frame < previous_frame:

        flash_video = False

        # Keep the GIF ready for the next flash
        flashbang_video.current_frame = 0
        flashbang_video.timer = 0

        return

    flashbang_video.draw(screen, (0, 0))
