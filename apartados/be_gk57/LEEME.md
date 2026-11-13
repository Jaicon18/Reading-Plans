# BE-GK57: check and test (to merge into tools/ in the next skill version)

Grand Kia rev3b, 12-nov. The same error happened three times in one rev: a copy or backup of a chain input was left INSIDE the work tree, and the chain read it through a glob or as "most recent":
1. `etapas/4_canon/resuelto_Z1.rev3a.bak.json` matched build_canon's `resuelto_Z*.json` glob, so the OLD A-Z1-20 was loaded.
2. `burbujas/G2/CADENA.md` and `CADENA.prev.md` were edited after the main CADENA.md, so the gate took one of them as the most recent CADENA.md and reported a false "A501 without circle".
3. The previous deliveries `entrega_rev*/` sat inside the work dir, and the gate scanned them through the `takeoff_work` link.

Rule: backups, previous copies and previous deliveries go OUTSIDE the work tree (`bak_<rev>/`, `entregas_previas/`).

- `be_gk57.py::fallas(workdir, rev)`. CLI: `python3 be_gk57.py <workdir> <rev>`.
- `test_be_gk57.py`: the three real cases each FAIL; the same files under `bak_<rev>/` PASS.
