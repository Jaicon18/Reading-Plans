"""Tabla por type y por material: rev13, rev2 y corridas del runner (#4, #5, #7); variación entre corridas."""
import sys, re, collections, statistics, openpyxl, warnings
warnings.filterwarnings("ignore")
PRIN = [("5/8\" Type X", r'^5/8" gypsum board, Type X$'), ("5/8\" Type X W.R.", r'^5/8" gypsum board, Type X W\.R\.'),
        ("3-5/8\" stud", r'^3-5/8" metal stud \(LF'), ("6\" stud", r'^6" metal stud \(LF'),
        ("Bottom track 3-5/8\"", r'^Bottom track 3-5/8"$'), ("Bottom track 6\"", r'^Bottom track 6"$'),
        ("1/2\" cement board", r'^1/2" cement board'), ("5/8\" cement board", r'^5/8" cement board'),
        ("FRT plywood 5/8\"", r'^FRT plywood substrate \(5/8'), ("FRT plywood 3/4\"", r'^FRT plywood substrate \(3/4'),
        ("FRP panels", r'^FRP panels'), ("METAL trim", r'^METAL trim'), ("Blocking FRT", r'^Blocking FRT')]
def tipos(f):
    ws = openpyxl.load_workbook(f, data_only=True)["Partition Takeoff"]; t = None; d = collections.defaultdict(lambda: [0.0, 0.0])
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] and isinstance(r[0], str) and r[0].startswith("TYPE ") and r[1] is None:
            t = r[0][5:].strip(); t = "OTHER FRAMING (incl. column wraps)" if t in ("C25", "OTHER FRAMING (NOT A PARTITION)") else t; continue
        if r[0] and isinstance(r[0], str) and not r[1] and r[2] is None and not r[0].startswith("TYPE "): t = r[0].strip()[:30]; continue
        if t and isinstance(r[2], (int, float)) and r[1] and "TOTAL" not in str(r[1]).upper():
            d[t][0] += r[2]; d[t][1] += r[7] if isinstance(r[7], (int, float)) else 0
    return d
def mats(f):
    ws = openpyxl.load_workbook(f, data_only=True)["Material Summary"]; out = {}
    for r in ws.iter_rows(values_only=True):
        if r and isinstance(r[0], str) and isinstance(r[2], (int, float)):
            for n, p in PRIN:
                if re.search(p, r[0].strip()) and n not in out: out[n] = r[2]
    return out
def main():
    F = dict(a.split("=", 1) for a in sys.argv[1:])
    cols = list(F)
    T = {k: tipos(v) for k, v in F.items()}; M = {k: mats(v) for k, v in F.items()}
    runs = [c for c in cols if c.startswith("#")]
    def clase(err, cv):
        """sistemático = el error medio pasa 5 % y supera 2x la dispersión entre corridas; variación = dispersión > 5 %."""
        if err is None: return "—"
        e = abs(err); c = cv or 0
        if e > 5 and e > 2 * c: return "SYSTEMATIC"
        if c > 5 and e > 5: return "MIXED"
        if c > 5: return "READING VARIATION"
        return "OK"
    def pct(x, y): return "—" if not y or x is None else f"{(x - y) / y * 100:+.1f} %"
    print("## By type (Length LF / Board SF)\n")
    print("| Type | " + " | ".join(cols) + " | runs CV (LF) | runs mean vs rev13 | class |"); print("|---" * (len(cols) + 4) + "|")
    for t in sorted(set().union(*[set(T[c]) for c in cols]), key=str):
        v = [T[c].get(t) for c in cols]; lf = [T[c].get(t, [0, 0])[0] for c in runs]
        m = statistics.mean(lf); cvn = statistics.pstdev(lf) / m * 100 if m else None; ref = T['rev13'].get(t, [0])[0]
        err = (m - ref) / ref * 100 if ref else None
        print(f"| {t} | " + " | ".join(f"{x[0]:.1f} / {x[1]:.0f}" if x else "—" for x in v) + f" | {'—' if cvn is None else f'{cvn:.1f} %'} | {pct(m, ref)} | {clase(err, cvn)} |")
    print("\n## Principal materials\n")
    print("| Material | " + " | ".join(cols) + " | " + " | ".join(f"{c} vs rev13" for c in runs) + " | runs CV | runs mean vs rev13 | class |"); print("|---" * (len(cols) + len(runs) + 4) + "|")
    for n, _ in PRIN:
        v = [M[c].get(n) for c in cols]; rv = [M[c].get(n) or 0 for c in runs]; m = statistics.mean(rv)
        cvn = statistics.pstdev(rv) / m * 100 if m else None; ref = M['rev13'].get(n); err = (m - ref) / ref * 100 if ref else None
        print(f"| {n} | " + " | ".join("—" if x is None else f"{x:,.0f}" for x in v) + " | " + " | ".join(pct(M[c].get(n), M['rev13'].get(n)) for c in runs) + f" | {'—' if cvn is None else f'{cvn:.1f} %'} | {pct(m, ref)} | {clase(err, cvn)} |")


if __name__ == "__main__":
    main()
