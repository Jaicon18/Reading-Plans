import re, sys, os
R = {f"R80e.{a}": f"R80e.{a+6}" for a in range(57, 67)}
B = {f"BE-{a}": f"BE-{a+7}" for a in range(93, 98)}
rx = re.compile(r"R80e\.(5[7-9]|6[0-6])(?!\d)|BE-(9[3-7])(?!\d)")
def f(m):
    return R.get(m.group(0)) or B.get(m.group(0)) or m.group(0)
for root in sys.argv[1:]:
    paths = [root] if os.path.isfile(root) else [os.path.join(d, n) for d, _, fs in os.walk(root) for n in fs]
    for p in paths:
        if not p.endswith((".py", ".md", ".json", ".jsonl")): continue
        s = open(p, encoding="utf-8", errors="ignore").read()
        t = rx.sub(f, s)
        if t != s: open(p, "w", encoding="utf-8").write(t); print("renum", p)
