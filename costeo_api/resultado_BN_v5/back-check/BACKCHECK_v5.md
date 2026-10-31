# Back-check — B&N Colorado Springs, runner take-off v5 (2026-10-31)

## Header
- **Project:** Barnes & Noble, Colorado Springs. Bid set `bidset_SIN_MARKUPS.pdf`, 69 pages, clean (no markups). The same set was used by the runner v5 and by rev13.
- **Scope reviewed:** the five largest differences of the v5 Excel against rev13:
  - column wraps;
  - 6" stud;
  - metal trim;
  - type 2 LF;
  - Type X W.R.
- **⚠️ QUARANTINE: CONTAMINATED.** This back-check ran in the same session that produced the runner take-off, and it knows rev13. Per the back-check protocol (PASO 0), it is valid **only as a method / arithmetic audit and as a plan check of the focus discrepancies**, not as a blind scope verification. A clean back-check must run in a new chat with only the bid set.
- **Sources:**
  - #2 runner v5 (Claude, API);
  - rev13 (Claude take-off with the estimator's decisions; not an independent Bluebeam source);
  - no Bluebeam source (#1) is available.
  - Per the anti-majority rule, agreement between v5 and rev13 is **not** verification. Every finding below rests on a printed note or dimension on the plan.

## Findings (by severity)

| # | Wall / item | Sheet | Class | Against | v5 | rev13 | Plan reading | Delta | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Column wraps (9 columns) | A-101 | OMISSION — CRITICAL | runner v5 | 0 wraps | 9 wraps, 72 LF | Key note **C25** at all 9 columns: "EX. COLUMN. NEW 24"x24" GWB SURROUND OVER 3 5/8" METAL FRAMING FROM SLAB TO 8'-0" AFF" [CONFIRMADO, A-101 C25]. Reading A cited C23 ("existing column to remain exposed"), but C23 is not the note tagged at these columns. | +72 LF of wrap [DERIVADO: 9 × 4 faces × 2'-0"]; board +576 SF [DERIVADO: 72 × 8'-0"]; corner bead +288 LF [DERIVADO: 9 × 4 corners × 8'-0"] | `cols_mosaic.png` (all 9 C25 leaders verified on reopen), `A101_kn.png` |
| 2 | W2-04 extension, x 1011 → 1281 pt | A-101 / A-221 | DIMENSION (double count) — MAJOR | runner v5 | W2-04 86.74 ft (type 2) | W2-04 56.76 ft + C-H1-N 29.98 ft (H1, A-221) | The extra 30.0 ft [DERIVADO: (1281 − 1011) / 9 pt/ft] is the Cafe Workroom 104 north wall. It is counted again on the enlarged plan A-221 as C-H1-N (type H1), so v5 carries it twice and under two types. | −30.0 LF of type 2 [DERIVADO] | `W2-04_extension.png` (red = v5 extension, green = rev13 end; reopened) |
| 3 | Restroom / Cafe faces to deck | A-101, A-121 | METHOD — MAJOR | runner v5 | 11 faces at 25.0 ft (e.g. W2-06.1, W2-07, W5-01 in the restrooms) | 9.0 ft | A-121: restrooms have a GWB ceiling at 9'-0". The board of a face goes to the ceiling of the room that face looks into; the deck height (25'-0", 1/A-400B) is the stud height. | W.R. restroom faces 1028.9 SF in v5 vs 445.9 SF [DERIVADO from board_out] | `A121_restrooms_GWB_9-0.png` (rev13 evidence image; the hatch and GWB 9'-0" are printed on A-121) |
| 4 | Metal trim | — | OMISSION (partial) — MAJOR | runner v5 | 42 LF | 957.03 LF | Not re-quantified blind (contaminated). At minimum, the C25 wraps alone carry 288 LF of corner bead [DERIVADO, #1]. The rest stays [PENDIENTE] for a clean back-check. | ≥ +288 LF | — |
| 5 | 6" stud −46 % | A-221 | OPEN DISCREPANCY | — | 1700 LF | 3162.5 LF | Not caused by #1: the C25 wraps are 3-5/8". Candidates: H2A (4.53 vs 12.17 ft) and E1 (22.3 vs 27.88 ft) lengths on A-221, and soffit sides. Needs the A-221 dimension strings closed (cierre dimensional) in a clean back-check. | — | — |
| 6 | Fasteners at −100 % (Tek screws, clip angles, plywood screws, relief channel, P.A.F., 16 ga wire) | — | METHOD (pipeline) — MINOR for the plan | runner v5 | 0 | per rev13 | These are estimator decisions (misc_items) tied to walls that did not reconcile. They are listed as "sin objeto". This is not a plan difference. | — | — |

## Arithmetic / method audit (tools)
- canon.py, inventario.py, planmark, the reglas.py gate inside the Excel build, alcances and registro: **all pass**. reglas.py after the build leaves 1 failure, the back-check annotation itself.
- Waste is in separate cells (Inputs). Formulas are live (`plantilla_excel.py`).
- **Cobertura (reduced step 12):** 51 / 58 items (87.93 %). The 7 gaps are A-001 general notes 2, 6, 8, 9, 20 and 25 (two items); see `../cobertura.md`.

## Dimensional closure
Not performed in this contaminated pass. The chains on A-221 (H2A, E1) are the first to close in the clean back-check.

## RFIs
None new. The column-wrap note C25 is printed, so no RFI is needed for finding #1.

## Rules created from these findings (same turn)
- **R80e.47 — One wall, once:** a wall drawn on the general plan and on an enlarged plan is counted once, on the enlarged plan with its tag (finding #2). It is now in the reading prompt. An automatic gate needs sheet-to-sheet registration (as mep.py does) and stays as an open item.
- **R80e.48 — Height per face:** a face whose room has a ceiling cannot go above that ceiling + 1 ft unless its detail says full height (finding #3). The runner checks this after the decisions and sends violations to the correction step. It detects 11 faces in v5 and 0 in rev13.
- **R80e.46** (from the run) already makes A/B compare the none-reasons and misc_items, which would have surfaced finding #1.

## Corrected Excel
Not produced. The back-check is contaminated, so the corrections must come from a clean re-run with R80e.46 to R80e.48 active, not from hand edits (R76.7 / R80e.37).
