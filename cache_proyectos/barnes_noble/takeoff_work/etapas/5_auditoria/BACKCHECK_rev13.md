VERDICT: PASS WITH COMMENTS
LIBRARY: 44 PASS · 0 FAIL · 3 N/A

# Back-check rev13 - Barnes & Noble Colorado Springs (2026-10-28)

File: `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev13.xlsx`, md5 0941eb1ed8f72a8d3b7da523dbbac4bb (re-test of the rebuild; first pass was on 544435fc...). Nets are unchanged: only R37 and R58 differ from rev12. Baseline: rev12 in FINAL_FOR_REVIEW_2026-10-24_rev12, md5 7619b0cc728eb569f8f5fbdda318ffb8. Scope per R80e.30: Material Summary R37 and R58, plus Pending Items RFI-55, checked against `rev12_pvc_trim/RFI_PVC.md` and its crops (01, 02). The full library was run.

## 1. Decisions (RFI_PVC.md, estimator 2026-10-28)

| ID | Decision | Applied? | Evidence |
|---|---|---|---|
| PVC-1 | Trim 565.62 - 60.0 (hourglass caps keep the metal guard) + 19.0 J-mold below the countertop = 524.62 | YES | R58: Work Room 266.44 + Janitor 84.86 + types 3/4 154.32 (214.32 - 60.0) + below counter 19.0 = 524.62; R45 metal guards 72 unchanged |
| PVC-2 | Division bars +363 LF inside R58 | YES | R58 FRP-DIVISION-BARS 180 + 16 + 32 + 135 = 363. Net 530.54 -> 887.62 |
| FRP-3 | Work Room at finished dimensions, -23.0 SF | YES | R37 FRP-1-CAFE-WORKROOM 852.2 (85.22 x 10.0, 1/A-221 28'-5 7/8" x 12'-2" + stub) |
| FRP-4 | FRP-1 below the Cafe countertop, +57 SF | YES | R37 FRP-1-CAFE-BELOW-COUNTER 57 (19.0 x 3.0). Net 1,967.38 -> 2,001.38 |
| RFI-55 | New row, CLOSED | YES | Pending Items row 58 starts "CLOSED - estimator decision 2026-10-28:", has an N/SHEET, and the deltas match R37 / R58 |

Plan / crops: 3/A-225 and 4/A-225 "FRP J-MOLD AT BOTTOM OF FRP PANEL" confirmed (crop 01); 1/A-225 FRP-1 on all four Work Room walls, and "INCLUDING 6" BASE WITH TERMINATION BAR" belongs to the EP-1 floor (crop 02). Formats: R37 waste B6, pieces / B30; R58 waste B6, pieces / B18 (unchanged formulas).

Other nets: all 65 other Material Summary rows match rev12 exactly (row order and formulas unchanged). Inputs, Partition Takeoff, Review Items and Scope Checklist are identical to rev12. Pending Items changes only by the added row 58. Sheets and columns are unchanged.

## 2. Library

| Test | Result | Note |
|---|---|---|
| BE-01..BE-19, BE-52, BE-53, BE-56 | PASS | none of these rows changed except R37 / R58 |
| BE-20..BE-25, BE-29 | PASS | unchanged since rev12 |
| BE-26, BE-27, BE-28 | N/A | no ballistic / ATM recess / canopy |
| BE-40 | PASS | R37 breakdown = 2,001.38; R58 subtotals 266.44 + 84.86 + 154.32 + 19.0 + 363 = 887.62 |
| BE-41, BE-48, BE-55 | PASS | scan clean (only the inherited snake_case kinds, see comments) |
| BE-42..BE-45, BE-49..BE-51, BE-54 | PASS | |
| BE-46 | PASS | R58 = PVC FRP trim system profiles, same grouping as rev12 (see comment) |
| BE-47 | PASS | Re-tested: C16 / C25 now end with "Revised by RFI-55 ..." (852.20 SF; 154.32 LF + division bars 167 = 32 + 135). Was: Pending Items C16 (RFI-13) still reads "FRP + 1,030.64 SF (Cafe Work Room 875.20 ...)"; R37 now carries 852.2. C25 (RFI-22) still reads "PVC trim + 244.64 LF"; R58 types 3/4 now carry 154.32 + division bars |
| BE-57 | PASS | R37 / R58 non-metal = B6 |

## Blocking issues
None. B1 (BE-47) is fixed in the rebuild.

## Non-blocking comments
- 6/A-225: the coordinator states this is the Back Countertop Detail, printing "3'-0" AFF TO COUNTERTOP" (the source of the 3.0 ft height). Accepted; no crop was checked.
- The decision list was relayed by the coordinator; RFI_PVC.md contains the review only, with no decision section. RFI_PVC observation 2 also listed +19.0 LF top edge below the countertop, which is not carried. That is consistent with the relayed decision, since the countertop covers that edge.
- R58 mixes J-mold, inside corner, outside corner, edge trim and division bar profiles. The supplier order needs LF by profile, which the breakdown gives.
- R58's breakdown has no final "= 887.62 LF" line; adding one is optional.
- Scope Checklist D21 still ends "FRP-1 extent RFI-13 / RFI-22 not carried" (inherited, contradicts QUANTIFIED) and does not mention the Cafe below-countertop FRP. Update the text.
- Inherited from rev12: 0 % waste on yield and small-count rows (standing rule); snake_case kinds in Partition Takeoff A96-A109 and MS I49.

## Addendum (markups rev13, 2026-10-28)
The Excel was rebuilt after the markups update. The only cell that differs from the back-checked file (md5 0941eb1e) is the hidden `_reglas!A2` seal (canon hash), which changed because the canon gained `markup_label`. Every visible cell is identical: 0 differences in Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items and Scope Checklist. The verdict above stands for the rebuilt file.
