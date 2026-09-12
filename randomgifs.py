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

VIDEO_SIZE = (1080, 720)
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

def start_random_gif():
    global loaded_videos
    global random_video
    random_video = random.choice(loaded_videos)
    random_video.current_frame = 0
    random_video.timer = 0

def draw_random_gif(screen, dt, position=(500, 500)):
    global random_video
    if 'random_video' in globals() and random_video:
        random_video.update(dt)
        random_video.draw(screen, position)