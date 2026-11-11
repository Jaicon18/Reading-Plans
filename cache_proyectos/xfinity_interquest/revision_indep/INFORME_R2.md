# INFORME R2: independent review of the markups PDF and Excel (Xfinity Interquest rev1)

Reviewed:
- `/root/xf/work/etapas/8_excel/XF_markups_rev1 - OPEN IN BLUEBEAM.pdf`
- `/root/xf/work/etapas/8_excel/XF_Takeoff_FINAL_rev1.xlsx`
- canon `/root/xf/work/etapas/4_canon/takeoff_canon.json`
- clean plans `/root/xf/work/plans/bidset_SIN_MARKUPS.pdf`
- images `/root/xf/work/etapas/7_imagenes/*IMAGE ONLY*`

Files produced in `/root/xf/work/revision_indep/R2/`:
- `VISTA_BLUEBEAM.csv`: output of the tool.
- `BLUEBEAM_SIM_INDEP.csv`: my own simulation from /Vertices x /Measure.
- `markups_indep.json`
- `annots_dump.txt`
- `crops/*.png`: 150-300 dpi crops of every markup, plus clean and marked comparisons.

Tool gates: CE_VISTA_BLUEBEAM PASS (18/18 measured markups OK); CE_PDF_EDITABLE PASS. The independent checks below found issues that those gates do not detect.

**Totals: 2 ERROR, 11 MINOR, 1 informational note.**

---

## ERROR

### E1. A1.0: a key-7 dashed wall has no markup and is not in the Excel
- **Where:** A1.0 (page 4), at visible coordinates x 630.24 / 637.56 pt, running from the north demising inner face (y 1244.52) to a closed end (y 1401.72). It sits just east of the dashed display fixtures in the Storage / north-west zone.
- **Why it counts as a wall:**
  - Keynote 7 ("ALL EXISTING INTERIOR WALLS, DOORS, AND WINDOWS AS SHOWN DASHED TO BE REMOVED") points straight at it.
  - It is a dashed double line 7.32 pt thick (= 4.9"). This is exactly the thickness of DEMO-01..09.
- **Quantity:** length 157.2 pt / 18 = **8.73 LF**. At the carried height of 26'-0", that is **227.1 SF** of demolition missing.
- **Where it is missing:**
  - Bluebeam: no markup.
  - Excel: not in Material Summary row 14. That row and Scope ALC-E16 both say "DEMO-01..09".
  - Canon `misc_items` / `demo_geom.json`: not present.
  - No RFI or Review Item mentions it. RFI-03 settles only the L-element (DEMO-08/09) by the same keynote-7 logic.
- **Evidence:**
  - `crops/A1.0_UNMARKED_key7_wall_x630.png`
  - `crops/A1.0_fixtures_key7_unmarked.png`
  - `crops/A1.0_plan_clean.png` vs `crops/A1.0_plan_mk.png`
  - Vector lines measured from the clean PDF: verticals at x 630.24 (217 pt of dashes) and 637.56; end cap at y 1401.72.
- **Fix:** add DEMO-10 (8.73 LF x 26 = 227.1 SF; demolition total 1,651.88 becomes 1,879.0 SF). If it is judged millwork back, add an explicit RFI or exclusion instead.

### E2. W2-01 board does not deduct the net opening of Door 101
- **Where:**
  - Excel Partition Takeoff H6 = 321.38 SF.
  - PDF label "321.38 SF board (faces×layers)".
  - Material Summary row 13 breakdown.
- **What is wrong:** 321.38 = 13.973 x (12.5 + 10.5), the full faces with no deduction. Yet:
  - The markup and the canon measure W2-01 *through* the Door 101 R.O.: 0.333 + 3.000 + 10.640. See `crops/A2.0_W2_mk.png`.
  - Canon `openings`: Door 101, R.O. 3'-0" x head 7.167 ft, in W2-01.
  - Skill rule (SKILL.md "ABERTURA NETA = header − sill … ESO es lo único que se deduce del board", R78.1 `deduct_opening_sf`): the net opening must be deducted on each face.
  - The Excel I13 text itself says "faces: length x face height x layers - openings".
- **Delta:**
  - 3.0 x 7.167 = 21.50 SF per face, x 2 faces = **-43.0 SF**.
  - W2-01 board 321.38 becomes 278.38. Board total 483.35 becomes 440.35 SF. Purchase 11 sheets becomes 10.
  - Joint compound 34.8 lb becomes 31.7 lb; tape 178.84 LF becomes 162.93 LF.
  - The SF in the W2-01 PDF label must be updated too.

---

## MINOR

### M1. DEMO Wall Area in Bluebeam differs from the Excel by 0.01 SF in four rows
| Element | Bluebeam (Length x Depth) | Excel / label |
|---|---|---|
| DEMO-03 | 62.75 | 62.74 |
| DEMO-05 | 146.81 | 146.82 |
| DEMO-07 | 77.65 | 77.66 |
| DEMO-09 | 188.93 | 188.94 |
| **Subject total DEMO** | **1,651.86** | **1,651.88** |

- **Cause:** the canon rounds LF to 3 decimals before multiplying by 26. Example: 2.413 x 26 = 62.738, but the vertices give 43.44 pt = 2.41333 ft, and x 26 = 62.747.
- **Fix:** compute SF from unrounded LF, or round the vertices.
- **Evidence:** `BLUEBEAM_SIM_INDEP.csv`.

### M2. Legends are incomplete
- A1.0 has **no TAKE-OFF LEGEND box** in the PDF (A2.0 and A3.0 have one). See `crops/full_A1.0.png`.
- The A3.0 legend has **no EXCLUDED entry**, which U-160 requires. Its line "…14.47 SF" also runs past the right border of the box. See `crops/A3.0_legendbox.png`.
- The LEGEND page (p.18) lists only W2 and CF. DEMO, the SOF-01 board and EXCLUDED are missing. See `crops/full_LEGEND.png`.

### M3. A2.0 legend is drawn sideways
The A2.0 TAKE-OFF LEGEND box is rotated 90° in the visible view and reads bottom-to-top. See `crops/A2.0_legend_mk.png`.

### M4. EXCLUDED polygons have no hatch
The six EXCLUDED polygons are a grey translucent fill (IC .45, CA .25) with a dashed outline. Their appearance stream has no hatch pattern, but U-160 / the brief ask for a "grey hatched polygon". They have no /Measure (OK).

### M5. FreeText placement is legible but crowded in places
All six texts are 95.8-99.7 % inside their room and have no /CL. However:
- The Landlord text runs onto the wall on its right ("not in" over the jamb).
- The Toilet 104 text sits over three ceiling devices.
- The Storage text overlaps a 2x4 fixture symbol.

See `crops/A3.0_zone_toilets.png` and `crops/A3.0_rcp_overview.png`.

### M6. Inherited annotations show up as blank rows in the Markups List
The PDF carries 1,589 inherited "AutoCAD SHX Text" Square annotations on E0.0-P1.0, with no Subject and no /Measure. They come from the clean bid set. In Bluebeam they will appear as 1,589 blank-Subject rows in the Markups List. Quantities are not affected.

### M7. Spanish text in the Excel
Inputs B66 = "reviewed - no existe en el set (not in the set)". Spanish is not allowed.

### M8. W2-01 location text contradicts its length
Partition Takeoff A6/I6 says W2-01 runs "from door 101 south jamb to existing W4 post". The length (13.973) and the markup start at the north demising wall *through* the door. The description should say so.

### M9. Some Material Summary rows do not cite a real sheet
- Rows 32 and 33 (compound, tape): "N/SHEET: driver = …" with no sheet named.
- Row 28: "N/SHEET: GA-216", which is not a sheet of the set.

### M10. Scope Checklist and Partition Takeoff structure
- The Scope Checklist mixes in RFI rows (RFI-02..RFI-05, rows 42-45).
- ALC-X45 duplicates ALC-E03 (insulation).
- The Partition Takeoff column "Layers" shows 2 for W2, but each face is 1 layer (the 2 = faces). The header is ambiguous.

### M11. Placement problems in the delivered images
- **A3.0 image:**
  - The box label "EXISTING TOILET 103: EXCLUDED" sits inside **Storage 101**, above the toilet block.
  - "LANDLORD ROOM: EXCLUDED" straddles the exterior wall and the image edge of the room.
  - "STORAGE 101: EXCLUDED" and "RETAIL 100: EXCLUDED" cover the printed room tags.
  - "HALLWAY 102: EXCLUDED" runs into Retail.
  - See `crops/img_A3.0_zoom.png`.
- **A2.0 image:** the title / legend banner covers the DOOR SCHEDULE header. See `crops/img_A2.0.png`.

Names follow U-158 and the Wall IDs match the Excel, so only placement is at issue.

---

## Note (informational)
- **SOF-01 depth:** the markup Depth is 3.407 ft, while the label says 3'-4.875" (3.40625). The Wall Area is the same, 14.47 SF.
- **Misc rows without markups:** SOF-01 studs and track, the Door 101 header, braces, blocking on existing walls, corner bead and L bead have no markups. Only the SOF-01 board strip is marked. This is acceptable for misc rows, but the estimator cannot see them in Bluebeam.

---

## Checks that passed (evidence)

**1. Bluebeam Markups List simulation.** All 18 measured markups match the label text and the Excel (except M1):
- Page Label = printed sheet number; the label is found in the title block at (2807, 2030) on every page.
- Length = /Vertices x /X C 0.055555557; DepthUnit /C 1.
- W2-01 13.97 LF x 12.5 = 174.66 SF; W2-02 4.00 x 12.5 = 50.00.
- CF-01 / CF-02: 0.72 + 0.72 + 0.94 = 2.38 LF each; board 29.75 = Excel H10 / H11.
- SOF-01 board 4.247 x 3.407 = 14.47 = MS row 13.
- DEMO-01..09 = MS row 14.

**2. PDF integrity.**
- 1,621 /NM, all unique, none with '/' or '\'.
- No AcroForm, /SigFlags, /Perms, signature widgets or encryption.
- 18 Page Labels, all unique (A0.1…P1.0, LEGEND).
- /VP on A1.0, A2.0 and A3.0, each with R "1/4 in = 1 ft", BBox covering the full page, and the same /R as its markups. The LEGEND page has no /Measure markups (OK).

**3. RCP A3.0.** Every printed room has an EXCLUDED polygon and red FreeText "EXCLUDED - <reason> (A3.0)" with Subject EXCLUDED:
- Retail 100 and Storage 101: ACT by others.
- Hallway 102, Toilet 103 and Access Toilet 104: existing gyp. bd. 9'-0" to remain.
- Landlord N.I.C.

The SOF-01 8'-6" strip has its markup, sitting exactly on the unstippled strip between the two 0.48 pt lines. See `crops/A3.0_SOF01_mk.png` vs `_clean.png`.

**4. Markups sit on their drawn elements.**
- W2-01 and W2-02 are on the hatched W2 line. See `crops/A2.0_W2_mk.png`.
- CF-01 and CF-02 have 3 sides each, open on the pier side. See `crops/A2.0_CF01_mk.png` and `crops/A2.0_CF02_mk.png`.
- DEMO-01..09 follow the dashed walls. See `crops/A1.0_plan_mk.png` and the per-markup crops.
- The one exception is the missing wall in E1.

**5. Excel.**
- Opens with openpyxl and has exactly the 6 required sheets.
- No #REF!, #VALUE! or #DIV/0!; all formulas have cached values.
- No dollar amounts or currency formats.
- Partitions in schedule order (W2, then CF) with a SUBTOTAL per type and a GRAND TOTAL (22.733 LF / 468.88 SF).
- Spanish text only in B66 (M7). N/SHEET exceptions are listed in M9.

**6. Images.**
- Names are correct per U-158: "A1.0 - IMAGE ONLY (not editable) - walls rev1.png", "A2.0 … walls rev1.png", "A3.0 … ceilings rev1.png".
- Labels match the Excel IDs: DEMO-01..09 with their SF; W2-01 13.97, W2-02 4.00, CF-01 / CF-02 2.38; SOF-01-BOARD 4.25 LF / 14.47 SF.
