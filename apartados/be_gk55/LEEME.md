# BE-GK55: check + test (to merge into the next skill version, tools/)

Error (Grand Kia rev3b, REVERIF17 R17-F1, 12-nov):
- Adding the kn 52 patch F-Z1-21 created a false node with A-Z1-13, a wall that did NOT change.
- The two walls are on opposite sides of the kn 51 CMU infill and never meet.
- The false node added 1 stud = +8.21 LF of 362S162-19 that no listed change explained.

Rule:
- Between two revisions, every NEW node (L / T / split) that touches a wall whose band did not change goes in CAMBIOS_<rev>.txt, naming both ids,
  or the pair is declared non-meeting (`corner_skip` with N/SHEET). Without either: FAIL.
- `build_canon.nodos` and `fix_corners` respect `corner_skip`.

Files:
- `be_gk55.py::fallas(canon_prev, canon_new, cambios_txt)`
  CLI: `python3 be_gk55.py <canon_prev> <canon_new> <CAMBIOS.txt>`.
- `test_be_gk55.py`: real case (false T = FAIL; corner_skip = PASS; explained in CAMBIOS = PASS; node between two new walls is not checked).

Real check on GK: rev3a vs the canon REVERIF17 audited = FAIL (L A-Z1-13 / F-Z1-21); rev3a vs the corrected canon = PASS.
