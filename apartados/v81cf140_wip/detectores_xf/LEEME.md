# v140 — blind detectors found in Xfinity (audit 13-nov I-1 / I-4), logged by order of COORDINACIÓN 16:26

1. CB_RCP_TAGS (BE-CR30 / U-189): `tags_cielo` only counts coded tags (GYP-1, ACT-2...). A3.0 prints DESCRIPTIVE tags
   ("2x4 ACT 12'-0\" AFF", "GYP. BD. 8'-6\" AFF", "EXISTING GYP. BD. 9'-0\" AFF") -> {} -> N/A = PASS in vacuum (U-137).
   Second cause: RX_HOJA_RCP = "REFLECTED CEILING" with a literal space; a title split by a newline is not an RCP. Side note: A0.3
   ("REFER TO REFLECTED CEILING PLAN") is classified as an RCP sheet. Fix direction in INFORME_R_A3_xfinity.md.
2. CB_BE_CF10: "specs exist" only with a Project Manual or CSI numbers; A0.3 is an outline SPECIFICATIONS sheet without
   CSI numbers -> N/A. Fix: a sheet titled SPECIFICATIONS with >= 2 trade terms = specs present; accept "A0.3 <HEADING>" as the reference.
3. Gate false positive (CE_DOBLE_CIELO cuartos_rcp): "162" / "600" (stud designations on A3.0) and "200D" (A2.0 hardware) read as
   rooms; Xfinity rev1d carries 3 "not a room" rows in DOBLE_CIELO.csv.
Test: test_v140_detectores_xf.py (FAILS with v81cf138 = reproduces; must PASS in v140). In rev1d the tags are loaded in
canon.rcp_tags (6, 1 CARGADO SOF-01 + 5 with a reason N/HOJA) and DOBLE_CIELO.csv comes from the independent review R_A3.
