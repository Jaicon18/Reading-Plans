# RESUMEN rev5 — CR City Hotel (code review applied to the base)

Base = rev4 FINAL (kept unchanged in Drive). Source = "Revision de codigo 2026-11-06" (RESUMEN v2, punto1.json, punto2.json).
Rule applied: while an RFI is open, the BASE carries the larger option and the other option goes as a DEDUCT ALTERNATE with its delta.
Code sections verified in ICC (codes.iccsafe.org, IBC 2018) on 2026-11-06 by Claude in Chrome — _PUENTE_CLAUDE COD-001.

## Base changes

| # | Change | Drawing source | Code | SF | Status |
|---|---|---|---|---|---|
| 1 | 54 L4 rated rows extended to the underside of the roof sheathing; depth per S1.05 framing zone (RT-1 1.5 ft default; RJ-1 / RJ-2 / RJ-3 zones) | 2/A0.10, 10/A9.03 (CH), 1/A5.06 8'-11 1/4" LEVEL 4 to underside of roof framing, S1.05 | IBC 2018 §707.5, §708.4 | 1,665.68 | [DERIVADO] length x faces x layers x depth over the run |
| 2 | ELEC/TELE 120 2 HR, 4 walls (W.6-L1-24, W.6-L1-25 -> W.6-2; new W.6-L1-23 C / D) | 1/A7.50; A0.00 "ELECTRICAL AND IT ROOMS - 2 HR"; 1/A0.01 "2HR FB" | IBC 2018 §707.1, §707.5 (the 2 HR comes from the drawings; Table 509 does not rate electrical / IT rooms) | 341.76 | [DERIVADO] 50.16 + 192.24 + 33.12 + 66.24 — RFI-23 |
| 3 | DATA 118B 2 HR (new W.6-L1-20 C, W.6-L1-23 E / F) | 1/A7.50; A0.00 | IBC 2018 §707.1, §707.5 | 360.24 | [DERIVADO] 139.20 + 73.68 + 147.36 — RFI-24 |
| 4 | FW.4-L4-19 1 HR (FW.4-L4-19 A / B; bar face added) | A0.06 FW rows; 1/A2.04 | IBC 2018 §708.4 | 144.09 | [DERIVADO] bar face 12.07 x 10.4375 = 125.98 + corridor face head 12.07 x 1.5 = 18.11 — RFI-25 |
| 5 | XW.6.6-2 L4 interior face: NOT loaded | 04/A9.05 "ROOF DETAIL - PITCHED LEVEL 4 ROOF": interior board ends at the top plate / ceiling, heel space spray foam (image Auditoria/code_review_rev5/P5_rev5_A905_04.png) | — | 0 | [DERIVADO] no new RFI |

Sum of changes = 2,511.77 SF [DERIVADO 1,665.68 + 341.76 + 360.24 + 144.09]; matches the NET board delta 2,511.73 SF (Type X 2,269.30 + W.R. 205.45 + shaftliner 36.98), 0.04 SF rounding.

## Corrections vs the code-review figures
- Point 1: 1,665.68 SF, not 1,704.14. The 5 cement-board overlay rows were extended in the review on top of the rated layers of the same face: 38.44 SF double counted. They are not extended in rev5.
- Point 4: 144.09 SF, not 107.88. 107.88 was the bar face at 8.9375 ft; per point 1 a rated wall on L4 goes to the sheathing on both faces (+18.10 bar face head, +18.11 corridor face head).

## DEDUCT ALTERNATES (Proposal)

| ID | RFI | Alternate | Delta SF |
|---|---|---|---|
| DA-1 | RFI-23 | ELEC/TELE 120 walls as tagged on 1/A7.50 (W / S / E rated 0) | -341.76 |
| DA-2 | RFI-24 | DATA 118B west and east walls as tagged (W.6-0) | -360.24 |
| DA-3 | RFI-25 | FW.4-L4-19 as FW.4-0 (no rating) | -144.09 |
| DA-4 | — | XW.6.6-2 L4 interior face to sheathing: not in base | 0 |

## NET material delta rev4 -> rev5

| Material | Unit | Delta |
|---|---|---|
| 5/8" Type X | SF | +2,269.30 |
| 5/8" Type X W.R. | SF | +205.45 |
| 1" shaftliner | SF | +36.98 |
| Joint compound | LB | +178.18 |
| Paper tape | LF | +915.66 |

## Checks
- verif_codigo.py on rev5: ROOF_HEAD 0 red; XW_FSD 0 red / 17 amber (FSD of 0-rated exterior walls not printed on the code plan; IBC 2018 Table 602); ROOM_MIX 6 flags:
  - 120 and 118B: remaining flag is the original W.6-0 row of the shared wall; the added rows (W.6-L1-23 C/D/E/F, W.6-L1-20 C) carry the 2 HR layers on those segments.
  - 113, 115, 117, 119: the 2 HR wall belongs to the adjacent rated stair / elevator enclosure; the room itself is not a rated room on A0.00.
- Delivery gate: PASS 172 / AMBER 4 / FAIL 0 (GREEN). Proposal: 0 missing items.
- All rev5 images reopened: Auditoria/code_review_rev5/.
