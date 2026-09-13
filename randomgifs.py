import gifplayer
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

videos = [
    "images/gifs/1.gif",
    "images/gifs/2.gif",
    "images/gifs/3.gif",
    "images/gifs/4.gif",
    "images/gifs/5.gif",
    "images/gifs/6.gif",
    "images/gifs/7.gif"
]

VIDEO_SIZE = (1280, 720)
MAX_WORKERS = 4

print("Loading videos...")
loaded_videos = []

def load_video(video_path):
    """Load one GIF."""
    try:
        video = gifplayer.Gif(
            video_path,
            size=VIDEO_SIZE
        )

        return video_path, video, None

    except Exception as e:
        return video_path, None, e


with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    futures = [
        executor.submit(load_video, path)
        for path in videos
    ]

    for future in as_completed(futures):
        video_path, video, error = future.result()

        if error is not None:
            print(f"Failed to load {video_path}: {error}")
        else:
            loaded_videos.append(video)
            print(f"Loaded {video_path}")

print(f"Loaded {len(loaded_videos)} videos")

random_video = None
random_video_playing = False

gif_time = 0.0
def timed(dt):
    global gif_time
    gif_time += dt
    if gif_time >= 300.0: # 5 minutes
        gif_time = 0
        start_random_gif()

def start_random_gif():
    global random_video
    global random_video_playing

    if not loaded_videos:
        return

    random_video = random.choice(loaded_videos)

    random_video.current_frame = 0
    random_video.timer = 0

    random_video_playing = True

def draw_random_gif(screen, dt, position=(500, 500)):
    global random_video
    global random_video_playing

    if random_video is None or not random_video_playing:
        return

    # Remember which frame we were on
    previous_frame = random_video.current_frame

    # Advance the GIF
    random_video.update(dt)

    # If the frame went backwards, the GIF looped
    if random_video.current_frame < previous_frame:
        # Keep the last frame instead of going back to frame 0
        random_video.current_frame = previous_frame

        # Stop playback
        random_video_playing = False

    random_video.draw(screen, position)
