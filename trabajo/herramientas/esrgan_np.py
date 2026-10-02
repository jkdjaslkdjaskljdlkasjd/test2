# Real-ESRGAN realesr-animevideov3 (SRVGGNetCompact, x4) en numpy, sin torch.
# Pesos oficiales: github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth
# Arquitectura (basicsr SRVGGNetCompact): conv3x3(3->64)+PReLU, 16 x [conv3x3(64->64)+PReLU], conv3x3(64->48),
# pixel_shuffle(4) y se suma la entrada ampliada por vecino mas cercano. Precision completa (float32), por bloques.
import zipfile, pickle, numpy as np, sys, time

def cargar(pth):
    z = zipfile.ZipFile(pth)
    pref = z.namelist()[0].split('/')[0]
    class Storage:
        def __init__(self, key, dtype): self.key, self.dtype = key, dtype
    def rebuild(storage, offset, size, stride, *a):
        raw = np.frombuffer(z.read('%s/data/%s' % (pref, storage.key)), storage.dtype)
        return np.lib.stride_tricks.as_strided(raw[offset:], size, [s * raw.itemsize for s in stride]).copy() if size else raw[offset:offset+1].copy()
    class U(pickle.Unpickler):
        def find_class(self, mod, name):
            if name == '_rebuild_tensor_v2': return rebuild
            if name == 'FloatStorage': return np.float32
            if mod == 'collections' and name == 'OrderedDict':
                import collections; return collections.OrderedDict
            return super().find_class(mod, name)
        def persistent_load(self, pid):
            return Storage(pid[2], np.float32)
    d = U(z.open('%s/data.pkl' % pref)).load()
    return d.get('params', d)

def conv(x, w, b):
    # x: (H, W, Cin) ; w: (Cout, Cin, 3, 3)
    H, W, C = x.shape
    p = np.pad(x, ((1, 1), (1, 1), (0, 0)))
    out = np.empty((H, W, w.shape[0]), np.float32)
    out[:] = b
    for dy in range(3):
        for dx in range(3):
            out += p[dy:dy + H, dx:dx + W].reshape(-1, C).dot(w[:, :, dy, dx].T).reshape(H, W, -1)
    return out

def red(x, P):
    n = 0
    while 'body.%d.weight' % n in P:
        w = P['body.%d.weight' % n]
        if w.ndim == 4:
            x = conv(x, w, P['body.%d.bias' % n])
        else:  # PReLU
            x = np.where(x >= 0, x, x * w)
        n += 1
    return x

def ampliar(img, P, bloque=128, borde=24):
    """img: (H, W, 3) float32 0..1 -> (4H, 4W, 3). Bloques con solapamiento para no dejar uniones."""
    H, W, _ = img.shape
    out = np.zeros((H * 4, W * 4, 3), np.float32)
    for y0 in range(0, H, bloque):
        for x0 in range(0, W, bloque):
            y1, x1 = min(y0 + bloque, H), min(x0 + bloque, W)
            ya, xa = max(y0 - borde, 0), max(x0 - borde, 0)
            yb, xb = min(y1 + borde, H), min(x1 + borde, W)
            t = img[ya:yb, xa:xb]
            f = red(t, P)                                  # (h, w, 48)
            h, w = t.shape[:2]
            f = f.reshape(h, w, 3, 4, 4).transpose(0, 3, 1, 4, 2).reshape(h * 4, w * 4, 3)   # pixel_shuffle
            f += np.repeat(np.repeat(t, 4, 0), 4, 1)
            out[y0 * 4:y1 * 4, x0 * 4:x1 * 4] = f[(y0 - ya) * 4:(y0 - ya + y1 - y0) * 4, (x0 - xa) * 4:(x0 - xa + x1 - x0) * 4]
    return np.clip(out, 0, 1)

if __name__ == '__main__':
    from PIL import Image
    P = cargar(sys.argv[1])
    print({k: v.shape for k, v in list(P.items())[:4]}, len(P))
    im = np.asarray(Image.open(sys.argv[2]).convert('RGB'), np.float32) / 255
    t = time.time(); o = ampliar(im, P); print('listo', round(time.time() - t, 1), 's', o.shape)
    Image.fromarray((o * 255 + 0.5).astype(np.uint8)).save(sys.argv[3])
