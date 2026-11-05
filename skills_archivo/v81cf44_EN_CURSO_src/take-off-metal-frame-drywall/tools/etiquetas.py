"""etiquetas.py — v80f (R80e.21): colocación de etiquetas sin solapes para las imágenes de evidencia (planmark,
partitions by type).

Problema que corrige: cada etiqueta se dibujaba en un desplazamiento fijo junto a su wall; en zonas densas (centro de
A-101, restrooms) las etiquetas quedaban encimadas entre sí y sobre otras líneas, ilegibles.

colocar(dr, etiquetas, font, size, obstaculos=(), ...):
  etiquetas: [{'text', 'anchor': (x, y), 'color': (r, g, b), 'own': [segmentos del propio wall]}] en píxeles.
  obstaculos: segmentos [((x0, y0), (x1, y1)), ...] que una etiqueta no debe tapar (los walls marcados).
  Para cada etiqueta (de la más apretada a la más libre) prueba posiciones en anillos crecientes alrededor del
  anchor (16 direcciones); toma la primera que queda dentro de la imagen, no toca otra etiqueta ya puesta y no tapa
  ningún obstáculo. Si ninguna cumple, toma la de menor solape. Dibuja: leader line del anchor al borde de la caja,
  caja blanca con borde del color del type y el texto. Devuelve la lista de cajas (para tests).
"""
import math

DIRS = [(math.cos(a), math.sin(a)) for a in [k * math.pi / 8 for k in range(16)]]


def _choca(a, b, pad=0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def _tapa(box, seg, pad=2, n=24):
    (x0, y0), (x1, y1) = seg
    for k in range(n + 1):
        t = k / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        if box[0] - pad <= x <= box[2] + pad and box[1] - pad <= y <= box[3] + pad:
            return True
    return False


def _caja(ax, ay, dx, dy, w, h, d):
    """Caja de w x h cuyo punto más cercano al anchor queda a distancia d en la dirección (dx, dy)."""
    cx, cy = ax + dx * d, ay + dy * d
    x0 = cx if dx > 0.3 else (cx - w if dx < -0.3 else cx - w / 2)
    y0 = cy if dy > 0.3 else (cy - h if dy < -0.3 else cy - h / 2)
    return (x0, y0, x0 + w, y0 + h)


def _punto_borde(box, ax, ay):
    return (min(max(ax, box[0]), box[2]), min(max(ay, box[1]), box[3]))


def colocar(dr, etiquetas, font, size, obstaculos=(), pad=4, anillos=14, paso=None, ancho_linea=2):
    W, H = size
    medidas = []
    for e in etiquetas:
        b = dr.textbbox((0, 0), e['text'], font=font)
        medidas.append((b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad, b))
    paso = paso or max(m[1] for m in medidas) * 0.9 if medidas else 10
    # orden: primero las etiquetas con más vecinos cerca (zonas densas), así toman los huecos buenos
    def densidad(i):
        ax, ay = etiquetas[i]['anchor']
        return -sum(1 for e in etiquetas if math.dist(e['anchor'], (ax, ay)) < 6 * paso)
    orden = sorted(range(len(etiquetas)), key=densidad)
    puestas, cajas = [], [None] * len(etiquetas)
    for i in orden:
        e = etiquetas[i]
        w, h, tb = medidas[i]
        ax, ay = e['anchor']
        own = e.get('own') or []
        mejor, mejor_c = None, None
        # direcciones ordenadas: primero hacia afuera de la zona (lejos de los anchors vecinos y del centro local)
        vx = vy = 0.0
        for e2 in etiquetas:
            bx, by = e2['anchor']
            dd = math.dist((ax, ay), (bx, by))
            if 0 < dd < 12 * paso:
                vx += (ax - bx) / dd ** 2; vy += (ay - by) / dd ** 2
        dirs = sorted(DIRS, key=lambda u: -(u[0] * vx + u[1] * vy)) if (vx or vy) else DIRS
        for r in range(1, anillos + 1):
            d = r * paso
            for dx, dy in dirs:
                box = _caja(ax, ay, dx, dy, w, h, d)
                if box[0] < 0 or box[1] < 0 or box[2] > W or box[3] > H:
                    continue
                c = sum(4 for p in puestas if _choca(box, p, pad)) + \
                    sum(1 for s in obstaculos if s not in own and _tapa(box, s))
                if c == 0:
                    mejor, mejor_c = box, 0
                    break
                if mejor_c is None or c < mejor_c:
                    mejor, mejor_c = box, c
            if mejor_c == 0:
                break
        box = mejor or _caja(ax, ay, 1, -1, w, h, paso)
        puestas.append(box)
        cajas[i] = box
        col = e.get('color', (0, 0, 0))
        dr.line([(ax, ay), _punto_borde(box, ax, ay)], fill=col, width=ancho_linea)
        dr.rectangle(box, fill=(255, 255, 255), outline=col, width=2)
        dr.text((box[0] + pad - tb[0], box[1] + pad - tb[1]), e['text'], fill=col, font=font)
    return cajas


def solapes(cajas, pad=0):
    """Pares de cajas que se tocan (para verificar la imagen)."""
    out = []
    for i in range(len(cajas)):
        for j in range(i + 1, len(cajas)):
            if _choca(cajas[i], cajas[j], pad):
                out.append((i, j))
    return out
