# Barnes & Noble – Colorado Springs — Metal Frame & Drywall Take-off — rev12

rev12 = rev11 plus the estimator decisions on the 34 RFIs (`../RFI_REVISION_ESTIMADOR.json`, 2026-10-27).
- The rev11 change is kept: wood blocking uses the non-metal waste (Inputs B6) and 16 ft sticks (Inputs B26). It now comes from the pipeline, not a hand edit.
- Counts used:
  - `../rfi_mep_cruces/` (8 duct crossings + 2 TG-1);
  - `../rfi29_corner_guards/` (72 + 1);
  - `../rfi43_cement_board/` (E1 to 12'-0");
  - `../rfi49_cased_openings/` (0 cased openings).
- Wall LF does not change. The markups PDF and the images are the rev11 ones (`Planos marcados/`).
- Rule R80e.30: only the touched rows were verified.
- Format: 6 sheets, no new sheets or columns, waste metal B5 / non-metal B6. One Inputs row was added: B30, FRP panel SF.

## Changes rev11 → rev12 (Material Summary Net)
| Material | Unit | rev11 | rev12 | Δ | Δ % |
|---|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 15,109.29 | 14,266.95 | -842.34 | -5.6 % |
| 1/2" cement board / cementitious backer | SF | 739.90 | 434.28 | -305.62 | -41.3 % |
| Blocking 2X wood (not labeled FRT) | LF | 17.00 | 0 (removed) | -17.00 | -100.0 % |
| FRT plywood substrate (5/8 in.) | SF | 1,790.51 | 2,686.45 | +895.94 | +50.0 % |
| FRT plywood substrate (3/4 in.) | SF | 402.46 | 370.46 | -32.00 | -8.0 % |
| Additional head track at openings over 4'-0" wide | LF | 10.67 | 83.32 | +72.65 | +680.9 % |
| Stud reinforcement at MEP penetrations | PCS | 0.00 | 10.00 | +10.00 | new |
| PVC trim - edge trim molding and inside corner molding at the FRP | LF | 0.00 | 530.54 | +530.54 | new |
| Power-driven fasteners and duct sleeves | PCS | 0.00 | 8.00 | +8.00 | new |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | 6,114.04 | 5,103.23 | -1,010.81 | -16.5 % |
| Power-driven fasteners, slab pins for the bottom track | PCS | 777.43 | 388.72 | -388.71 | -50.0 % |
| Joint compound, all purpose | LB | 1,166.54 | 1,105.89 | -60.65 | -5.2 % |
| Joint tape, paper | LF | 5,994.70 | 5,683.03 | -311.67 | -5.2 % |
| FRP panels | SF | — | 1,967.38 | +1,967.38 | new |
| Moment clip ClarkDietrich MC series with stiffening plate (A/A-410), one per stud of types 3 / 4 | PCS | — | 162.00 | +162.00 | new |
| Hilti Kwik HUS-EZ 1/4" x 1-5/8" concrete screws at the moment clips (3/A-410, 4/A-410) | PCS | — | 324.00 | +324.00 | new |
| #10-16 screws at the moment clips, (1) at each flange (A/A-410) | PCS | — | 324.00 | +324.00 | new |
| Metal corner guard 2"x2"x72" at outside corners (A-001A) | PCS | — | 72.00 | +72.00 | new |
| Stainless steel corner guard 48" A.F.F. (C22/A-101) | PCS | — | 1.00 | +1.00 | new |
| Control joint, gypsum board walls (ASTM C840, 30 ft max) | LF | — | 250.00 | +250.00 | new |
| #8 screws at diagonal brace ends, 2 per end (manufacturer rule; 3/A-410 prints none) | PCS | — | 512.00 | +512.00 | new |

Partitions total: no change, **569.82 LF**. Rows not listed are unchanged.

## How each RFI was closed
In the Pending Items sheet, every RFI in the decision file now reads "CLOSED - estimator decision 2026-10-27: …", with its N/SHEET and the delta applied.
- **Excluded, with a Scope Checklist note:**
  - RFI-30, access panels (ALC-17);
  - RFI-36, W-3 blocking by GC / fixture installer (ALC-16);
  - RFI-50, server room plywood by GC (ALC-10).
- **Kept as carried:** RFI-03, 05, 32, 33, 35, 38, 39, 40, 41, 42, 45, 46, 47, 48, 52, 53 and 54.

| RFI | Decision | Applied |
|---|---|---|
| RFI-ACC-slab-pins | B: 1 row @ 16" | slab pins 777.43 → 388.72 |
| RFI-ACC-stud-reinforcement-mep | A: count on M-102 | plates 10 (8 ducts + 2 TG-1), duct sleeves 8 |
| RFI-09 / RFI-31 | B: 2-piece header at every door | head track 10.67 → 83.32 LF (9 doors; RFI-31 is inside it) |
| RFI-13 | B: FRP-1 in scope | FRP + 1,030.64 SF + PVC trim |
| RFI-21 | A: cloud fascia GWB | 5/8" Type X + 53.6 SF |
| RFI-22 | B: one face of types 3 / 4 | FRT plywood 5/8" + 936.74 SF, FRP + 936.74 SF, GWB − 936.74 SF, PVC trim + 244.64 LF |
| RFI-24 | A: control joints | + 250.0 LF |
| RFI-28 | A: moment clips | + 162 clips, + 324 HUS-EZ, + 324 #10-16 |
| RFI-29 | Both | metal corner guards 72, stainless 48" 1 |
| RFI-43 | A: E1 to 12'-0" | 1/2" cement board − 305.62 SF |
| RFI-44 | WD-1 to 15'-0" | FRT plywood − 40.8 SF, 5/8" Type X + 40.8 SF |
| RFI-49 | 0 cased openings | 2x wood blocking − 17.0 LF |
| RFI-50 | Excluded | 3/4" FRT plywood − 32.0 SF |
| RFI-51 | Brace end screws | + 512 #8 screws |

## Error library
Independent back-check of the final Excel: **PASS WITH COMMENTS — LIBRARY 44 PASS · 0 FAIL · 3 N/A**, BE-57 included. It confirms all 34 RFI decisions and the 21 expected changes. See `takeoff_work/etapas/5_auditoria/BACKCHECK_rev12.md`. The first pass found 2 FAIL, both fixed:
- BE-41: internal folder names in Pending Items.
- BE-40: the head track breakdown was cut off.

Comments (not blocking):
- **0 % waste on two kinds of rows, by the standing rule since v67.** Accessory yield rows (screws, pins, compound, tape) carry the yield instead of waste. Counted schedule pieces of 20 PCS or fewer also carry none: stainless corner guard 1, plates 10, sleeves 8, hanger count.
- **Head track row:** the breakdown lists all 9 doors, and the total of 83.32 LF is in the Net column.
- **PVC trim (530.54 LF):** derived as J-mold top and bottom plus inside corners. RFI-13 gave no figure, so the estimator should confirm it.

## Gates
- REGLAS OK (820 rules, 0 failures)
- ALCANCES OK (24 reviewed, 2 RFI)
- `registro.py entregable` OK
- EXCEL v67 OK
- ETAPAS PASA
- BITACORA OK (17 mandatory tools current + back-check)

Skill **v80r**: rule R80e.35 (estimator decisions in the pipeline: estimator MEP count, N-piece door header, FRP + PVC by items, new families, RFI closure in Pending Items). It also syncs R80e.33 / R80e.34. Packed with `zip -qrD` (132 files). test_ciego_tools and test_smoke_ciego pass. File: `take-off-metal-frame-drywall_FINAL_v80r.zip`.

Drive: not uploaded. Nothing sent to the client.
