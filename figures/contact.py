#!/usr/bin/env python
"""Tile the nine production PNGs into out/house-contact.png (3 x 3)."""

from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent / "out"
STEMS = [
    "f01-font-usage-over-time", "f02-variable-font-adoption", "f04-hosting-combinations",
    "f05-woff2-request-share", "f06-format-mix-unique-urls", "f07-resource-hints",
    "f08-font-display", "f09-size-percentiles", "f10-script-coverage",
]
TILE_W, GUTTER, GROUND = 800, 24, (200, 203, 211)


def main():
    tiles = []
    for stem in STEMS:
        im = Image.open(OUT / f"{stem}.png").convert("RGB")
        tiles.append(im.resize((TILE_W, round(im.height * TILE_W / im.width)), Image.LANCZOS))
    th = tiles[0].height
    sheet = Image.new("RGB", (3 * TILE_W + 4 * GUTTER, 3 * th + 4 * GUTTER), GROUND)
    for i, tile in enumerate(tiles):
        r, c = divmod(i, 3)
        sheet.paste(tile, (GUTTER + c * (TILE_W + GUTTER), GUTTER + r * (th + GUTTER)))
    sheet.save(OUT / "house-contact.png")
    print(f"wrote {OUT / 'house-contact.png'}")


if __name__ == "__main__":
    main()
