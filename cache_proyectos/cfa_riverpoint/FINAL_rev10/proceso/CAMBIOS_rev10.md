# CAMBIOS rev10 - CFA #2284 River Point (estimator answers 5-nov + full RFI hunt over both GC sets)

Excel produced by plantilla_excel.py armar (skill v81cf42 = v81cf41 + BE-CF25) with the reglas.py gate passing; every quantity computed by canon.py / accesorios.py from the corrected canon (scripts/correcciones_rev10.py). rev1-rev9 files untouched.

| # | Item | rev9 | rev10 | Delta | N/SHEET | Rule / decision |
|---|---|---|---|---|---|---|
| 1 | RFI-07 play-bay ceiling framing | open | closed - user answer 5-nov 'A Planos: joist nuevo' (option A, already loaded) | 0 | A2/S-241 | user decision |
| 2 | RFI-26 serving ceiling 10'-2" vs 10'-0" | open | closed - estimator decision R-ALC-10 option A (10'-2" loaded, note on A-221 10'-0") | 0 | D2 / D3/A-622 vs A-221 | R-ALC-10 |
| 3 | RFI-11 dining half wall height | 8-term grep | full hunt (both GC sets, all disciplines, vectors at printed scale): height printed nowhere; length 22.00 LF confirmed [DERIVED] | 0 | A-050 KN8, E-200 | BE-CF25 (RFI stays open, 3'-6" conservative loaded) |
| 4 | DEMO-12 existing menuboard furr down | 55.559 SF (18.872 LF x (0.944 + 2.0)) | 60.42 SF (18.69 LF x (1.233 + 2.0)) | +4.86 SF demolition | A-052 outline at 18 pt/ft | #0 DERIVED (vector at printed scale) |
| 5 | RFI-20 draftstop patch | 9-term grep | full hunt: patch size printed nowhere; 4 x 6" PVC conduits (P-211), Type VB not rated (G-003) | 0 | A-052 n.9, P-211, G-003 | BE-CF25 (open, 32 SF loaded) |
| 6 | RFI-27 drive-thru furr down | open (no furr down loaded, framed alternative) | resolved: 2x wood furr-out (A-501 C2, A-402 A3), Div. 06 | 0 | A-501 C2, A-402 A3 | found in the drawings |
| 7 | DEMO-C6 east-room gyp ceiling demo | 38.35 SF | 34.57 SF [DERIVED A-052 at 18 pt/ft; A-050 34.59] | -3.78 SF demolition | A-052 KN10 + A-050 | RFI-28 resolved |

## Material Summary NET rev9 -> rev10

| Row | Unit | rev9 | rev10 | Delta |
|---|---|---|---|---|
| Demolition - gypsum board and metal stud framing (SF = length x height x layers) | SF | 3306.68 | 3307.76 | +1.08 |
