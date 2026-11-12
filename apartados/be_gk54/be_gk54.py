"""BE-GK54 (Grand Kia rev3a, U-193 red M-A111-29, 12-nov): two parallel bands with a gap (or two type tags) are TWO walls. A wall in
excluded_walls whose reason says it is the 'same (single) wall as <X>' FAILS when the coverage map (Auditoria/COBERTURA.csv) shows a
detected wall band parallel to <X>, on the same sheet, within 14 in. of X's band (gap between the two faces) and overlapping it, that is
RED or carried by nobody - unless the exclusion carries 'gap_proof' (printed evidence that the gap does not exist).
Usage: python3 be_gk54.py <canon.json> <COBERTURA.csv>   -> exit 1 on FAIL."""
import csv, json, re, sys

RX_SAME = re.compile(r"(?i)\bsame\s+(?:single\s+)?wall\s+as\s+([A-Z][A-Z0-9]*-Z\d-\d{2})")


def fallas(canon, cob_rows, esc=9.0, gap_in=14.0, to_canon=None):
    """to_canon(sheet, x, y) -> (x, y): COBERTURA.csv is in rendered (rotated) page points; canon bands are unrotated page points."""
    to_canon = to_canon or (lambda h, x, y: (x, y))
    walls = {w['id']: w for w in canon.get('walls') or []}
    ev = []
    for e in canon.get('excluded_walls') or []:
        m = RX_SAME.search(str(e.get('reason') or ''))
        if not m or str(e.get('gap_proof') or '').strip():
            continue
        x = walls.get(m.group(1))
        b = (x or {}).get('band') or {}
        if b.get('ori') not in ('H', 'V'):
            continue
        c_mid = (float(b['c0']) + float(b['c1'])) / 2
        lo, hi = sorted((float(b['lo']), float(b['hi'])))
        tol = (gap_in / 12.0) * esc + abs(float(b['c1']) - float(b['c0']))
        for r in cob_rows:
            if r.get('hoja') != b.get('sheet') or r.get('tipo') != 'muro' or r.get('estado') != 'ROJO':
                continue
            rx, ry = to_canon(r['hoja'], float(r['x']), float(r['y']))
            L = float(r.get('largo_ft') or 0) * esc
            along, cross = (rx, ry) if b['ori'] == 'H' else (ry, rx)
            if abs(cross - c_mid) <= tol and along + L / 2 >= lo - esc and along - L / 2 <= hi + esc and abs(cross - c_mid) > 0.5:
                ev.append(f"{e['id']}: excluded as 'same wall as {m.group(1)}' but the coverage map has a separate parallel band "
                          f"{r['id']} ({rx}, {ry}) {r.get('largo_ft')} ft at {abs(cross - c_mid) / esc * 12:.1f} in. from it, RED: two leaves with a gap "
                          f"are two walls (BE-GK54); prove the gap does not exist ('gap_proof') or carry it")
    return ev


if __name__ == '__main__':
    c = json.load(open(sys.argv[1]))
    rows = list(csv.DictReader(open(sys.argv[2], encoding='utf-8-sig')))
    tc = None
    if len(sys.argv) > 3:                          # markups PDF: rendered -> unrotated points with each sheet's derotation
        import pymupdf
        d = pymupdf.open(sys.argv[3])
        pg = {(d[i].get_label() or str(i + 1)): d[i] for i in range(len(d))}
        def tc(h, x, y):
            p = pg.get(h)
            if p is None:
                return x, y
            q = pymupdf.Point(x, y) * p.rotation_matrix          # rendered -> unrotated (inverse of derotation_matrix)
            return q.x, q.y
    ev = fallas(c, rows, to_canon=tc)
    print('\n'.join(ev) if ev else 'BE-GK54 PASS: no "same wall" exclusion hides a separate parallel band')
    sys.exit(1 if ev else 0)
