#!/usr/bin/env python3
"""Render animated Stalion-Σ symbiosis diagram frames → MP4 via ffmpeg."""
from __future__ import annotations

import math
import os
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FPS = 24
DURATION = 8  # seconds
N_FRAMES = FPS * DURATION

OUT_DIR = Path("/home/workdir/artifacts/stalion_sigma_frames")
OUT_MP4 = Path("/home/workdir/artifacts/stalion_sigma_symbiosis_animated.mp4")


def font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def lerp(a, b, t):
    return a + (b - a) * t


def clamp01(x):
    return max(0.0, min(1.0, x))


def draw_round_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def particle_pos(t, path):
    """t in [0,1] along polyline path [(x,y), ...]"""
    if t <= 0:
        return path[0]
    if t >= 1:
        return path[-1]
    # equal segment approximation
    segs = []
    total = 0.0
    for i in range(len(path) - 1):
        x0, y0 = path[i]
        x1, y1 = path[i + 1]
        d = math.hypot(x1 - x0, y1 - y0)
        segs.append((d, x0, y0, x1, y1))
        total += d
    if total < 1e-6:
        return path[0]
    dist = t * total
    for d, x0, y0, x1, y1 in segs:
        if dist <= d:
            u = dist / d if d > 0 else 0
            return (lerp(x0, x1, u), lerp(y0, y1, u))
        dist -= d
    return path[-1]


def render_frame(i: int) -> Image.Image:
    t = i / max(1, N_FRAMES - 1)  # 0..1 over whole video
    phase = (i / FPS)  # seconds

    img = Image.new("RGB", (W, H), (15, 20, 28))
    d = ImageDraw.Draw(img)

    # grid
    for x in range(0, W, 80):
        d.line([(x, 0), (x, H)], fill=(30, 40, 52), width=1)
    for y in range(0, H, 80):
        d.line([(0, y), (W, y)], fill=(30, 40, 52), width=1)

    f_title = font(28, bold=True)
    f_sub = font(14)
    f_card = font(13, bold=True)
    f_small = font(11)
    f_flow = font(12, bold=True)

    # title pulse
    title_alpha_boost = 0.5 + 0.5 * math.sin(phase * 2.0)
    title_color = (int(200 + 40 * title_alpha_boost), int(180 + 30 * title_alpha_boost), int(80 + 20 * title_alpha_boost))
    d.text((W // 2, 28), "STALION-Σ  ·  VISUAL SYMBIOSIS", font=f_title, fill=title_color, anchor="mt")
    d.text((W // 2, 58), "Blueprint motifs  ↔  Software modules   ·   Capability ≠ Permission",
           font=f_sub, fill=(120, 140, 160), anchor="mt")

    # Left column motifs
    motifs = [
        ("Humanoid Frame", "anatomical body"),
        ("Exoskeleton Mark IV", "piston / actuators"),
        ("Exploded Plates", "modular sheets"),
        ("Authority Boundary", "capability ≠ permission"),
        ("Resonance Coil", "coherence metaphor"),
        ("Sensor Head Cluster", "perception stack"),
    ]
    modules = [
        ("core.stalion_sigma", "unified cycle", (26, 40, 58), (74, 130, 190)),
        ("safety.safety_kernel", "veto / scale", (13, 55, 38), (45, 160, 95)),
        ("memory · personality · twin", "safe twin only", (26, 40, 58), (74, 130, 190)),
        ("ethics.ethics_core", "ABSOLUTE PROHIBITIONS", (80, 20, 20), (220, 70, 70)),
        ("reflection_layer", "self-critique", (26, 40, 58), (74, 130, 190)),
        ("edge / sensors", "perception", (26, 40, 58), (74, 130, 190)),
    ]

    left_x, right_x = 40, 720
    card_w, card_h = 300, 52
    start_y = 90
    gap = 60

    for idx, ((mt, ms), (mod, mdesc, fill, border)) in enumerate(zip(motifs, modules)):
        appear = clamp01((phase - idx * 0.25) / 0.4)
        if appear <= 0:
            continue
        y = start_y + idx * gap
        # left card
        is_auth = idx == 3
        pulse = 0.5 + 0.5 * math.sin(phase * 3 + idx)
        left_border = (220, 80, 80) if is_auth else (200, 160, 50)
        if is_auth:
            left_border = (int(180 + 50 * pulse), int(50 + 30 * pulse), int(50 + 30 * pulse))
        alpha_fill = (30, 35, 45) if appear > 0.3 else (20, 25, 32)
        draw_round_rect(d, (left_x, y, left_x + card_w, y + card_h), 6, fill=alpha_fill, outline=left_border, width=2 if is_auth else 1)
        d.text((left_x + card_w // 2, y + 16), mt, font=f_card, fill=(240, 210, 140) if not is_auth else (255, 180, 180), anchor="mt")
        d.text((left_x + card_w // 2, y + 36), ms, font=f_small, fill=(140, 150, 165), anchor="mt")

        # right card
        bw = 2 if idx == 3 else 1
        if idx == 3:
            border = (int(200 + 40 * pulse), int(60 + 40 * pulse), int(60 + 20 * pulse))
        draw_round_rect(d, (right_x, y, right_x + 360, y + card_h), 6, fill=fill, outline=border, width=bw)
        d.text((right_x + 180, y + 16), mod, font=f_card, fill=(220, 235, 255) if idx != 3 else (255, 220, 220), anchor="mt")
        d.text((right_x + 180, y + 36), mdesc, font=f_small, fill=(140, 170, 150) if idx == 1 else (130, 150, 170), anchor="mt")

        # connection line + particle
        path = [
            (left_x + card_w, y + card_h // 2),
            (520, y + card_h // 2),
            (520, y + card_h // 2),
            (right_x, y + card_h // 2),
        ]
        line_col = (220, 80, 80) if is_auth else (180, 150, 60)
        d.line([path[0], path[1], path[3]], fill=line_col, width=2)
        # dashed offset illusion via particle
        pt = (phase * 0.35 + idx * 0.12) % 1.0
        px, py = particle_pos(pt, [path[0], path[1], path[3]])
        r = 5 if is_auth else 4
        d.ellipse((px - r, py - r, px + r, py + r), fill=(255, 100, 100) if is_auth else (240, 210, 100))

    # Bottom pipeline
    pipe_y = 520
    draw_round_rect(d, (40, pipe_y, 1080, pipe_y + 130), 10, fill=(12, 16, 22), outline=(200, 160, 50), width=2)
    d.text((560, pipe_y + 18), "ПОТОК РЕШЕНИЯ  ·  Capability ≠ Permission", font=f_flow, fill=(240, 210, 140), anchor="mt")

    stages = [
        ("Sensors", "observe", (36, 52, 72), (74, 130, 190)),
        ("Ethics Gate", "BLOCK / OK", (80, 20, 20), (220, 70, 70)),
        ("Safety Veto", "scale / hold", (13, 55, 38), (45, 160, 95)),
        ("Decision", "cmd / hold", (26, 50, 80), (70, 140, 200)),
        ("Memory", "hash-chain", (55, 40, 25), (200, 160, 50)),
    ]
    stage_w, stage_h = 130, 55
    sx0 = 70
    sgap = 160
    centers = []
    cycle = (phase % 5.0)  # which stage highlighted
    for si, (name, sub, fill, border) in enumerate(stages):
        sx = sx0 + si * sgap
        sy = pipe_y + 45
        centers.append((sx + stage_w // 2, sy + stage_h // 2))
        active = abs(cycle - si) < 0.6 or (si == 0 and cycle > 4.4)
        bw = 3 if active else 1
        bcol = tuple(min(255, c + 40) for c in border) if active else border
        draw_round_rect(d, (sx, sy, sx + stage_w, sy + stage_h), 6, fill=fill, outline=bcol, width=bw)
        d.text((sx + stage_w // 2, sy + 16), name, font=f_flow, fill=(255, 255, 255), anchor="mt")
        d.text((sx + stage_w // 2, sy + 36), sub, font=f_small, fill=(180, 190, 200), anchor="mt")
        if si < len(stages) - 1:
            d.text((sx + stage_w + 15, sy + stage_h // 2), "→", font=font(20, True), fill=(200, 160, 50), anchor="mm")

    # traveling token on pipeline
    pipe_path = centers
    pt = (phase / 5.0) % 1.0
    tx, ty = particle_pos(pt, pipe_path)
    d.ellipse((tx - 8, ty - 8, tx + 8, ty + 8), fill=(240, 210, 100), outline=(255, 240, 180))
    d.ellipse((tx - 3, ty - 3, tx + 3, ty + 3), fill=(255, 255, 220))

    # Right excluded panel
    draw_round_rect(d, (1100, 90, 1255, 320), 8, fill=(30, 15, 15), outline=(160, 50, 50), width=2)
    d.text((1177, 110), "НЕ РЕАЛИЗУЕТСЯ", font=f_flow, fill=(255, 160, 160), anchor="mt")
    for j, line in enumerate([
        "✗ explosives",
        "✗ cutting weapons",
        "✗ lethal effectors",
        "✗ disable_veto",
        "✗ unbounded self-mod",
        "",
        "Twin: personality only",
    ]):
        col = (255, 140, 140) if "Twin" in line else (200, 140, 140)
        d.text((1115, 145 + j * 22), line, font=f_small, fill=col)

    # Creed
    draw_round_rect(d, (1100, 340, 1255, 480), 8, fill=(20, 30, 42), outline=(70, 120, 180), width=1)
    d.text((1177, 358), "CREED", font=f_flow, fill=(160, 190, 220), anchor="mt")
    d.text((1115, 390), "Ability ≠ authority.", font=f_small, fill=(200, 180, 120))
    d.text((1115, 412), "Human-controlled.", font=f_small, fill=(160, 175, 190))
    d.text((1115, 434), "Always stoppable.", font=f_small, fill=(160, 175, 190))

    # footer
    d.text((W // 2, H - 28), "Stalion-Σ 1.1.0-research  ·  Animated Visual Symbiosis  ·  Research only",
           font=f_small, fill=(90, 105, 120), anchor="mt")

    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Rendering {N_FRAMES} frames @ {FPS} fps → {OUT_DIR}")
    for i in range(N_FRAMES):
        frame = render_frame(i)
        frame.save(OUT_DIR / f"frame_{i:04d}.png")
        if i % 24 == 0:
            print(f"  frame {i}/{N_FRAMES}")

    tmp = OUT_MP4.with_suffix(".tmp.mp4")
    if tmp.exists():
        tmp.unlink()
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(OUT_DIR / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "20",
        "-preset", "medium",
        "-movflags", "+faststart",
        str(tmp),
    ]
    print("Encoding MP4...")
    subprocess.run(cmd, check=True, capture_output=True)
    subprocess.run(["ffprobe", "-v", "error", str(tmp)], check=True)
    tmp.rename(OUT_MP4)
    print(f"OK: {OUT_MP4}")
    # also make a short gif preview
    gif_path = Path("/home/workdir/artifacts/stalion_sigma_symbiosis_preview.gif")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(OUT_MP4),
        "-vf", "fps=12,scale=640:-1:flags=lanczos",
        "-loop", "0",
        str(gif_path),
    ], check=True, capture_output=True)
    print(f"GIF: {gif_path}")


if __name__ == "__main__":
    main()
