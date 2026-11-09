"""Gera as texturas do kit por código: grain.png (grão de filme) e leaves.png (sombra de folhas para o mundo "papel").
uso: python make_textures.py <pasta_saida>      (precisa de numpy + pillow)
"""
import sys, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'img'); OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(11)

# grão: ruído cinza em volta de 128, 512x512, ladrilhável
g = np.clip(128 + rng.normal(0, 38, (512, 512)), 0, 255).astype(np.uint8)
Image.fromarray(g, 'L').convert('RGB').save(OUT / 'grain.png')

# folhas: silhuetas de folhas de palmeira em cinza, desfocadas (usar com mix-blend-mode: multiply)
W, H = 1400, 2000
im = Image.new('L', (W, H), 255); d = ImageDraw.Draw(im)
for _ in range(9):
    x0, y0 = rng.uniform(-200, W + 200), rng.uniform(-200, H + 200)
    ang = rng.uniform(0, 2 * math.pi); L = rng.uniform(500, 900)
    x1, y1 = x0 + L * math.cos(ang), y0 + L * math.sin(ang)
    d.line([(x0, y0), (x1, y1)], fill=150, width=10)
    for k in range(26):
        f = k / 26; cx, cy = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
        for side in (-1, 1):
            a2 = ang + side * rng.uniform(.7, 1.1); ll = 240 * math.sin(math.pi * (0.15 + .8 * f))
            pts = [(cx, cy), (cx + ll * math.cos(a2 - .08), cy + ll * math.sin(a2 - .08)),
                   (cx + ll * math.cos(a2 + .08), cy + ll * math.sin(a2 + .08))]
            d.polygon(pts, fill=int(rng.uniform(120, 165)))
im = im.filter(ImageFilter.GaussianBlur(14))
Image.merge('RGBA', [im, im, im, Image.new('L', (W, H), 255)]).save(OUT / 'leaves.png')
print('ok', OUT / 'grain.png', OUT / 'leaves.png')
