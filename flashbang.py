import pygame
import cv2
from easing import ease_in_quad, ease_out_quad
from pygame import mixer

# Load video (video won't be used other than flashbang)
cap = cv2.VideoCapture('flashbang.mp4')
success, img = cap.read()
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
shape = img.shape[1::-1]
wn = pygame.display.set_mode(shape)
video_frame_duration = 1 / cap.get(cv2.CAP_PROP_FPS)
video_time_accum = 0.0

flashbang_duration = 2.5  # Duration of the flashbang effect in seconds
ease_time = 0.2  # Duration of the easing effect in seconds
time_since_flashbang = 0.0  # Time since the flashbang effect started
percentage = 0.0  # Percentage of inversion effect applied
is_flashing = False  # Flag to indicate if the flashbang effect is active
flash_delay = 2.55 # delay before flash comes (helps sound)
flash_video = False # starts the video
def flashbang():
    global time_since_flashbang, flash_video, is_flashing
    is_flashing = True
    flash_video = True
    time_since_flashbang = 0 - flash_delay
    # print("flash")
    mixer.music.set_volume(2.0)
    mixer.music.load("flashbang.mp3")
    mixer.music.play()

def update(dt, screen, colors):
    global time_since_flashbang, percentage, is_flashing

    if is_flashing:
        time_since_flashbang += dt

        if time_since_flashbang > 0:
            if time_since_flashbang < ease_time:
                percentage = ease_in_quad(
                    time_since_flashbang / ease_time
                )

            elif time_since_flashbang < flashbang_duration - ease_time:
                percentage = 1.0
                
            elif time_since_flashbang < flashbang_duration:
                # White → black
                percentage = 1 - ease_out_quad(
                    (time_since_flashbang -
                    (flashbang_duration - ease_time)) / ease_time
                )

            else:
                percentage = 0.0
                is_flashing = False

        # Invert colors
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



def video(dt):
    global flash_video, video_time_accum, video_frame_duration, success, img
    if flash_video:
        video_time_accum += dt
        while video_time_accum >= video_frame_duration:
            success, img = cap.read()
            video_time_accum -= video_frame_duration
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                flash_video = False
                break
        if success:
            wn.blit(pygame.image.frombuffer(img.tobytes(), shape, "RGB"), (0, 0))
