# Rev6 changes: O'Reilly Auto Parts, Evans CO, pass 2 (element 3, studs / Z-furring)

Backups: `takeoff_canon_AB_rev5.json` and `overlay_OReilly_p2_rev5.json`.

Edited files:
- `takeoff_canon_AB.json` (the reading):
  - S21 gauge, on 5 walls
  - KICKERS-S42-HDR op
  - RFI-03 rewritten
  - new RFI-19
- `overlay_OReilly_p2.json` (G09):
  - ops of PEMB-6IN-S42-02, PEMB-6IN-S42-01 and L4X4-S42-03
  - RFI-10 closing text
- `overlay_mapeo.md`: row 09.
- `canon_ov.json`, regenerated with `overlay.aplicar_canon`. Applying it twice gives the same result.

Checks:
- `validar_canon.py` reports CANON OK on both files.
- `tools/canon.py canon_ov.json /tmp/rev6_out` gives `partition_types.avisos = []`.

No carried quantity changed. The only tool-output change is the split of the excluded framing / drywall screws, because S21 is now light gauge.

Rule #0 applies: no length was scaled. All crops are in `img_rev6/`. Each one was rendered with pymupdf from `bidset_SIN_MARKUPS.pdf`, circled, then reopened and checked.

| # | Item | Before (rev5) | After (rev6) | Printed dimension / N/SHEET | Image |
|---|---|---|---|---|---|
| 1 | PEMB-6IN-S42-02 | 14 x 5.0 = 70.0 LF. The 5.0 ft was a scaled purlin bay ("271 pt at 54 pt/ft") | **70.0 LF**, [PENDIENTE] **RFI-19 option A**:<br>**Count:** 14 = ROUNDUP(25.455/2)+1. The @ 24\" O.C. is printed on 1/S5.1.<br>**Length:** 5'-0\" = 2/S5.1 5'-0\"+-, the only printed horizontal on the S42 header details.<br>**(B)** 10'-0\" stock, reaching one purlin past the kicker top as drawn: 140.0 LF (+70.0) | 1/S5.1 \"6\"x2\"x16ga STUDS (600S200-54) @ 24\" O.C. ... ATTACH TO EACH PURLIN\". No length dimension | rev6_p1p2p3_S5.1_1_6in_24oc_no_length.png |
| 1 | PEMB-6IN-S42-01 | 11 x 5.0 (scaled) = 55.0 LF | **55.0 LF**, [PENDIENTE] **RFI-19 option A**:<br>**Count:** 11 = ROUNDUP(38.667/4)+1, from the @ 48\" printed on 4/S5.1.<br>**Length:** 5'-0\" (2/S5.1).<br>**(B)** 110.0 LF (+55.0) | 4/S5.1 \"600S200-54 @ 48\" O.C. FASTEN TO EACH PURLIN\". No length dimension | rev6_p1p2_S5.1_4_6in_48oc_no_length.png |
| 1 | L4X4-S42-03 | ROUNDUP(50.333/5.0)+1 = 12 pcs (purlin spacing scaled) | **12 pcs**, [PENDIENTE] **RFI-19 option A**: 5.0 ft = 2/S5.1 5'-0\"+- used as a **proxy**. That dimension is the kicker reach, not the purlin spacing, which is not printed.<br>**(B)** one per kicker @ 48\" O.C. (MAX): 14 pcs (+2) | 2/S5.1 L4x4x3/16x1'-0\" \"fastened to purlin web\", \"PURLIN BEYOND\", 5'-0\"+- | rev6_p1p3_S5.1_2_5-0_kicker_reach_purlin_beyond.png |
| 1 | RFI-19 (new) | - | **Question:** purlin spacing and member length, by PEMB shop drawing, not printed.<br>**Options:**<br>(A) 0, carried<br>(B) +70.0 / +55.0 LF 600S200-54, +2 L4x4<br>(C) other<br>**Sheets checked, no purlin spacing printed:** 1/2/4/5 S5.1, S4.1 framing key plan, S1.1 notes 7 and 9, S5.2, S5.3, A3.1, A3.2 (only \"T.O. PURLIN EL. (VARIES)\").<br>Estimator decision RFI 09 = A stands: the members are carried. RFI-10 stays CLOSED as a decision only | see left | all 3 above |
| 2 | S21-N/E/S/W1/W2 gauge | \"18 ga (150ZF125-18)\", source \"18 = 43 mil\" | **\"25 ga (18 mil, 150ZF125-18)\"**. In the SSMA designation the suffix is mils (S1.1 note 7.A), so -18 = 18 mil = 25 ga.<br>Size 1-1/2\" Z-furring and @ 24\" O.C. confirmed | S21/A1.1 \"150ZF125-18 ... AT 24\" O.C.\"; A3.1 key 10 | rev6_p2_A1.1_types_S21_S24.png, rev6_p2_A3.1_key8_600S162-43.png |
| 2 | S24 / S41 / S43 / S61 | 362S162-33 @ 24\" (S61 600S162-33 @ 24\") | **Confirmed, no change** | A1.1 types S24 / S41 / S43 / S61 | rev6_p2_A1.1_types_S21_S24.png, rev6_p2_A1.1_types_S41_S42_S43_S61.png |
| 2 | S42-01..04 | 362S162-33 @ 24\" | **Confirmed**. A1.1 says \"3-5/8\" ... (REFER STRUCTURAL)\". 1/S5.1, 2/S5.1 and 4/S5.1 print \"362S162-33 @ 24\" O.C. MAX\" | A1.1 S42; 1/S5.1, 2/S5.1, 4/S5.1 | rev6_p1p2p3_S5.1_1_6in_24oc_no_length.png, rev6_p1p2_S5.1_4_6in_48oc_no_length.png |
| 2 | EXT-MS / HEAD-A | 800S162-54 + 600S162-54 @ 16\" | **Confirmed** | S5.3 keys 17 / 18 | rev6_p2_S5.3_keys_17_18_22.png |
| 2 | CORN-S | 600S162-43 (minimum) @ 16\" | **Confirmed** | S5.3 key 22 | rev6_p2_S5.3_keys_17_18_22.png |
| 2 | VH-B1 / B2 / C | 600S162-43 @ 24\" | **Confirmed** (estimator decision 14) | A3.1 key 8 | rev6_p2_A3.1_key8_600S162-43.png |
| 2 | Ceiling joists CJ-* | 600S162-54 @ 24\" | **Confirmed** | A4.2 key 5 (7/A4.2) | rev6_p2_A4.2_key5_joists.png |
| 3 | KICKERS-S42-HDR | 22 x 7.07 = 155.54 LF; \"45 deg drawn\" in the op | **155.54 LF.**<br>**Count:** CONFIRMADO. 362S162-33 @ 48\" O.C. (MAX) is printed on 1/S5.1 and 2/S5.1.<br>**Length:** [PENDIENTE] **RFI-03 option A**. Only the 5'-0\"+- horizontal is printed; the 45 deg is drawn only.<br>**RFI-03 rewritten:**<br>(A) 0, carried<br>(B) -33.96 LF = 121.58 LF, from printed elevations. The foot is 1'-0\"+- above FINISH CEILING 111'-6\" (5/A4.2) = 12.5 ft. The head is at the underside of the purlin, 14.505 / 15.035 ft (RFI-01). Lengths are SQRT(5^2 + 2.005^2) = 5.387 for S42-02 and SQRT(5^2 + 2.535^2) = 5.606 for S42-03<br>(C) other.<br>The old B (\"+-1 ft x 20\") was dropped: the kicker count is 22, not 20 | 1/S5.1, 2/S5.1 (@ 48\" MAX, 1'-0\"+-, 5'-0\"+-); 5/A4.2; 6/A4.2 | rev6_p1p3_S5.1_2_5-0_kicker_reach_purlin_beyond.png, rev6_p1p2p3_S5.1_1_6in_24oc_no_length.png |

Not carried, noted only: 2/S5.1 also prints \"CONT. 6\"x2\"x16ga STUD (600S200-54) FASTENED TO PURLIN\" at the kicker top of S42-03. This is a third continuous line. CONT-6IN-S42-03 carries only the 2 lines at the wall top (\"each side\"), so the third line's 50.33 LF is open for the estimator. It was not added in this rev.
