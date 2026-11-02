# TOOL_ISSUES — reader A, CFA #2284 River Point

1. **No ceiling system for 6" LGS ceiling joists.** S-241 (C3 dropped ceiling plan + A2 LGS ceiling joist schedule)
   frames the new gyp ceilings at Entry A, Entry B, Men's and Women's with 600S162-33 @ 16" (span < 15 ft) and a
   rim joist. `canon.py` `ceilings[].system` only accepts furring / stud_joist / canopy_joist / framed_soffit /
   usg_grid, and every joist system is counted as **3-5/8"** (F_36). Loading these ceilings in `ceilings[]` would
   turn 6" joists into 3-5/8" studs (false fact). Workaround (data not bent): joists, rim track and 5/8" board
   loaded as `misc_items` (`CLG-*-J` family `6" stud`, `CLG-*-R` family `ceiling / soffit track 6"`, `CLG-*-B`
   family `5/8" gyp board regular`), with a trace list `ceilings_info`. Proposed fix: a `joist_size` field on
   `framed_soffit` / `stud_joist` mapped through STUD_FAM.
2. **Z-furring family name hard-codes 1-1/2".** M2.1 is a **2"** metal Z channel @ 24" (A-202 schedule, A1/A-605).
   `stud_size` "2\" Z-furring channel" is routed by STUD_FAM to the family `1-1/2" Z-furring` (F_ZF). The LF
   (96.0) is right; the family label is wrong for this project. Proposed fix: Z-furring family by size.
3. **`top_track_kind` warned as out-of-schema** ("clave fuera del esquema, canon.py no la lee") although
   `canon.py` reads it in R80w.31 (`top_track_tramos`). It is missing from WALL_KEYS. Harmless warning.
4. `demo_geom` is a top-level list not checked by `canon.py` / `validar_canon.py` (only `markups_demo.py` reads
   it); its lf / sf were written consistent with the `DEMO-*` misc_items.
