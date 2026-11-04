import sys, pymupdf, numpy as np
A = pymupdf.open(sys.argv[1]); B = pymupdf.open(sys.argv[2])
print("pages", A.page_count, B.page_count)
tot_x, bad = 0, []
for i in range(min(A.page_count, B.page_count)):
    pa, pb = A[i], B[i]
    xa = {x[1] for x in pa.get_xobjects()}; xb = {x[1] for x in pb.get_xobjects()}
    miss = sorted(xa - xb)
    ta, tb = pa.get_text(), pb.get_text()
    d = None
    if miss or ta != tb:
        ia = pa.get_pixmap(dpi=30, annots=False); ib = pb.get_pixmap(dpi=30, annots=False)
        a = np.frombuffer(ia.samples, np.uint8); b = np.frombuffer(ib.samples, np.uint8)
        d = float((np.abs(a.astype(int) - b.astype(int)) > 40).mean()) if a.size == b.size else -1
    if miss or ta != tb:
        tot_x += len(miss)
        bad.append((i + 1, miss[:6], len(miss), ta == tb, d))
for b in bad:
    print(b)
print("missing xobjects total", tot_x, "pages", len(bad))
