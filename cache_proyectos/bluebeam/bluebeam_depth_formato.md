# Bluebeam Revu — how Depth and Wall Area / Area are stored in the PDF

Scope: **format only**. Reference file in quarantine (BOA Broomfield, Mariale markups), page label **A04.01** (page index 28).
Take-off quantities are redacted as `<value>`. The only numbers kept are the 3 Depth values and the unit factors.
Read with PyMuPDF `doc.xref_object(xref, compressed=False)`. Revu writes `xfa:APIVersion="BluebeamPDFRevu:2018"`.

## 1. Summary of keys

| What | Where | Stored or computed? |
|---|---|---|
| Depth (value) | `/Depth <number>` on the annot dict itself | **Stored**. A plain number in the unit of `/DepthUnit`. No `/Depth` key when depth is not set (e.g. 7 of 8 Polygons, 18 PolyLines in this file). |
| Depth (unit) | `/DepthUnit [ << /Type /NumberFormat /U (...) /C ... /D 100 /FD true /SS () >> ]` on the annot dict | **Stored**. Always a 1-element array. |
| Markup type | `/IT /PolyLineDimension` (Polylength) · `/IT /PolygonDimension` (Area) | Stored |
| Measurement kind | `/MeasurementTypes 130` (PolyLine/length) · `129` (Polygon/area) | Stored (bitmask; 128 + 2 = length, 128 + 1 = area — [DERIVADO] from the values seen) |
| Scale + units | `/Measure n 0 R` → `/Type /Measure /Subtype /RL /R (0.25 in = 1 ft)` with `/X /D /A /T /V` NumberFormat arrays + `/TargetUnitConversion` | Stored. Same shared object (xref 4283) for every markup on the sheet. |
| Length / Area result | Only as **text**: 2nd `<p>` of `/RC`, after `\r` in `/Contents`, and in the `/AP /N` stream (`(<value> ft) Tj` / `(<value> sf) Tj`) | **Text only. No numeric key.** Revu recomputes from `/Vertices` + `/Measure`. |
| **Wall Area** (PolyLine × Depth) | — | **Not stored anywhere.** No `/WallArea` key, nothing in `/RC`, `/Contents` or `/AP`. Revu computes it (length × Depth) for its Markups List / Properties. |
| Volume (Polygon × Depth) | — | **Not stored.** Only the unit exists: `/Measure /V [ /U (cu ft) ]`. |
| `/BS*`, `/BSI*` keys | none on these markups | `/BSIColumnData [ () () () ]` exists only on 4 `QUESTION` PolygonCloud markups in the file (empty custom columns). Not related to depth. |
| Other measure keys | `/RiseDrop 0` (PolyLine), `/SlopeType 0\|1` + `/PitchRun 12` (Polygon), `/Segments false`, `/Cap true`, `/AlignOnSegment true` | Stored |

## 2. `/DepthUnit` variants seen in the whole file

`/C` = factor from **unscaled PDF points** to the unit (it's not the drawing scale):

| `/U` | `/C` | Check | Meaning |
|---|---|---|---|
| `(in)` | `.01388889` | 1/72 = pt → in | inches |
| `(ft)` | `.001157407` | 1/864 = 1/(72·12) = pt → ft | decimal feet |
| `(')` | `.001157407` | same as ft | **feet-inches** (Revu unit `ft' in"`) |
| `(mm)` | `.3527778` | 25.4/72 = pt → mm | millimetres |

Counts: PolyLine `(')` 61 with Depth · `(ft)` 9 with Depth + 3 without · `(mm)` 15 without · `(in)` 1 with Depth. Polygon `(ft)` 1 with Depth + 7 without.

### `1.5 ft' in"` vs `6 in`
- `6 in` → `/Depth 6` + `/DepthUnit [ << /U (in) /C .01388889 ... >> ]`. The value is in inches.
- `1.5 ft' in"` → `/Depth 1.5` + `/DepthUnit [ << /U (') /C .001157407 ... >> ]`. **The value is always stored in decimal feet** (1.5 = 1'-6"). The `(')` label only tells Revu to *show* it as feet-inches. The display string is not stored in the PDF.
- Decimal feet → `/Depth 15.5` + `/U (ft)`.
- [PENDIENTE] exactly how the Revu UI renders `(')` (e.g. `1'-6"`). It is not in the PDF; we would have to check it in Revu itself.

To write: `/Depth` = number in the chosen unit; `/DepthUnit` = 1 NumberFormat with `/U` and `/C` from the table above, `/D 100 /FD true /SS ()`.

## 3. Raw examples (trimmed; `/Vertices` and quantities redacted)

### A. PolyLine, depth in inches — xref 4152
```
/Subj (CEILING TRANSITION 3 5/8" METAL STUD BRACING 48" OC. 3 5/8" METAL STUD AND TRACK 16"OC. 5/8 GYPSUM BOARD)
/Type /Annot  /Subtype /PolyLine  /F 4  /C [ 1 0 0 ]  /IC [ 1 0 0 ]
/T (Mariale)
/Measure 4283 0 R
/RiseDrop 0
/DS (font: Helvetica 12pt; text-align:center; line-height:13.8pt; color:#FF0000)
/Cap true  /AlignOnSegment true  /Segments false
/MeasurementTypes 130
/IT /PolyLineDimension
/DepthUnit [ << /Type /NumberFormat /U (in) /C .01388889 /D 100 /FD true /SS () >> ]
/Depth 6
/AP << /N 4160 0 R >>          % stream draws "(<value> ft) Tj"
/Vertices [ ... ]
/RC (<?xml version="1.0"?><body xmlns:xfa="http://www.xfa.org/schema/xfa-data/1.0/" xfa:contentType="text/html" xfa:APIVersion="BluebeamPDFRevu:2018" xfa:spec="2.2.0" style="font:Helvetica 12pt; text-align:center; line-height:13.8pt; color:#FF0000" xmlns="http://www.w3.org/1999/xhtml"><p>CEILING TRANSITION ... 5/8 GYPSUM BOARD</p><p><value> ft</p></body>)
/Label (CEILING TRANSITION ... 5/8 GYPSUM BOARD)
/Contents <FEFF ... >          % UTF-16BE: "<Subj>\r<value> ft"
/NM (OSDWNVFLDYKAFPYY)
```

### B. PolyLine, depth in feet-inches — xref 4194
```
/Subj (CEILING TRANSITION 3 5/8" METAL STUD BRACING 48" OC. 3 5/8" METAL STUD AND TRACK 16"OC. 5/8 GYPSUM BOARD)
/Subtype /PolyLine
/Measure 4283 0 R
/RiseDrop 0
/MeasurementTypes 130
/IT /PolyLineDimension
/Depth 1.5
/DepthUnit [ << /Type /NumberFormat /U (') /C .001157407 /D 100 /FD true /SS () >> ]
/AP << /N 4197 0 R >>
/RC (... <p>CEILING TRANSITION ...</p><p><value> ft</p></body>)
/Contents <FEFF ... >          % "<Subj>\r<value> ft"
/NM (ZBRKVYKYOTDIAZPG)
```

### C. Polygon (Area Measurement) with depth — xref 4266
```
/Subj (Area Measurement)
/Type /Annot  /Subtype /Polygon  /F 4  /C [ 1 0 0 ]  /FillOpacity 1
/T (jesra)
/Depth 15.5
/Cap true  /AlignOnSegment true
/MeasurementTypes 129
/SlopeType 0
/PitchRun 12
/IT /PolygonDimension
/DepthUnit [ << /Type /NumberFormat /U (ft) /C .001157407 /D 100 /FD true /SS () >> ]
/AP << /N 4268 0 R >>          % stream draws "(xxxxx) Tj" "(<value> sf) Tj"
/Vertices [ ... ]
/RC (... <p>xxxxx</p><p><value> sf</p></body>)
/Measure 4283 0 R
/Label (xxxxx)
/Contents <FEFF ... >          % "xxxxx\r<value> sf"
/NM (JRQCKOYWYXGJUEBT)
```
Polygon without depth (e.g. `RCP 5/8" GYPSUM BOARD`, xref 4165) keeps `/DepthUnit [ << /U (ft) ... >> ]` but has **no `/Depth`**; it also has `/SlopeType 1`, `/FillOpacity .2`, `/CA 0`.

### Shared `/Measure` — xref 4283
```
<< /Type /Measure /Subtype /RL /R (0.25 in = 1 ft)
   /X [ << /Type /NumberFormat /U (ft) /C .05555556 /D 100 /SS () >> ]      % pt → ft at 1/4"=1'-0" (4/72)
   /D [ << /Type /NumberFormat /U (ft) /C 1 /D 100 /SS () >> ]
   /A [ << /Type /NumberFormat /U (sf) /C 1 /D 100 /FD true /SS () >> ]
   /T [ << /Type /NumberFormat /U <B0> /C 1 /D 100 /FD true /PS () /SS () >> ]   % degrees
   /V [ << /Type /NumberFormat /U (cu ft) /C 1 /D 100 /FD true /SS () >> ]
   /TargetUnitConversion .001157407 >>
```

## 4. Rules for our markup tool
1. Write `/Depth` (number) + `/DepthUnit` (1 NumberFormat) directly on the annot. Leave `/Depth` out when there's no depth.
2. For feet-inches use `/U (')` with the value in **decimal feet**.
3. Do **not** write Wall Area / Volume: Revu computes them. Length/Area go only as text in `/RC`, `/Contents` (`label\rvalue unit`) and `/AP`.
4. `/IT /PolyLineDimension` + `/MeasurementTypes 130` for Polylength; `/IT /PolygonDimension` + `/MeasurementTypes 129` for Area.
