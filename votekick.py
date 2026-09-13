import io
import os
import socket
import threading

import pygame
import qrcode
from flask import Flask, Response, jsonify, request
from werkzeug.serving import make_server

from fonts import normal_font

# OBS: WEB LOGIC IS AI GENERATED AT THE MOMENT: CHANGE!!

selected = "PERSON"
votekick = False

font_size = 32
qr_size = 400     # QR image size on screen, in px
margin = 40       # distance of each QR from the left/right screen edge

votes = {"a": 0, "b": 0}
voter_choice = {}
CHOICES = {"YES": "a", "NO": "b"}

_app = Flask(__name__)
_server = None
_server_thread = None

qr_yes_surface = None
qr_no_surface = None


def _get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "localhost"
    finally:
        s.close()


PORT = int(os.environ.get("VOTEKICK_PORT", 3000))
HOST_IP = os.environ.get("VOTEKICK_HOST_IP", _get_local_ip())
BASE_URL = f"http://{HOST_IP}:{PORT}"


@_app.route("/YES")
@_app.route("/NO")
def _vote():
    label = request.path.strip("/").upper()
    choice = CHOICES.get(label)
    if not choice:
        return "Invalid option", 404

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    prev = voter_choice.get(ip)
    if prev != choice:
        if prev:
            votes[prev] = max(0, votes[prev] - 1)
        votes[choice] += 1
        voter_choice[ip] = choice

    display_label = f"KICK {selected}" if choice == "a" else "KEEP"
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body{{font-family:system-ui,sans-serif;background:#111;color:#fff;
        display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center}}
      h1{{font-size:2rem}}
    </style></head>
    <body><h1>Voted for<br>{display_label}</h1></body></html>
    """


@_app.route("/results")
def _results():
    total = votes["a"] + votes["b"]
    pct_a = round(votes["a"] / total * 100) if total else 0
    pct_b = 100 - pct_a if total else 0
    return jsonify(votesA=votes["a"], votesB=votes["b"], total=total,
                    percentA=pct_a, percentB=pct_b)


def _make_qr_surface(label):
    url = f"{BASE_URL}/{label}".upper()
    img = qrcode.make(url, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    surface = pygame.image.load(buf, "qr.png").convert()
    # plain scale (not smoothscale) - blurring a QR code's hard edges hurts scan reliability
    return pygame.transform.scale(surface, (qr_size, qr_size))


def start():
    global selected, votekick, votes, voter_choice, _server, _server_thread
    global qr_yes_surface, qr_no_surface

    selected = input("Who should you votekick: ").upper()
    print(f"Selected person: {selected}")

    votes = {"a": 0, "b": 0}
    voter_choice = {}

    qr_yes_surface = _make_qr_surface("YES")
    qr_no_surface = _make_qr_surface("NO")

    _server = make_server("0.0.0.0", PORT, _app)
    _server_thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _server_thread.start()
    print(f"Votekick server running at {BASE_URL} (scan the YES/NO QR codes to vote)")

    votekick = True


def stop():
    global votekick, _server, _server_thread
    votekick = False
    if _server is not None:
        _server.shutdown()
        _server_thread.join(timeout=2)
        _server = None
        _server_thread = None


def side(screen, colors, x, qr_y, qr_surface, pct, label, bar_color, bar_on_left):
    bar_w, bar_h = 20, 400
    screen.blit(qr_surface, (x, qr_y))

    label_surface, label_rect = normal_font.render(
        f"{label}  {round(pct * 100)}%", fgcolor=colors["text"], size=int(font_size * 0.6)
    )
    screen.blit(label_surface, (x + qr_size // 2 - label_rect.width // 2, qr_y + qr_size + 10))

    bar_x = (x + qr_size + 10) if bar_on_left else (x - 10 - bar_w)
    pygame.draw.rect(screen, (60, 60, 60), (bar_x, qr_y, bar_w, bar_h))
    pygame.draw.rect(screen, bar_color, (bar_x, qr_y, bar_w, bar_h * pct))


timer = 0
def update(dt, screen, colors):
    global timer
    if not votekick:
        return

    screen_w, screen_h = screen.get_size()
    screen.fill(colors["background"])

    title, title_rect = normal_font.render(f"VOTEKICK: {selected}", fgcolor=colors["text"], size=font_size)
    screen.blit(title, (screen_w // 2 - title_rect.width // 2, font_size * 1.5 - title_rect.height // 2))

    total = votes["a"] + votes["b"]
    pct_a = votes["a"] / total if total else 0.5
    pct_b = votes["b"] / total if total else 0.5
    qr_y = screen_h // 2 - qr_size // 2

    if qr_yes_surface is not None:
        side(screen, colors, margin, qr_y, qr_yes_surface, pct_a, "KICK", (0, 120, 255), bar_on_left=True)

    if qr_no_surface is not None:
        no_x = screen_w - margin - qr_size
        side(screen, colors, no_x, qr_y, qr_no_surface, pct_b, "KEEP", (255, 60, 60), bar_on_left=False)

    timer += dt
    timer_height = 20
    duration = 60.0
    remaining = max(0.0, 1.0 - timer / duration)
    fill_w = int(screen.get_width() * remaining)

    pygame.draw.rect(screen, (60, 60, 60), (0, screen.get_height() - timer_height, screen.get_width(), timer_height))
    pygame.draw.rect(screen, (60, 170, 60), (0, screen.get_height() - timer_height, fill_w, timer_height))
