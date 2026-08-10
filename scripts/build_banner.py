#!/usr/bin/env python3
"""Render the profile banner to assets/banner.png.

Rasterised rather than SVG on purpose: an SVG served through GitHub's image
proxy cannot load a web font, so the typography would fall back to whatever
serif the viewer's OS happens to have. A PNG renders identically everywhere.

    python scripts/build_banner.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path("C:/Windows/Fonts")

W, H = 1600, 700
SS = 2  # supersample factor, downsampled at the end for clean edges

# Sampled from jonathansolvesproblems.com and the aurora banner, then saturated enough
# to hold up at banner scale. The site's own values are far too dark to read.
BG = (7, 8, 12)
TEAL = (63, 169, 162)
PURPLE = (166, 100, 196)
WHITE = (242, 244, 247)
MUTED = (151, 160, 172)

NAME_A, NAME_B = "Jonathan ", "Andrei"
ROLE_A, ROLE_B = "Senior Full Stack ", "Developer"
LINKS = "github.com/JonathanSolvesProblems      jonathansolvesproblems.com"
SKILLS = "Python   ·   TypeScript   ·   React   ·   Next.js   ·   LLM Agents   ·   RAG   ·   AWS"

PORTRAIT = ROOT / "assets" / "portrait.png"


CONTENT_L, CONTENT_R = 560, W - 70  # text column, in final pixels


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONTS / name
    if not path.exists():
        sys.exit(f"missing font: {path}")
    return ImageFont.truetype(str(path), size * SS)


def fit(name: str, size: int, text: str, draw: ImageDraw.ImageDraw) -> ImageFont.FreeTypeFont:
    """Largest size at or below `size` whose text fits the content column.

    Without this a longer skill list or a longer name silently runs off the
    right edge, which is exactly how "AWS" got clipped the first time.
    """
    limit = (CONTENT_R - CONTENT_L) * SS
    for s in range(size, 8, -1):
        f = font(name, s)
        if draw.textlength(text, font=f) <= limit:
            if s != size:
                print(f"  fit: {name} {size} -> {s} to keep '{text[:28]}...' in frame")
            return f
    return font(name, 8)


def glow(arr: np.ndarray, cx: float, cy: float, rx: float, ry: float,
         color: tuple[int, int, int], strength: float) -> None:
    """Additive radial falloff, in place."""
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - cx * w) / (rx * w)) ** 2 + ((yy - cy * h) / (ry * h)) ** 2)
    f = np.clip(1.0 - d, 0.0, 1.0) ** 2.2
    arr += np.asarray(color, dtype=np.float32) * f[..., None] * strength


def background() -> Image.Image:
    w, h = W * SS, H * SS
    arr = np.zeros((h, w, 3), dtype=np.float32)
    arr[:] = BG

    # Aurora: magenta low and left, teal high and right, matching the site.
    glow(arr, 0.26, 0.74, 0.40, 0.78, PURPLE, 1.05)
    glow(arr, 0.62, 0.92, 0.34, 0.52, PURPLE, 0.55)
    glow(arr, 0.76, 0.24, 0.46, 0.74, TEAL, 0.78)
    glow(arr, 0.52, 0.55, 0.28, 0.45, (40, 60, 90), 0.45)

    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")

    # Concentric arcs, echoing the soft geometry in the reference layout.
    rings = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rings)
    cx, cy = int(w * 0.20), int(h * 0.52)
    for i, r in enumerate((0.44, 0.60, 0.78, 0.98)):
        rr = int(r * h)
        rd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                   outline=(255, 255, 255, 20 - i * 3), width=2 * SS)
    rings = rings.filter(ImageFilter.GaussianBlur(1.5 * SS))
    img = Image.alpha_composite(img.convert("RGBA"), rings).convert("RGB")

    # Vignette so the type sits on a calmer field.
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    v = np.clip(1.0 - 0.42 * np.clip(d - 0.45, 0, None) ** 1.5, 0, 1)
    out = np.asarray(img, dtype=np.float32) * v[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def portrait_disc(diameter: int) -> tuple[Image.Image, Image.Image]:
    """Circular portrait plus a soft outer glow layer."""
    if not PORTRAIT.exists():
        sys.exit(f"missing portrait: {PORTRAIT}\nRun the crop step first.")
    d = diameter * SS
    src = Image.open(PORTRAIT).convert("RGB").resize((d, d), Image.LANCZOS)

    mask = Image.new("L", (d * 4, d * 4), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, d * 4, d * 4], fill=255)
    mask = mask.resize((d, d), Image.LANCZOS)

    disc = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    disc.paste(src, (0, 0), mask)

    # Ring drawn oversized then downsampled, so the stroke stays smooth.
    ring = Image.new("RGBA", (d * 4, d * 4), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([6, 6, d * 4 - 6, d * 4 - 6],
                                 outline=TEAL + (235,), width=10 * SS)
    disc = Image.alpha_composite(disc, ring.resize((d, d), Image.LANCZOS))
    return disc, mask


def main() -> None:
    img = background()
    draw = ImageDraw.Draw(img)

    f_name = fit("constanb.ttf", 112, NAME_A + NAME_B, draw)
    f_role = fit("constanz.ttf", 68, ROLE_A + ROLE_B, draw)   # bold italic
    f_link = fit("constani.ttf", 33, LINKS, draw)
    f_skill = fit("constan.ttf", 31, SKILLS, draw)

    # Portrait on the left.
    D = 330
    disc, _ = portrait_disc(D)
    px, py = int(150 * SS), int((H - D) / 2 * SS)
    halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse(
        [px - 26 * SS, py - 26 * SS, px + (D + 26) * SS, py + (D + 26) * SS],
        fill=TEAL + (46,))
    halo = halo.filter(ImageFilter.GaussianBlur(22 * SS))
    img = Image.alpha_composite(img.convert("RGBA"), halo).convert("RGB")
    img.paste(disc, (px, py), disc)
    draw = ImageDraw.Draw(img)

    x = 560 * SS
    # Name, two-tone.
    y = 268 * SS
    draw.text((x, y), NAME_A, font=f_name, fill=WHITE, anchor="ls")
    draw.text((x + draw.textlength(NAME_A, font=f_name), y), NAME_B,
              font=f_name, fill=TEAL, anchor="ls")

    # Role, two-tone italic, mirroring the name's split.
    y = 372 * SS
    draw.text((x, y), ROLE_A, font=f_role, fill=TEAL, anchor="ls")
    draw.text((x + draw.textlength(ROLE_A, font=f_role), y), ROLE_B,
              font=f_role, fill=WHITE, anchor="ls")

    # Hairline between identity and details.
    ly = 410 * SS
    draw.line([x, ly, int(W * SS - 150 * SS), ly], fill=(255, 255, 255, 40),
              width=max(1, SS // 2))

    draw.text((x, 470 * SS), LINKS, font=f_link, fill=MUTED, anchor="ls")
    draw.text((x, 546 * SS), SKILLS, font=f_skill, fill=WHITE, anchor="ls")

    out = img.resize((W, H), Image.LANCZOS)
    dest = ROOT / "assets" / "banner.jpg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    # JPEG at 92 with no chroma subsampling: 3.4x smaller than PNG here, and
    # checked against the PNG under amplified contrast for banding in the dark
    # aurora gradients, which is the one thing JPEG would plausibly ruin.
    out.save(dest, quality=92, subsampling=0, optimize=True, progressive=True)
    print(f"wrote {dest.relative_to(ROOT)}  {out.size[0]}x{out.size[1]}  "
          f"{dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
