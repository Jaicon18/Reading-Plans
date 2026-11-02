# TOOL_ISSUES — reader B (CFA #2284 River Point)

1. **ceilings[] has no system for a 6" LGS-joist dropped ceiling, and no board-only system.**
   S-241 C3 + A2/S-241 print the dropped gyp ceilings (Entry A, Entry B, Men's, Women's) on ceiling joists. The LGS
   alternative is 600S162-33 @ 16" o.c. The only joist systems in `canon._ceilings` are `framed_soffit` and
   `canopy_joist`. Both count **3-5/8"** joists (F_36), so the 6" member would come out under the wrong size family.
   `furring` / `stud_joist` add carrying channel and hangers that are not printed.
   - I did not bend the data. Those 4 ceilings went into `misc_items`: the joists as "6\" stud (todos los gauges)"
     (LF + pcs, op written) and the board as "5/8\" gyp board regular" (SF).
   - As a result they do not appear in `ceilings[]`, and no ceiling perimeter track is generated for them. The LGS rim
     track is not printed either (RFI-08).
   - Proposed fix: a `joist_size` field for `framed_soffit` (or a `board_only` / `joist_6` system).
2. **framed_soffit spacing comes from the global `constants.furring_oc_in`.** C3/S-801 prints the menu furr-down at
   362S162-33 @ **32"** o.c., while C4/A-624 prints the island soffit @ 16". Only one value is possible, so 16" is used
   for both, which is conservative on the menu furr-down. Proposed fix: a per-ceiling `oc_in`.
3. **demo_geom is not read or validated by canon.py.** Only the `misc_items` DEMO-nn reach the familia.
   `demo_geom` stays a sidecar list for markups_demo.py. Ceiling demolitions were given a closed perimeter polyline,
   with `lf` = perimeter, `h_ft` = 0 and `sf` = area. markups_demo then computes Length x Depth = 0, so the SF only
   appears in its contents text.
