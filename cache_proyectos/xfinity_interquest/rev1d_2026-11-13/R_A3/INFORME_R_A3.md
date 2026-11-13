# INFORME R_A3: A3.0 RCP tags, double ceiling, A0.3 specs, detector root causes

- **Reviewer:** Claude (Opus 5.5), independent reviewer R_A3 (read-only on canon, scripts, Excel and delivery)
- **Date-time:** 2026-11-13 16:36 UTC
- **Project:** Xfinity Interquest, drywall / metal framing take-off (bid today)
- **Inputs:** plans/bidset_SIN_MARKUPS.pdf (A3.0 = page 6, A0.3 = page 3, per SHEET_MAP.json); 4_canon/takeoff_canon.json; XF_Takeoff_FINAL_rev1.xlsx 'Material Summary'; AUDITORIA_ADVERSARIAL_2026-11-13.md + XF_A3.0_storage_hall_rcp.png
- **Coordinates:** x_pt / y_pt are pt in the rotated page space (page.rect 3024 x 2160, /Rotate 270). This is the same space the canon uses (SOF-01 band y 1618.2 / 1625.52, x 846.84 to 923.28 matches the T3 leader dot at (884.0, 1622.7)).
- **Outputs (all in /root/xf/work/revision_indep/R_A3/):** RCP_TAGS_A3.0.csv, DOBLE_CIELO.csv, A0.3_SPECS_vs_MS.md, A3.0_T1..T5 PNG crops (red = tag, blue = leader arrowhead dot). Every PNG was reopened with PIL, and T1, T3, T4b and T5 were also checked visually.

## 1. A3.0 tag by tag

Method: pymupdf `get_text('dict')` on page 6, then every line with "AFF" / "ACT" / "GYP" was read, rendered and its leader followed. A3.0 prints **5 tag boxes**. One leader (T4) branches to two rooms, so there are **6 room-ceiling assignments**. That matches the audit's "6". The words "EXISTING TOILET" / "EXISTING ACCESS. TOILET" are room names, not ceiling tags.

| # | Room | Printed tag | Height | x_pt, y_pt (tag centre) | Canon carries it as | Disposition |
|---|---|---|---|---|---|---|
| T1 | RETAIL 100 | NEW GRID AND TILES / 2x4 ACT / 12'-0" AFF | 12'-0" [CONFIRMED 1/A3.0] | 1228.5, 1938.5 | ceilings_info "NOT ours (ACT)"; ceilings = [] | EXCLUIDO: ACT = other trade (ALC-E01) |
| T2 | STORAGE 101 | EXIST. GRID & NEW TILES / 2x4 ACT / 10'-0" AFF | 10'-0" [CONFIRMED 1/A3.0] | 451.0, 1399.5 | ceilings_info "NOT ours" | EXCLUIDO: ACT = other trade (ALC-E01) |
| T3 | HALLWAY 102 north end (opening to Storage, where DEMO-01 is removed) | GYP. BD. / 8'-6" AFF (no "EXISTING") | 8'-6" [CONFIRMED 1/A3.0] | 451.0, 1552.5; leader dot 884.0, 1622.7 | SOF-01, height_ft 8.5: misc SOF-01-TRACK 16.988 LF, SOF-01-STUDS 15.0 LF, "SOF-01 board" 14.47 SF, trim CB-SOF-01 | **CARGADO** |
| T4 | HALLWAY 102 | EXISTING / GYP. BD. / 9'-0" AFF | 9'-0" [CONFIRMED 1/A3.0] | 451.5, 1698.0; dot 870.9, 1706.5 | ceilings_info "EXISTING to remain - not ours" | EXCLUIDO: existing to remain (ALC-E13 / ALC-11) |
| T4b | TOILET 103 (branch of the T4 leader, dot 810.0, 1684.9) | same tag as T4 | 9'-0" [CONFIRMED 1/A3.0] | 451.5, 1698.0 | ceilings_info "same tag leader branch ... existing, not ours" | EXCLUIDO: existing to remain (ALC-E13 / ALC-11) |
| T5 | ACCESS. TOILET 104 | EXISTING / GYP. BD. / 9'-0" AFF | 9'-0" [CONFIRMED 1/A3.0] | 451.5, 1922.0; dot 821.8, 1861.6 | ceilings_info "existing, not ours" | EXCLUIDO: existing to remain (ALC-E13 / ALC-11) |

**FALTA: none.** Every tag has a disposition in the canon. Notes:
- ALC-E13 in the Scope Checklist is worded for existing **walls** W1 / W4. The existing **ceilings** are actually covered by ALC-11 ("Hallway 102 / Toilets 103-104 tagged EXISTING ..."). Optional fix: add "existing gyp. bd. ceilings 9'-0" (1/A3.0) to remain" to ALC-E13.
- A0.1 general note 3 "PATCH ANY EXISTING WALLS AND/OR CEILINGS AS NEEDED" means a patch allowance for the existing 9'-0" ceilings is a Scope line, not a quantity. The audit already raised this.
- Landlord Room (N.I.C.) has no ceiling tag; it is excluded (canon excluded_areas).

## 2. DOBLE_CIELO (Golden Rule #3)

DOBLE_CIELO.csv uses the gate header exactly (compuerta_entrega.py COLS_DOBLE / doble_cielo_fallas): `Room,Level,Type,Upper ceiling,Lower ceiling,Heights,N/SHEET,Framing,Row / reason`, with Type in {single, double}. It was validated by calling `doble_cielo_fallas(filas, cuartos_rcp(set_texto), niveles_membrana(canon))` and `refs_doble_fallas` (read-only import, `python3 -I -B`): **0 failures**.

| Room | Result | Implication for our scope |
|---|---|---|
| Retail 100 | single: 2x4 ACT 12'-0" | None (ACT by others). The W2 face goes to 12'-6". |
| Storage 101 | single: existing grid + new tiles 10'-0" | None. The SOF-01 storage face (8'-6" to 10'-6") sits beside the ACT, not above or below it. |
| Hallway 102 | single: existing GYP 9'-0" + new SOF-01 header 8'-6" side by side (different areas, step), **not stacked** | SOF-01 is loaded; the existing ceiling is not touched. |
| Toilet 103 | single: existing GYP 9'-0" | None. |
| Access. Toilet 104 | single: existing GYP 9'-0" | None. |
| Landlord (N.I.C.) | single: none | N.I.C. |

**No double ceiling in this set**: 0 stacked ceilings, so the quantity impact is 0. No rated floor or roof assembly gives a membrane. Gate side-finding: `cuartos_rcp` reads 3 false "rooms": `162` and `600` from the SSMA designator legend on A3.0 ("162 X 1/100 INCHES", "600 X 1/100 INCHES", "600S162-54"), and `200D` from the A2.0 hardware schedule ("THRESHOLD 200D"). Without a row for each, CE_DOBLE_CIELO would FAIL, so I added 3 explicit "not a room" rows. This is a gate bug to fix later: room numbers inside SSMA designators and hardware model numbers should be filtered out.

## 3. A0.3 specs vs Material Summary (detail in A0.3_SPECS_vs_MS.md)

- **MISMATCH: 0.** These all MATCH: 5/8" Type X board (MS 13), metal beaded trim (MS 17 / 18), perforated paper tape (MS 33), ready-mixed all-purpose compound (MS 32), and studs / track (A0.3 prints no gauge, so the A2.0 gauges stand; coating is printed nowhere, [PENDING]).
- **NOT IN EXCEL (2, both already disclosed, no change to loaded quantities):**
  - "ALL PURPOSE TEXTURE FINISH" (A0.3 PAINTING, gypsum board treatment) vs Level 4 (A2.0 gen. note 3): Review Items row 7. Conditional delta 483.35 SF on new board = 321.38 + 88 + 29.75 + 29.75 + 14.47 [DERIVED], or 3,072.97 SF with patch areas included.
  - Owens Corning 3-1/2" sound batt (A0.3 THERMAL; A2.0 wall legend "WITH SOUND BATT INSULATION U.N.O." hatch): excluded by estimator standing order (ALC-E03 / ALC-X46). Conditional delta 224.66 SF = 13.973 x 12.5 + 4.00 x 12.5 [DERIVED], only if W2 carries the sound-batt hatch. I did not re-verify the hatch; ALC-E03 says plain hatch.
- Minor: A0.3 says "ASTM A36" for the board. That is a steel standard (typo; the board standard is ASTM C1396) and has no quantity effect. The A2.0 note "USE WATER RESISTANT GYPSUM BOARD ... WHERE TILE IS USED" is worth a look for the PR-W4 patch board in the toilets. That is outside A0.3 and was not re-quantified.

## 4. Detector root causes (tools/chequeos_biblioteca.py)

### CB_RCP_TAGS: "N/A: ninguna hoja de RCP con tags de cielo impresos" (function `rcp_tags`, around line 4328, helper `tags_cielo`, around line 4310)
1. **Main cause: a keyed-tag-only regex.** `tags_cielo` counts only `\b([A-Z]{2,4})-(\d{1,2})\b(?!\s*:)` with a prefix in PREF_CLG (GYP-1, ACT-2, FS-1 ...) or prefixes defined by a "CEILING LEGEND/TYPES" block with "XX-n:" entries. A3.0 uses **descriptive** tags with no hyphen-number code: "2x4 ACT" + "12'-0" AFF", "GYP. BD." + "8'-6" AFF", "EXISTING GYP. BD. 9'-0" AFF". Its legend has no "XX-n:" definitions either. So `tags_cielo(A3.0)` returns `{}`, `imp` stays empty, and the function returns `NA(...)`, which is a PASS done in a vacuum (U-137). On the real `/root/xf/work/set_texto.json` A3.0 text, RX_HOJA_RCP and RX_PLAN_RCP are both True and `tags_cielo` returns `{}`, which confirms it.
2. **Latent second cause:** `RX_HOJA_RCP = r"REFLECTED CEILING|\bRCP\b"` uses a literal space. A title split across lines ("REFLECTED\nCEILING PLAN", which is exactly how pymupdf extracts A3.0's title block) does not match it, so the sheet is skipped before tags are even looked at. On this set it happened to match elsewhere in the text, but a minimal input shows it failing even with a keyed tag. RX_PLAN_RCP already uses `\s+`.
3. Side note: A0.3 matches both RX_HOJA_RCP and RX_PLAN_RCP ("REFER TO REFLECTED CEILING PLAN FOR GRID AND TILE TYPES"), so a spec sheet is classified as an RCP. The negative look-behind covers only "RE: ".

Minimal reproductions (run with `python3 -I -B`, sys.path set to tools/):
```python
import chequeos_biblioteca as CB
t = "A3.0 REFLECTED CEILING PLAN\n2x4 ACT\n12'-0\" AFF\nGYP. BD.\n8'-6\" AFF\nEXISTING\nGYP. BD.\n9'-0\" AFF"
CB.tags_cielo(t)                                             # {}
CB.rcp_tags(CB.B(canon={"misc_items": []}, hojas={"A3.0": t}))   # ('PASS', ['N/A: ninguna hoja de RCP con tags de cielo impresos'])  <- should FAIL (5 tags, no rcp_tags)
t2 = "A3.0 REFLECTED\nCEILING PLAN\nGYP-1"                   # cause 2: keyed tag, title split by newline
CB.rcp_tags(CB.B(canon={"misc_items": []}, hojas={"A3.0": t2}))  # ('PASS', ['N/A: ...'])  <- should FAIL
# control: "A3.0 REFLECTED CEILING PLAN\nGYP-1" -> FAIL "1 tags de gypsum impresos ... el canon no trae rcp_tags" (works)
```
Fix direction (not applied): (a) also count descriptive tags `(?:\d+\s*x\s*\d+\s+ACT|GYP\.?\s*BD\.?|GWB|ACT)` followed within about 2 lines by `\d+'\s*-\s*\d+(?:\s*\d+/\d+)?"\s*AFF`, and count each "... AFF" height as one tag instance; (b) `RX_HOJA_RCP = r"(?i)REFLECTED\s+CEILING|\bRCP\b"`; (c) an RCP sheet with ≥ 1 "AFF" and 0 tags recognized should return AMBER or FAIL, not NA.

### CB_BE_CF10: "el set no trae specs del trade" (function `be_cf10`, around line 2366)
- Spec presence is decided only by `bool(b.specs)` (a Project Manual in entrega.json `specs_dir`) **or** `re.search(r"\b09\s?2[0-9]\s?\d{2}\b|\b05\s?4[0-1]\s?00\b|SECTION 09", set_txt)`. A0.3 is an **outline spec printed on a drawing sheet**, organized by headings ("METALS: LIGHTGAGE FRAMING", "FINISHES: GYPSUM DRYWALL: ... GYPSUM BOARD ... TYPE X 5/8", "JOINT COMPOUND", "TRIM") with **no CSI numbers and no "SECTION 09"**. There is no Project Manual (`b.specs` is empty). The Excel cites "A0.3", not section numbers, so `citadas` is empty too. The result is `NA("el set no trae specs del trade y la entrega no cita ninguna sección")`. On the real set_texto, the regex is False for A0.3 and A3.0.
- Minimal reproduction:
```python
a03 = "SPECIFICATIONS\nMETALS:\nLIGHTGAGE FRAMING: METAL STUDS SHALL BE USED IN WALLS AS SHOWN ON DRAWINGS\nFINISHES: GYPSUM DRYWALL:\nGYPSUM BOARD: ASTM A36, TYPE X 5/8 FIRECODE\nJOINT COMPOUND: ASTM C 475 OF THE TYPE INDICATED."
ms = [{"fila": 13, "material": '5/8" gypsum board, Type X', "unit": "SF", "net": 3072.97, "fuente": "N/SHEET: 2/A2.0, A0.3"}]
CB.be_cf10(CB.B(hojas={"A0.3": a03}, ms=ms))   # ('PASS', ['N/A: el set no trae specs del trade ...'])  <- should evaluate
# control: same + "\nSECTION 09 29 00" -> FAIL "MS fila 13 ... sin sección de spec" (detector engages)
```
- Fix direction (not applied): treat a sheet titled "SPECIFICATIONS" (or a sheet text with ≥ 2 of `GYPSUM BOARD|LIGHTGAGE|METAL STUDS|JOINT COMPOUND|DRYWALL` next to `PRODUCTS|EXECUTION|ASTM`) as "specs present". Then accept citations of the form "A0.3 <HEADING>" (sheet + paragraph heading) as the spec reference for each MS row.

## Bottom line
6 tag assignments (5 printed boxes): 1 CARGADO (SOF-01), 2 EXCLUIDO ACT (ALC-E01), 3 EXCLUIDO EXISTING (ALC-E13 / ALC-11); **0 FALTA**. 0 double ceilings. 0 spec MISMATCH; 2 NOT-IN-EXCEL items are already disclosed and do not change loaded quantities. Two detector bugs are explained above with repros, plus one gate false-positive (`cuartos_rcp`).
