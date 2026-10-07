#!/usr/bin/env python3
"""Project overview poster for Stalion-Σ 1.1.0-research."""
from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1400, 900
OUT = Path("/home/workdir/artifacts/stalion_sigma_project_poster.png")


def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def rr(d, xy, r, fill, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def main():
    img = Image.new("RGB", (W, H), (12, 16, 24))
    d = ImageDraw.Draw(img)

    # subtle grid
    for x in range(0, W, 70):
        d.line([(x, 0), (x, H)], fill=(22, 30, 42), width=1)
    for y in range(0, H, 70):
        d.line([(0, y), (W, y)], fill=(22, 30, 42), width=1)

    # header bar
    rr(d, (0, 0, W, 110), 0, fill=(18, 26, 38))
    d.rectangle((0, 108, W, 112), fill=(200, 160, 50))

    d.text((W // 2, 36), "STALION-Σ", font=font(42, True), fill=(240, 210, 120), anchor="mt")
    d.text((W // 2, 78), "Research Platform  ·  v1.1.0  ·  Visual Symbiosis  ·  Ethics-First Robotics Kernel",
           font=font(16), fill=(140, 160, 180), anchor="mt")

    # Left: Architecture stack
    rr(d, (40, 140, 520, 520), 12, fill=(18, 26, 38), outline=(60, 90, 130), width=2)
    d.text((280, 160), "ARCHITECTURE", font=font(18, True), fill=(180, 200, 230), anchor="mt")

    layers = [
        ("core.stalion_sigma", "Unified cycle · Pneuma + Logos", (40, 80, 120)),
        ("ethics.ethics_core", "ABSOLUTE_PROHIBITIONS · immutable", (120, 30, 30)),
        ("safety.safety_kernel", "Veto before actuators · scale/hold", (20, 80, 50)),
        ("memory.memory_graph", "Hash-chain · append-only", (50, 60, 90)),
        ("personality + reflection", "Safe trait bounds · self-critique", (50, 70, 100)),
        ("twin.digital_twin", "SAFE mode only · personality params", (40, 70, 90)),
        ("design.visual_symbiosis", "Blueprint motifs ↔ modules", (70, 55, 30)),
    ]
    y = 195
    for name, desc, col in layers:
        rr(d, (60, y, 500, y + 38), 6, fill=col, outline=(100, 140, 180), width=1)
        d.text((80, y + 8), name, font=font(13, True), fill=(230, 240, 255))
        d.text((80, y + 24), desc, font=font(11), fill=(180, 200, 215))
        y += 44

    # Center: Decision flow
    rr(d, (550, 140, 980, 360), 12, fill=(18, 26, 38), outline=(200, 160, 50), width=2)
    d.text((765, 160), "DECISION FLOW", font=font(18, True), fill=(240, 210, 120), anchor="mt")

    stages = [
        ("Sensors", (50, 90, 140)),
        ("Ethics", (140, 35, 35)),
        ("Safety", (25, 100, 60)),
        ("Decision", (40, 80, 130)),
        ("Memory", (90, 70, 30)),
    ]
    sx = 580
    for i, (name, col) in enumerate(stages):
        rr(d, (sx, 220, sx + 70, 280), 8, fill=col, outline=(220, 200, 150), width=1)
        d.text((sx + 35, 250), name, font=font(11, True), fill=(255, 255, 255), anchor="mm")
        if i < len(stages) - 1:
            d.text((sx + 82, 250), "→", font=font(18, True), fill=(200, 160, 50), anchor="mm")
        sx += 78

    d.text((765, 310), "Capability is not permission", font=font(14, True), fill=(240, 200, 100), anchor="mt")
    d.text((765, 335), "Human veto · Always stoppable · No ethics self-mod", font=font(12), fill=(150, 170, 190), anchor="mt")

    # Right: Status / Scope
    rr(d, (1000, 140, 1360, 360), 12, fill=(30, 18, 18), outline=(160, 50, 50), width=2)
    d.text((1180, 160), "SCOPE / SAFETY", font=font(18, True), fill=(255, 160, 160), anchor="mt")
    for j, line in enumerate([
        "✓ Research / simulation only",
        "✓ Ethical AI kernel",
        "✓ Digital Twin (safe)",
        "✓ ROS2 topics bridge",
        "✗ No lethal autonomy",
        "✗ No ethics removal",
        "✗ No unbounded self-mod",
    ]):
        col = (120, 220, 150) if line.startswith("✓") else (255, 140, 140)
        d.text((1020, 200 + j * 22), line, font=font(13), fill=col)

    # Bottom modules strip
    rr(d, (40, 550, 1360, 720), 12, fill=(18, 26, 38), outline=(60, 100, 80), width=2)
    d.text((700, 570), "DELIVERABLES", font=font(18, True), fill=(160, 220, 180), anchor="mt")

    boxes = [
        ("Python Kernel", "stalion_sigma/"),
        ("Ethics + Safety", "immutable veto"),
        ("Visual Symbiosis", "SVG + MP4"),
        ("ROS2 bringup", "pneuma / ethics nodes"),
        ("Gazebo / URDF", "basic world"),
        ("Tests + Sim", "scripts/run_sim"),
    ]
    bx = 60
    for title, sub in boxes:
        rr(d, (bx, 605, bx + 200, 690), 8, fill=(25, 45, 40), outline=(80, 160, 120), width=1)
        d.text((bx + 100, 635), title, font=font(13, True), fill=(200, 240, 210), anchor="mm")
        d.text((bx + 100, 660), sub, font=font(11), fill=(140, 180, 160), anchor="mm")
        bx += 215

    # Footer
    d.text((W // 2, 760), "Stalion-Σ 1.1.0-research  ·  Symbolic-Ethical Cognitive Architecture",
           font=font(14), fill=(120, 140, 160), anchor="mt")
    d.text((W // 2, 790), "For embodied rescue / assistive research  ·  Not a combat product  ·  Not a claim of consciousness",
           font=font(12), fill=(90, 110, 130), anchor="mt")
    d.text((W // 2, 830), "Repository: stalion_sigma/  ·  License: research use  ·  Absolute prohibitions sealed",
           font=font(12), fill=(100, 120, 100), anchor="mt")

    # corner marks
    for cx, cy in [(20, 20), (W - 20, 20), (20, H - 20), (W - 20, H - 20)]:
        d.line([(cx - 12, cy), (cx + 12, cy)], fill=(200, 160, 50), width=2)
        d.line([(cx, cy - 12), (cx, cy + 12)], fill=(200, 160, 50), width=2)

    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
