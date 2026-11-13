# Grand Kia: full canon (with walls) for rev3a and rev3b

These are the snapshots the independent U-181 auditor verified. They are the same files the Excel / PDF of each delivery came from.

| File | Rev | sha256 | Audit |
|---|---|---|---|
| takeoff_canon_rev3a.json | rev3a (delivered 12-nov, VERDE v81cf118) | a5eb2235c2a00022d6a7a8a99c72b537b7a15a452beee7e8ada0e9df6c59b2ba | REVERIF16, open 0 |
| takeoff_canon_rev3b.json | rev3b (delivered 13-nov, VERDE v81cf129) | 1ab5af2c48061c89920ddd8da951399fb4e070ee793d432151ab96eab7801ff4 | REVERIF20, open 0 |

Contents: walls 144 → 148, misc_items 436 → 439, excluded_walls 17 → 16.

The changes from rev3a to rev3b are in ../CAMBIOS_rev3b.txt and ../DELTA_rev3a_rev3b.md:
- A-Z1-20, F1-Z1-06, F-Z1-21/22, WR-05 + TRIM-057, RI-18C;
- corners R70.2;
- excluded_walls with the measured gap_proofs.

Bands use unrotated page points. Sheets A111 / A112 / A113 / A108 / A109 have rotation 270.
For the coverage map: canon point = rendered_point * page.rotation_matrix.
