# ENSAMBLE / CUADRE — Chuze Fitness Austin Bluffs, take-off rev1 (2026-11-01; rev0 files kept alongside)

Excel built only by `plantilla_excel.py armar` (reglas.py compuerta inside) and checked by `verificar`. Every
number below is read back from the delivered files (canon / Excel), none typed.

## 1. LF per type: reconciled canon vs Partition Takeoff

| Type (A301 order) | Canon walls | Canon LF | Excel rows | Excel LF | Δ LF |
|---|---|---|---|---|---|
| A2-3D | 3 | 98.05 | 3 | 98.05 | +0.00 |
| A3C | 22 | 206.17 | 19 | 206.17 | -0.00 |
| A6C | 3 | 23.83 | 3 | 23.83 | +0.00 |
| A6D | 27 | 391.08 | 26 | 391.07 | -0.00 |
| B2E | 5 | 103.96 | 5 | 103.96 | +0.00 |
| C3C | 6 | 24.54 | 6 | 24.54 | +0.00 |
| C3D | 9 | 44.86 | 6 | 44.86 | +0.00 |
| C3G | 0 | 0.00 | 0 | 0.00 | +0.00 |  (no tag on any plan: types_none_reason)
| D3F | 0 | 0.00 | 0 | 0.00 | +0.00 |  (no tag on any plan: types_none_reason)
| D3G | 6 | 60.01 | 5 | 60.01 | +0.00 |
| D6F | 2 | 22.41 | 2 | 22.41 | +0.00 |
| D6G | 2 | 26.44 | 2 | 26.44 | +0.00 |
| X6D | 1 | 5.37 | 1 | 5.37 | +0.00 |
| OTHER FRAMING - SOFFIT SIDE | 11 | 220.24 | 11 | 220.24 | +0.00 |
| **Total** | 97 | **1226.96** | 89 | **1226.96** | -0.00 |

Partition GRAND TOTAL cell (partitions only, OTHER FRAMING excluded): 1006.721

Excel rows < canon walls where untagged returns (`part_of`) join their tagged wall in one row (ids joined with '+', PT2).

## 2. Material Summary (NET without waste; pieces = ROUNDUP(NET x (1 + waste) / stock))

| Material | Unit | NET | Waste % | Purchase | Selling unit | Pieces |
|---|---|---|---|---|---|---|
| Bottom track 3-5/8" | LF | 531.68 | 0.15 | 611.43 | run 10 ft | 62 |
| Bottom track 6" - per source | LF | 446.72 | 0.15 | 513.73 | run 10 ft | 52 |
| Bottom track 6" - 600T250-54 | LF | 22.41 | 0.15 | 25.77 | run 10 ft | 3 |
| Bottom track 2-1/2" | LF | 103.96 | 0.15 | 119.55 | run 10 ft | 12 |
| Top / deflection track 3-5/8" | LF | 531.68 | 0.15 | 611.43 | run 10 ft | 62 |
| Top / deflection track 6" - per source | LF | 446.72 | 0.15 | 513.73 | run 10 ft | 52 |
| Top / deflection track 6" - 600T250-54 | LF | 22.41 | 0.15 | 25.77 | run 10 ft | 3 |
| Top / deflection track 2-1/2" | LF | 103.96 | 0.15 | 119.55 | run 10 ft | 12 |
| 2-1/2" stud | LF | 2,009.04 | 0.15 | 2,310.40 | stick 20 ft | 116 |
| 6" metal stud (LF of material) - per source | LF | 11,246.87 | 0.15 | 12,933.90 | stick 20 ft | 647 |
| 6" metal stud (LF of material) - 600S162-33 | LF | 432.00 | 0.15 | 496.80 | stick 20 ft | 25 |
| 3-5/8" metal stud (LF of material) | LF | 10,545.09 | 0.15 | 12,126.85 | stick 20 ft | 607 |
| Ceiling perimeter track at GWB ceilings (size not printed, RFI) | LF | 567.58 | 0.15 | 652.72 | run 10 ft | 66 |
| Bracing 1-1/2" C.R. channel | LF | 5,390.39 | 0.15 | 6,198.95 | C.R. channel 16 ft | 388 |
| Hanger wire | LF | 2,428.49 | 0.15 | 2,792.76 | continuous coil (LF) | 2,793 |
| 5/8" gypsum board, MOISTURE RESISTANT | SF | 5,483.88 | 0.06 | 5,812.91 | 4x12 ft sheet (Inputs) | 122 |
| 5/8" gypsum board, Type X | SF | 30,456.68 | 0.06 | 32,284.08 | 4x12 ft sheet (Inputs) | 673 |
| 5/8" gypsum board, Type X W.R. (water resistant) | SF | 1,475.02 | 0.06 | 1,563.52 | 4x12 ft sheet (Inputs) | 33 |
| Armstrong HD8906 drywall grid main tee (heavy-duty main runner, spec 09 51 23) | LF | 523.35 | 0.15 | 601.85 | main tee 12 ft | 51 |
| Armstrong XL8945P drywall grid cross tee (spec 09 51 23) | LF | 969.80 | 0.15 | 1,115.27 | cross tee 4 ft | 279 |
| Armstrong KAM151220E knurled angle molding at the C-5 perimeter (spec 09 51 23) | LF | 458.91 | 0.15 | 527.75 | molding 12 ft | 44 |
| Cement board screws 1-1/4" (manufacturer spacing) | PCS | 1,451.72 | 0.15 | 1,669.48 | piece | 1,670 |
| #10 framing screws - printed stud-to-track fastener (see Where it comes from) | PCS | 1,148.00 | 0.15 | 1,320.20 | piece | 1,321 |
| Deep-leg slotted deflection track - printed product (see Where it comes from) | LF | 11.00 | 0.15 | 12.65 | run 10 ft | 2 |
| Metal stud blocking at wall-mounted items (notes) | LF | 225.31 | 0.15 | 259.11 | stick 20 ft | 13 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - corner bead | LF | 441.22 | 0.15 | 507.40 | trim stick 10 ft | 51 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - gypsum edge trim | LF | 1,335.77 | 0.15 | 1,536.14 | trim stick 10 ft | 154 |
| 5/8" cement backer units behind tile (A301 type notes; spec 09 29 00 2.5) | SF | 1,209.77 | 0.06 | 1,282.36 | 4x12 ft sheet (Inputs) | 27 |
| Control joint, gypsum board walls (ASTM C840, 30 ft max) | LF | 363.93 | 0.15 | 418.52 | trim stick 10 ft | 42 |
| Hanger wire 12 ga - hanger count (one per hanger, height per room) | PCS | 187.00 | 0.00 | 187.00 | each | 187 |
| Additional head track at openings over 4'-0" wide | LF | 0.00 | 0.15 | 0.00 | run 10 ft | 0 |
| Stud reinforcement at MEP penetrations | PCS | 0.00 | 0.00 | 0.00 | each | 0 |
| Extra framing - ATM recess (only what a detail prints at the recess; the wall stays in its type) | LF | 0.00 | 0.15 | 0.00 | stick 20 ft | 0 |
| 2-1/2" CFMF @ 16" O.C. at coiling grille head (detail per plans) | LF | 0.00 | 0.15 | 0.00 | stick 20 ft | 0 |
| Gypsum board jamb return at openings | SF | 0.00 | 0.06 | 0.00 | 4x12 ft sheet (Inputs) | 0 |
| PVC trim - edge trim molding and inside corner molding at the FRP | LF | 0.00 | 0.06 | 0.00 | trim stick 10 ft | 0 |
| Power-driven fasteners and duct sleeves | PCS | 0.00 | 0.00 | 0.00 | each | 0 |
| Access panel 24"x24" | PCS | 1.00 | 0.00 | 1.00 | each | 1 |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | 44,898.70 | 0.00 | 44,898.70 | each | 44,899 |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | 4,940.00 | 0.00 | 4,940.00 | each | 4,940 |
| Power-driven fasteners, slab pins for the bottom track | PCS | 828.60 | 0.00 | 828.60 | each | 829 |
| Expansion anchors Hilti 1/4" Kwik Bolt II, exterior bottom track @ 8" O.C. | PCS | 0.00 | 0.00 | 0.00 | each | 0 |
| Joint compound, all purpose | LB | 2,693.92 | 0.00 | 2,693.92 | lb | 2,694 |
| Joint tape, paper | LF | 13,843.76 | 0.00 | 13,843.76 | LF | 13,844 |
| Level 5 finish | SF | 0.00 | 0.06 | 0.00 | SF | 0 |
| Deflection clips at non-load-bearing walls to structure | PCS | 0.00 | 0.00 | 0.00 | each | 0 |
| Heavy-gauge framing screws #10-16 x 3/4" pan head (18/16/14 ga studs) | PCS | 0.00 | 0.00 | 0.00 | each | 0 |
| Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | PCS | 0.00 | 0.00 | 0.00 | each | 0 |

## 3. Gates (last run, bitacora.jsonl)

| Gate | rc | Note |
|---|---|---|
| plantilla_excel.py armar (reglas.py compuerta inside) | 0 | Excel written and sealed (_reglas sheet) |
| plantilla_excel.py verificar | 0 | EXCEL v67 OK |
| markups_bluebeam.py verificar | 0 | MARKUPS OK, 97 annotations = 97 canon walls / elements |
| registro.py entregable | 0 | 22 verified + 2 pendiente_rfi (ALC-05, ALC-17), 0 pending |
| alcances.py compuerta | 0 | ALCANCES OK against the Excel |
| reglas.py compuerta etapas --excel | 1 | only failure: S:§1:2fab33 'back-check made on another version of the Excel' (the registered back-check is the rev0 Excel; a new entry only after the auditor re-verifies rev1) |
| etapas.py compuerta etapas | 0 | COMPUERTA ETAPAS: PASA |
| bitacora.py compuerta | 1 | 4 lines, all from the back-check registered on the rev0 Excel hash (reglas rc 1 = same cause) |

## 4. Canon additions in Stage 4-5 and rev1 (no measured wall length changed; rev1 deltas in CAMBIOS_rev1.md)

1. accesorios_rfi += "gypsum board jamb return": accesorios.py left the family PENDIENTE (no opening with jamb_return).
   Plan: only unframed openings = 2 cased openings (A426, A429); no cased-opening section in the set (A602 = door /
   storefront heads only; 'CASED' appears only in G001 abbreviations). Rule 0.F -> 0 loaded + RFI with delta.
2. Status labels normalized to the schema tokens (SKILL §1 #0, reglas A_ESTADO_DIM): CONFIRMED/DERIVED/PENDING ->
   CONFIRMADO/DERIVADO/PENDIENTE in *_status / status keys only (scripts/normalizar_estados.py). No value changed.
3. constants.slab_pin_spacing_ft = 1.3333 ft (16" O.C.) from the S200 BOTTOM TRACK ANCHORAGE SCHEDULE called by B/S200
   (accesorios.py used its 1.0 ft default without it; the canon details already cite the 16" spacing).
4. Evidence / format fields for reglas.py (scripts/enriquecer_evidencia.py, log enriquecer_log.txt, 348 changes):
   to_deck_source (head detail N/HOJA printed in top_track), face height_source sheet citation, soffit-side detail
   citation, details source N/HOJA, RFI source + delta (from their options A/B/C), pending_reason + sheets_searched
   on PENDIENTE walls (from the RFIs they cite), dimension-chain tick statement (chain vs vector cross-check),
   storefront / cased sill_ft 0 + source, storefront structure 'steel' (8/A602, RFI-12), pier faces_ft +
   fos_chain_faces (the canon faces), A2-3D rows_source, untagged_reason sheet, gaps_ok / corners_ok read on the
   plan (resolucion.md R-27 + crops scratch/E45/g_A429.png, g_A424.png, g_A431.png), and 5 wording fixes of '~'.
5. Evidence images by program: runner/evidencia.py (img / height_img / detail_img / stud_img, never overwrites),
   images in 4_canon/img_evid/.
6. Stud gauge placeholder 'PENDING' (not printed) -> the assumption the RFI says is LOADED (RFI-04: 20 ga at head D/E
   walls, 25 ga at head C/F/G walls; RFI-09: 20 ga soffit framing), original text kept in gauge_pending_info
   (scripts/gauge_rfi.py). The RFIs stay open; no tool family depends on 20 / 25 ga (heavy-gauge screws = 18/16/14 only).
   Reason: plantilla_excel.verificar refuses any 'PENDING' cell in a Partition Takeoff row; the Stud Size cell now
   shows the loaded assumption with its RFI.
7. Soffit-side stud_size 'PENDING - 6" assumed (RFI-09)' (4 walls) -> '6" (not printed - assumed, RFI-09 ...)'; the
   original text kept in stud_size_pending_info. Same family (6") in canon.py before and after.
8. rev1 (step 11 / 12 gaps, scripts/rev1_canon.py, refs 'R1-'): misc_items (control joints, tile backer + screws, RTU
   curb caps + TEK, A502 box headers, 6/A502 diagonal braces, head F board cap, head C kickers, Retail Storage 126 studs
   to deck + bracing, 1/A506 hatch tracks), trim_items (head F metal edge, L-bead at board ends against the deck, corner
   bead at the C3C boxes and cased openings), blocking_items (A103 tracks, metal straps, 10/A505.B studs), MR + mr_source
   on the 2 Men's Locker soffit faces, ceilings moldings = angle only + source C-5/A121, constants.product_names
   (Armstrong grid, cement backer), plan_scale_by_sheet for A421.A-A425.A (18 pt/ft printed), band.path for the arc and
   the 3-side boxes, accesorios_none with sheets for the 0 rows, token / citation fixes in RFI texts. Wall lengths,
   heights and faces unchanged (except the 2 MR faces).

## 5. Files

| File | Bytes | sha256 (12) |
|---|---|---|
| CAMBIOS_rev1.md | 6,872 | 4991c3ca9d64 |
| Chuze_AustinBluffs_Markups_rev0.pdf | 220,449,999 | b83d4f3ff537 |
| Chuze_AustinBluffs_Markups_rev1.pdf | 220,451,000 | 71de084e5143 |
| Chuze_AustinBluffs_Takeoff_rev0.xlsx | 49,409 | 2536ef0c6c7a |
| Chuze_AustinBluffs_Takeoff_rev1.xlsx | 53,701 | 66ce8d3a6e2d |
| ENSAMBLE_CUADRE.md | 13,795 | 6376c819aa11 |
| RESPUESTA_FINAL.md | 1,417 | 4783d66e3238 |
| RESPUESTA_FINAL_rev1.md | 878 | f975525456aa |
| imagenes/A101_walls_by_type.png | 1,293,097 | d498a5dac00b |
| imagenes/A421.A_walls_by_type.png | 1,322,252 | 02848fe767a8 |
| imagenes/A421_walls_by_type.png | 1,603,019 | 42cfe724421b |
| imagenes/A422.A_walls_by_type.png | 980,619 | 1b78a2ffa261 |
| imagenes/A422_walls_by_type.png | 1,097,796 | 3c479d4759b1 |
| imagenes/A423.A_walls_by_type.png | 1,410,086 | 2adf8fda1254 |
| imagenes/A423_walls_by_type.png | 1,739,017 | 7dad6d22cf3c |
| imagenes/A424.A_walls_by_type.png | 1,283,342 | 57128bde469f |
| imagenes/A424_walls_by_type.png | 1,958,362 | 05482b1916f2 |
| imagenes/A425.A_walls_by_type.png | 1,270,198 | 4e6713e7f625 |
| imagenes/A425_walls_by_type.png | 1,916,281 | f36ad2646318 |
| imagenes/A426_walls_by_type.png | 1,470,122 | 74f54a223e00 |
| imagenes/A427_walls_by_type.png | 1,448,708 | b6c7c127c501 |
| imagenes/A429_walls_by_type.png | 1,773,156 | 9b65eef262a2 |
| imagenes/A431_walls_by_type.png | 1,534,769 | b46c28192c6a |
| imagenes/A432_walls_by_type.png | 4,095,825 | 0a0661a5c845 |
| imagenes/A434_walls_by_type.png | 989,573 | fc9eaf690c43 |
| imagenes/A435_walls_by_type.png | 1,345,891 | e49b27d3fbe3 |
| imagenes/imagenes_resumen.json | 4,471 | 42945d55cbee |
| imagenes_rev1/A101_walls_by_type.png | 1,293,524 | 328500ced4f7 |
| imagenes_rev1/A421.A_walls_by_type.png | 1,322,627 | 6ff249e5e1a8 |
| imagenes_rev1/A421_walls_by_type.png | 1,603,464 | ed65989b1da5 |
| imagenes_rev1/A422.A_walls_by_type.png | 981,007 | 20caaf9835df |
| imagenes_rev1/A422_walls_by_type.png | 1,098,167 | 278d1d6b5284 |
| imagenes_rev1/A423.A_walls_by_type.png | 1,410,461 | a373da065481 |
| imagenes_rev1/A423_walls_by_type.png | 1,739,338 | 1849cbcc02d5 |
| imagenes_rev1/A424.A_walls_by_type.png | 1,283,780 | d8b419c51c8b |
| imagenes_rev1/A424_walls_by_type.png | 1,958,714 | f334820363df |
| imagenes_rev1/A425.A_walls_by_type.png | 1,270,537 | 9a1e60bddfd8 |
| imagenes_rev1/A425_walls_by_type.png | 1,915,397 | 29e98d037b22 |
| imagenes_rev1/A426_walls_by_type.png | 1,470,490 | a97ed55d517e |
| imagenes_rev1/A427_walls_by_type.png | 1,449,057 | 0a182008f512 |
| imagenes_rev1/A429_walls_by_type.png | 1,773,514 | f3716d2df03e |
| imagenes_rev1/A431_walls_by_type.png | 1,535,132 | cfded06f0428 |
| imagenes_rev1/A432_walls_by_type.png | 4,095,678 | 6f5db4a19e47 |
| imagenes_rev1/A434_walls_by_type.png | 989,903 | 4c48c22b5986 |
| imagenes_rev1/A435_walls_by_type.png | 1,346,233 | 18957dbe5553 |
| imagenes_rev1/imagenes_resumen.json | 4,471 | 42945d55cbee |
