#!/usr/bin/env python3
"""Sonidos nuevos para Mokoshotar, sintetizados desde cero (sin muestras externas).

ataque_mordisco_1/2 : se disparan al iniciar el salto (fotograma 7); el impacto suena a +0,200 s (= fotograma 13)
hechizo_escarcha_1/2: se disparan en el fotograma 9; la liberación suena a +0,233 s (= fotograma 16)
critico_aullido     : aullido de lobo para el golpe crítico
Salida: WAV 44,1 kHz 16 bit + OGG Vorbis, y espectrogramas de control.
uso: sfx_moko.py out_dir
"""
import sys, os, json
import numpy as np
from scipy import signal
from scipy.io import wavfile

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
SR = 44100
rng = np.random.default_rng(2026)


def t_(d):
    return np.arange(int(d * SR)) / SR


def env(n, a, d, sustain=0.0, curve=4.0):
    """envolvente ataque lineal + caída exponencial"""
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-6), np.exp(-(t - a) * curve / max(d, 1e-6)))
    return np.maximum(e, 0) * (1 - sustain) + sustain * (t < a + d)


def bp(x, lo, hi, order=4):
    sos = signal.butter(order, [lo, hi], btype='band', fs=SR, output='sos')
    return signal.sosfilt(sos, x)


def lp(x, f, order=4):
    return signal.sosfilt(signal.butter(order, f, btype='low', fs=SR, output='sos'), x)


def hp(x, f, order=4):
    return signal.sosfilt(signal.butter(order, f, btype='high', fs=SR, output='sos'), x)


def place(buf, x, at):
    x = np.array(x, dtype=float)
    k = min(len(x), int(0.04 * SR))
    if k > 1:
        x[-k:] *= np.linspace(1, 0, k)   # sin cortes bruscos al final de cada capa
    i = int(at * SR)
    n = min(len(x), len(buf) - i)
    buf[i:i + n] += x[:n]


def sweep_noise(d, f0, f1, q=0.5):
    """ruido filtrado con banda móvil (whoosh)"""
    n = int(d * SR)
    x = rng.standard_normal(n)
    y = np.zeros(n)
    blk = 512
    zi = None
    for i in range(0, n, blk):
        t = i / max(n - 1, 1)
        fc = f0 * (f1 / f0) ** t
        lo, hi = fc * (1 - q / 2), min(fc * (1 + q / 2), SR / 2 - 100)
        sos = signal.butter(2, [lo, hi], btype='band', fs=SR, output='sos')
        if zi is None:
            zi = signal.sosfilt_zi(sos) * 0
        y[i:i + blk], zi = signal.sosfilt(sos, x[i:i + blk], zi=zi)
    return y


def reverb(x, dur=1.2, mix=0.25, damp=3500):
    n = int(dur * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 5.5 / dur)
    ir = lp(ir, damp)
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = signal.fftconvolve(x, ir)
    dry = np.concatenate([x, np.zeros(len(wet) - len(x))])
    return dry * (1 - mix) + wet * mix


def bells(d, freqs, decay=1.2, amp=1.0):
    t = t_(d)
    y = np.zeros_like(t)
    for k, f in enumerate(freqs):
        ph = rng.uniform(0, 2 * np.pi)
        y += np.sin(2 * np.pi * f * t + ph) * np.exp(-t * (2 + k * 0.7) / decay) / (1 + 0.3 * k)
    return y * amp


def crunch(d=0.09):
    n = int(d * SR)
    x = rng.standard_normal(n) * env(n, 0.001, d * 0.6, curve=6)
    clicks = np.zeros(n)
    for _ in range(14):
        i = rng.integers(0, n - 50)
        clicks[i:i + 30] += rng.standard_normal(30) * rng.uniform(0.5, 1.2)
    return bp(x, 1800, 7000) * 0.8 + hp(clicks, 3000) * 0.6


def thump(d=0.18, f=75):
    t = t_(d)
    fr = f * (1 + 1.5 * np.exp(-t * 40))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 22)


def growl(d, f0=95, jitter=0.12):
    t = t_(d)
    f = f0 * (1 + jitter * lp(rng.standard_normal(len(t)), 25) * 4)
    saw = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR)
    am = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 23 * t + 3 * lp(rng.standard_normal(len(t)), 15)))
    y = bp(saw * am, 120, 1400) + 0.3 * bp(rng.standard_normal(len(t)), 300, 2500) * am
    return y * env(len(t), 0.04, d * 0.8, curve=2)


def ice_crack(d=0.35):
    t = t_(d)
    y = np.zeros_like(t)
    for _ in range(9):
        at = rng.uniform(0, d * 0.5)
        place(y, hp(rng.standard_normal(int(0.006 * SR)), 5000) * env(int(0.006 * SR), 0.0005, 0.005, curve=5) * rng.uniform(0.2, 0.6), at)
    y += bells(d, [3520, 4730, 6110, 7400], decay=0.25, amp=0.25)
    return y


def norm(x, peak_db=-1.0):
    x = x - np.mean(x)
    p = np.max(np.abs(x)) + 1e-9
    return x / p * 10 ** (peak_db / 20)


def fade(x, fi=0.003, fo=0.08):
    # recortar silencio final (< -60 dBFS) y luego fundido
    lvl = np.abs(x) > 10 ** (-60 / 20)
    if lvl.any():
        x = x[:np.nonzero(lvl)[0][-1] + int(0.02 * SR)]
    x = np.array(x)
    n = len(x)
    a, b = int(fi * SR), int(fo * SR)
    x[:a] *= np.linspace(0, 1, a)
    x[n - b:] *= np.linspace(1, 0, b)
    return x


# ---------- ATAQUES ----------
IMP = 0.200


def ataque_1():
    d = 0.9
    y = np.zeros(int(d * SR))
    place(y, sweep_noise(0.24, 400, 2600, 0.9) * env(int(0.24 * SR), 0.18, 0.06, curve=6) * 0.5, 0.0)   # salto
    place(y, crunch(0.10) * 1.0, IMP)                       # mordisco
    place(y, thump(0.2, 70) * 0.9, IMP)
    place(y, ice_crack(0.45) * 0.35, IMP + 0.01)            # hielo que cruje
    return fade(norm(reverb(y, 0.6, 0.18)))


def ataque_2():
    d = 1.0
    y = np.zeros(int(d * SR))
    place(y, growl(0.32, 88) * 0.55, 0.0)                    # gruñido previo
    place(y, sweep_noise(0.16, 3800, 700, 1.0) * env(int(0.16 * SR), 0.12, 0.05, curve=5) * 0.6, IMP - 0.12)  # zarpazo
    place(y, crunch(0.08) * 0.9, IMP)
    place(y, thump(0.16, 90) * 0.7, IMP)
    place(y, bells(0.6, [2637, 3951, 5274, 6645], decay=0.35, amp=0.35), IMP + 0.02)   # esquirlas de hielo
    return fade(norm(reverb(y, 0.7, 0.22)))


# ---------- HECHIZOS ----------
REL = 0.233


def hechizo_1():
    d = 1.9
    y = np.zeros(int(d * SR))
    n = int(REL * SR)
    swell = sweep_noise(REL, 300, 4500, 1.2) * np.linspace(0, 1, n) ** 2
    place(y, swell * 0.5, 0)                                                  # carga de viento helado
    place(y, bells(1.6, [1318.5, 1975.5, 2637, 3322.4, 4186], decay=1.6, amp=0.7), REL)   # cristal (escala Mi)
    place(y, crunch(0.12) * 0.6, REL)                                         # estallido
    tail = bp(rng.standard_normal(int(1.4 * SR)), 2500, 9000) * env(int(1.4 * SR), 0.05, 1.2, curve=3) * 0.18
    place(y, tail, REL)                                                       # brillo de escarcha
    t = t_(1.2)
    place(y, np.sin(2 * np.pi * 55 * t) * np.exp(-t * 4) * 0.5, REL)          # golpe grave
    return fade(norm(reverb(y, 1.6, 0.35, 6000)), fo=0.3)


def hechizo_2():
    d = 2.1
    y = np.zeros(int(d * SR))
    n = int(REL * SR)
    t = t_(REL)
    rumble = lp(rng.standard_normal(n), 180) * np.linspace(0.2, 1, n) * 1.6
    place(y, rumble + sweep_noise(REL, 6000, 900, 1.0) * np.linspace(0, 1, n) ** 3 * 0.5, 0)  # retumbe + aire invertido
    place(y, bells(1.8, [880, 1046.5, 1568, 2093, 2793.8], decay=1.9, amp=0.65), REL)        # campanas graves
    place(y, ice_crack(0.6) * 0.7, REL)
    t2 = t_(1.6)
    wind = sweep_noise(1.6, 900, 3000, 0.6) * env(len(t2), 0.2, 1.3, curve=2.5) * 0.35
    place(y, wind, REL + 0.05)
    return fade(norm(reverb(y, 1.8, 0.38, 5000)), fo=0.35)


# ---------- CRÍTICO: aullido ----------
def aullido():
    d = 2.6
    t = t_(d)
    # contorno de f0: sube, sostiene con vibrato, cae
    k = np.array([0.0, 0.35, 0.7, 1.6, 2.1, 2.6])
    v = np.array([300, 520, 560, 545, 470, 360])
    f0 = np.interp(t, k, v)
    vib = 1 + 0.018 * np.sin(2 * np.pi * 5.2 * t) * np.clip((t - 0.5) / 0.4, 0, 1)
    f0 = f0 * vib * (1 + 0.004 * lp(rng.standard_normal(len(t)), 8) * 30)
    # formantes: "u" -> "a" -> "u"
    F1 = np.interp(t, [0, 0.5, 1.6, 2.6], [320, 650, 620, 330])
    F2 = np.interp(t, [0, 0.5, 1.6, 2.6], [800, 1150, 1100, 780])
    F3 = np.interp(t, [0, 0.5, 2.6], [2300, 2500, 2300])
    y = np.zeros_like(t)
    phase = 2 * np.pi * np.cumsum(f0) / SR
    for h in range(1, 13):
        fh = h * f0
        a = (np.exp(-((fh - F1) / 170) ** 2) * 1.0 + np.exp(-((fh - F2) / 230) ** 2) * 0.35
             + np.exp(-((fh - F3) / 350) ** 2) * 0.06 + 0.01) / h ** 1.25
        if h == 1:
            a = a + 0.9      # aullido: fundamental dominante, casi puro
        y += a * np.sin(h * phase)
    y2 = np.zeros_like(t)
    ph2 = 2 * np.pi * np.cumsum(f0 * 1.007) / SR
    for h in range(1, 5):
        y2 += (0.8 if h == 1 else 0.25 / h) * np.sin(h * ph2 + 1.3)
    y = lp(y, 3500)
    breath = bp(rng.standard_normal(len(t)), 600, 3000) * 0.05
    amp = np.interp(t, [0, 0.18, 0.5, 1.9, 2.4, 2.6], [0, 0.7, 1.0, 0.9, 0.25, 0])
    y = (y + 0.35 * y2 + breath) * amp
    return fade(norm(reverb(y, 2.4, 0.42, 4500)), fo=0.6)


SONIDOS = {
    "moko_ataque_mordisco_1": (ataque_1, "Ataque: salto + mordisco + crujido de hielo. Disparar en el fotograma 7; impacto a +0,200 s."),
    "moko_ataque_mordisco_2": (ataque_2, "Ataque: gruñido + zarpazo + esquirlas de hielo. Disparar en el fotograma 7; impacto a +0,200 s."),
    "moko_hechizo_escarcha_1": (hechizo_1, "Hechizo: carga de viento helado + cristales (Mi) + estallido. Disparar en el fotograma 9; liberación a +0,233 s."),
    "moko_hechizo_escarcha_2": (hechizo_2, "Hechizo: retumbe + aire invertido + campanas graves + viento. Disparar en el fotograma 9; liberación a +0,233 s."),
    "moko_critico_aullido": (aullido, "Golpe crítico: aullido de lobo (síntesis vocal, 2,6 s)."),
}
info = {}
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, axes = plt.subplots(len(SONIDOS), 1, figsize=(10, 2.2 * len(SONIDOS)))
for ax, (name, (fn, desc)) in zip(axes, SONIDOS.items()):
    x = fn()
    pcm = np.int16(np.clip(x, -1, 1) * 32767)
    wav = os.path.join(out, name + '.wav')
    wavfile.write(wav, SR, np.column_stack([pcm, pcm]))
    os.system('ffmpeg -v error -y -i "%s" -c:a libvorbis -q:a 6 "%s"' % (wav, wav[:-4] + '.ogg'))
    f, tt, S = signal.spectrogram(x, SR, nperseg=1024, noverlap=768)
    ax.pcolormesh(tt, f / 1000, 10 * np.log10(S + 1e-12), shading='auto', cmap='magma', vmin=-110, vmax=-30)
    ax.set_ylim(0, 12); ax.set_ylabel('kHz'); ax.set_title(name, fontsize=9)
    info[name] = {"descripcion": desc, "duracion_s": round(len(x) / SR, 3), "pico_dBFS": round(20 * np.log10(np.max(np.abs(x))), 2),
                  "rms_dBFS": round(20 * np.log10(np.sqrt(np.mean(x ** 2))), 2), "archivos": [name + '.wav', name + '.ogg']}
axes[-1].set_xlabel('s')
plt.tight_layout(); plt.savefig(os.path.join(out, 'espectrogramas.png'), dpi=90)
json.dump(info, open(os.path.join(out, 'sonidos.json'), 'w'), ensure_ascii=False, indent=1)
for k, v in info.items():
    print(k, v['duracion_s'], 's', 'pico', v['pico_dBFS'], 'rms', v['rms_dBFS'])
