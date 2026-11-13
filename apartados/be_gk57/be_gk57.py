"""BE-GK57 (Grand Kia rev3b, 12-nov, three times in one rev): a copy / backup of a chain input left INSIDE the work tree is read by a
glob or by 'most recent': (1) resuelto_Z1.rev3a.bak.json in etapas/4_canon/ was read by build_canon (glob resuelto_Z*.json) and loaded
the OLD A-Z1-20; (2) burbujas/G2/CADENA.md and CADENA.prev.md, edited later, became the 'most recent' CADENA.md and the gate counted a
false 'A501 bubble without circle'; (3) old delivery folders entrega_rev*/ under the work dir were scanned through the takeoff_work link.
Rule: backups, previous copies and previous deliveries go OUTSIDE the work tree (e.g. /root/<proj>/bak_<rev>/, entregas_previas/).
Check: no file in the work tree whose name marks a copy (.bak / .prev / .old / copy / _rev<N> of an input name / 'backup') next to the
input it copies, and no second entrega_rev* folder besides the current rev. Usage: python3 be_gk57.py <workdir> <rev>  -> exit 1 on FAIL."""
import os, re, sys

RX_COPIA = re.compile(r"(?i)(?:\.bak|\.prev|\.old|[._ -]copy|backup|\.orig)(?:\.|$)|\.rev\d+[a-z]?\.(?:bak\.)?(?:json|csv|md)$")
SALTA = ("bak_", "entregas_previas", "bitacora_logs", ".git", "__pycache__")


def fallas(w, rev):
    ev = []
    for raiz, ds, fs in os.walk(w, followlinks=False):
        ds[:] = [d for d in ds if not d.startswith(SALTA)]
        rel = os.path.relpath(raiz, w)
        if rel == ".":
            for d in ds:
                if re.match(r"entrega(?:_rev\w+)?$", d) and d != f"entrega_{rev}":
                    ev.append(f"{d}/: previous delivery inside the work tree (scanned by globs / takeoff_work link): move it out (BE-GK57)")
        for f in fs:
            if RX_COPIA.search(f):
                ev.append(f"{os.path.join(rel, f)}: copy / backup inside the work tree (read by a glob or as 'most recent'): move it to bak_<rev>/ (BE-GK57)")
    return ev


if __name__ == "__main__":
    ev = fallas(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
    print("\n".join(ev[:40]) if ev else "BE-GK57 PASS: no copies / backups / previous deliveries inside the work tree")
    sys.exit(1 if ev else 0)
