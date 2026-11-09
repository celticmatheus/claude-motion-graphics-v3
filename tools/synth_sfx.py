"""Gera TODOS os efeitos sonoros do kit por código (ruído, senos e envelopes) — nenhum som baixado.
uso: python synth_sfx.py <pasta_saida>      (precisa de numpy; ffmpeg para os .mp3)
Saída (mesmos nomes que o v3lib/os builds usam): whoosh.mp3 pop.mp3 sparkle.mp3 impact-bass-1.mp3
impact_2.wav riser_1.wav riser_2.wav subboom_1.wav sweepdown_1.wav swish_1.wav  — 48 kHz, estéreo, determinístico.
"""
import sys, wave, subprocess
from pathlib import Path
import numpy as np

SR = 48000
rng = np.random.default_rng(7)
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'sfx'); OUT.mkdir(parents=True, exist_ok=True)


def t(d):
    return np.arange(int(d * SR)) / SR


def env(n, a, r, curve=3.0):
    """ataque linear de a s, queda exponencial até o fim."""
    x = np.arange(n) / SR
    e = np.minimum(1, x / max(a, 1e-4))
    rel = np.clip((x - a) / max(r, 1e-4), 0, 1)
    return e * (1 - rel) ** curve


def lowpass(x, cut):
    """filtro passa-baixa de 1 polo (cut pode variar no tempo)."""
    cut = np.broadcast_to(np.asarray(cut, float), x.shape)
    a = np.exp(-2 * np.pi * cut / SR)
    y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y


def bandnoise(n, lo, hi):
    w = rng.standard_normal(n)
    return lowpass(w, hi) - lowpass(w, lo)


def stereo(x, width=0.15):
    d = int(0.004 * SR)
    l = x; r = np.concatenate([np.zeros(d), x[:-d]]) if d else x
    return np.stack([l * (1 - width) + r * width, r * (1 - width) + l * width], 1)


def norm(x, peak=0.85):
    m = np.max(np.abs(x)) or 1; return x / m * peak


def save(name, x):
    x = np.clip(stereo(norm(x)) if x.ndim == 1 else x, -1, 1)
    wav = OUT / (Path(name).stem + '.wav')
    with wave.open(str(wav), 'wb') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((x * 32767).astype('<i2').tobytes())
    if name.endswith('.mp3'):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-c:a', 'libmp3lame', '-q:a', '2', str(OUT / name)], check=True)
        wav.unlink()
    print('ok', name)


# whoosh — ruído com filtro que abre e fecha (vento passando), 0,57 s
n = int(.57 * SR); x = t(.57)
cut = 300 + 5200 * np.sin(np.pi * np.clip(x / .57, 0, 1)) ** 2
save('whoosh.mp3', lowpass(rng.standard_normal(n), cut) * np.sin(np.pi * x / .57) ** 1.5)

# swish_1 — whoosh curto e mais agudo
n = int(.35 * SR); x = t(.35)
save('swish_1.wav', bandnoise(n, 900, 300 + 7000 * (x / .35)) * env(n, .12, .23, 2))

# pop — bolha: seno que desce de tom, bem curto
x = t(.18); f = 900 * np.exp(-x * 18) + 220
save('pop.mp3', np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(x), .004, .17, 4))

# sparkle — vários sinos agudos em escada
x = t(1.8); s = np.zeros(len(x))
for k, (f0, t0) in enumerate([(2093, 0), (2637, .07), (3136, .14), (4186, .22), (3520, .3), (5274, .38)]):
    i = int(t0 * SR); m = len(x) - i
    s[i:] += (np.sin(2 * np.pi * f0 * x[:m]) + .3 * np.sin(2 * np.pi * f0 * 2.01 * x[:m])) * env(m, .002, 1.2, 5) * (0.9 - .08 * k)
save('sparkle.mp3', s)

# impact-bass-1 — pancada grave: seno que cai de 110 para 38 Hz + estalo de ruído
x = t(2.1); f = 72 * np.exp(-x * 6) + 38
body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(x), .003, 2.0, 2.5)
click = lowpass(rng.standard_normal(len(x)), 2500) * env(len(x), .001, .06, 3) * .6
save('impact-bass-1.mp3', np.tanh(1.6 * (body + click)))

# impact_2 — batida média, mais curta
x = t(.9); f = 140 * np.exp(-x * 14) + 55
save('impact_2.wav', np.tanh(2 * (np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(x), .002, .85, 3)
                                  + lowpass(rng.standard_normal(len(x)), 4000) * env(len(x), .001, .05, 3) * .5)))

# subboom_1 — sub grave longo (troca de mundo / capítulo)
x = t(2.4); f = 55 * np.exp(-x * 2.5) + 30
save('subboom_1.wav', np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(x), .01, 2.3, 2))

# riser_1 / riser_2 — ruído + seno que sobem e param no topo
for name, d, f0, f1 in [('riser_1.wav', 2.0, 200, 1800), ('riser_2.wav', 2.4, 120, 2400)]:
    x = t(d); p = x / d
    tone = np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * p ** 2) / SR) * .35
    noise = lowpass(rng.standard_normal(len(x)), 400 + 7000 * p ** 2)
    save(name, (tone + noise) * p ** 2 * (1 - np.clip((p - .97) / .03, 0, 1)))

# sweepdown_1 — o contrário do riser: desce e some
x = t(1.2); p = x / 1.2
save('sweepdown_1.wav', (lowpass(rng.standard_normal(len(x)), 6000 * (1 - p) + 200) + .3 * np.sin(2 * np.pi * np.cumsum(1500 * (1 - p) + 80) / SR)) * (1 - p) ** 2)
