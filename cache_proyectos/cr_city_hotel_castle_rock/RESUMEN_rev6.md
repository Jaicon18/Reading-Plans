# RESUMEN rev6 — CR City Hotel (adversarial audit by COORDINACIÓN, 2026-11-07)

Base = rev5 FINAL (code review + deduct alternates unchanged). Every finding was re-verified on the drawings, with the operation shown; images in Auditoria/auditoria_rev6/.

## Findings and what changed

| # | Finding | Drawing evidence | Result in rev6 |
|---|---|---|---|
| E1 | Lobby coffers counted twice | 2/A7.31 and 4/A7.31 print "1'-11 1/4\" RATED ASSEMBLY" with the 12'-0 3/4" level at its underside; 7/A7.31 puts 12'-0 3/4" at the underside of the rated membrane and the suspended ceiling panel at 11'-0". The coffer tag "GYP-1 12'-0 3/4\"" = the L1 FS-1 membrane, already loaded (7,928.8 SF). A0.08 "GC MAY ADD LAYER OF GYP BD" = GC option, not in the base. | CONFIRMED. CLG-L1-11 removed: -538.5 SF Type X, -134.62 LF main tee, -403.88 LF cross tee, -92.82 LF angle, -17 LF hanger wire. Images E1_*.png |
| E2 | Shower cement board short (201 / 301 west side) | 1/A2.02 and 1/A2.03: shower side from the wall face y 353.6 to the curb y 385.0 = 31.4/9 = 3.49 ft (rev5 used the pan diagonal end 358.0 = 3.0 ft). | CONFIRMED. Rule applied to ALL showers (wall face, not pan diagonal): 201 / 301 both sides 3.0 -> 3.48 ft; 309 N 3.12 -> 3.71; 310 7.0 -> 7.19; 309 W side 8.53 ft now loaded (same as 209 on L2, missed in rev5). Cement board +101.07 SF. Image E2_A202_shower201.png |
| E3 | Gate CB_BE_CF10 passed empty ("N/A: no specs") while the delivery cites 05 40 00 / 09 29 00 | Project Manual sections on file: 05 40 00, 06 10 00, 07 21 00, 07 84 13, 07 92 00, 09 21 16.23, 09 22 16, 09 29 00 | CONFIRMED. The check now reads the Project Manual (entrega.json specs_dir) and FAILS when the delivery cites a section it did not read; regression test test_cr_rev6_cf10_specs. Running for real, it found that the Material Summary rows did not cite their spec section: each row now cites it (09 29 00 2.3 / 2.4.A / 2.5 / 2.6, 09 22 16 2.2 / 2.3, 09 21 16.23 2.3.A / 2.4; exterior sheathing = no spec section on file, 06 10 00 refers to 06 16 00 'Sheathing', not received). |
| O1 | Angle molding = 4 x sqrt(area) | — | CONFIRMED (60 rows). Each row is now the measured room perimeter: union of the measured rectangles, the FS-1 polygon of the same room (218, 318, 322, 323), or rectangles read in vectors with an area check against the printed SF (128, 215, 216, 316, 417, 418, 421; images O1_*.png). Angle molding +575.38 LF (net with E1: +482.56 LF). |
| O2 | Corridor cove: L2 at 1.0 ft bottom, L3 / L4 at 0.375 ft | 7/A7.23 prints 7 3/4" (DIFFUSER BOX, HVAC) + 4 1/2" box; vertical 6 1/2" | CONFIRMED. Bottom = 4 1/2" = 0.375 ft on all three floors: SOF-L2-01 -95.16 SF, SOF-L2-02 -104.71 SF Type X. Image O2_A723_detail_7.png |

## NET material delta rev5 -> rev6

| Material | Unit | Delta |
|---|---|---|
| 5/8" Type X | SF | -738.38 (= -538.5 E1 - 95.16 - 104.71 O2) |
| 5/8" Type X W.R. | SF | -13.97 (W.R. strip above the longer cement board) |
| 5/8" cement board | SF | +101.07 |
| Main tee / cross tee | LF | -134.62 / -403.88 |
| Angle molding | LF | +482.56 |
| Hanger wire | LF | -17.00 |
| Joint compound / paper tape | LB / LF | -54.17 / -278.37 |

## Observation (not changed, for the estimator)
- 309 shower S side: on 1/A2.03 the shower pan ends about 7 pt (0.8 ft) before the wall line, so that side is not a shower wall in the drawing (209 on L2 is drawn tight to its wall and carries it). Delta if it were tiled like 209: +3.71 ft x 9.0 ft = +33.4 SF cement board.

## New rules (skill R80e.160) and gates
CB_CR_R6_E1 (ceiling at the underside of a rated assembly = the membrane), shower sides to the wall face (snap_caja), CB_BE_CF10 reads specs_dir, CB_CR_R6_O1 (no sqrt perimeters), CB_CR_R6_O2 (same printed width of a typical detail on every floor). Tests: test_cr_rev6_cf10_specs, test_cr_rev6_auditoria.
