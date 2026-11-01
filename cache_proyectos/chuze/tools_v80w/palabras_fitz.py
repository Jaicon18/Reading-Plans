# -*- coding: utf-8 -*-
"""palabras_fitz.py — words de una página con PyMuPDF, en el mismo formato que pdfplumber.extract_words(extra_attrs=['size']).

Origen (Chuze, 2026-11-01): arranque.py con pdfplumber tardaba > 2 min por hoja y llegaba a 10 GB de RAM en sets
vectoriales grandes (106 hojas de 3024x2160 pt). PyMuPDF da los mismos words en segundos.
Coordenadas: x0, x1, top, bottom en pt desde arriba-izquierda (igual que pdfplumber) — válido con rotation 0 y
cropbox == mediabox; si no, se usa pdfplumber (el llamador decide con `compatible`).
size = tamaño de fuente del span que contiene el centro del word.
"""
import fitz


def compatible(page):
    # coords de fitz = relativas a la esquina sup-izq de la página visible (0..w, 0..h), como pdfplumber.
    # Vale con rotation 0 y cropbox del mismo tamaño que el mediabox (un mediabox desplazado no cambia nada).
    cb, mb = page.cropbox, page.mediabox
    return page.rotation == 0 and abs(cb.width - mb.width) < 0.5 and abs(cb.height - mb.height) < 0.5


def words(page):
    spans = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                spans.append((fitz.Rect(s['bbox']), s['size']))
    out = []
    for x0, y0, x1, y1, t, *_ in page.get_text('words'):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        size = next((sz for r, sz in spans if r.x0 - 0.5 <= cx <= r.x1 + 0.5 and r.y0 - 0.5 <= cy <= r.y1 + 0.5), 0.0)
        out.append(dict(text=t, x0=x0, x1=x1, top=y0, bottom=y1, size=round(size, 2)))
    return out
