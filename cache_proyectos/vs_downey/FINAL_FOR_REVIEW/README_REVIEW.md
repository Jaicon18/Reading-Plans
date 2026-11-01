# README REVIEW — Victoria's Secret #679 Stonewood Center, 251 Stonewood St, Downey CA 90241

GC: Elite Retail Services (plan room project 525901). Bid due 11/02/2026 3:00 PM CT. Scope: cold-formed metal framing + gypsum board ONLY (wood, insulation, ACT, MEP, demolition, fasteners EXCLUDED).

## Files
| File | What |
|---|---|
| Take-off/VS679_Downey_Takeoff_FINAL_rev1.xlsx | Fixed 6-sheet Excel: Inputs, Partition Takeoff (schedule order STD, FUR, COL, INS, RFID, SF + subtotals), Material Summary (net / waste / purchase, N/SHEET per row), Pending Items (25 RFIs A/B/C), Review Items, Scope Checklist (ALC-01..27) |
| Planos marcados/A02.01_type_*.png | Marked plan per type (one type per image, every wall with id + LF) |
| Drive only: VS679_Downey_Markups_Bluebeam_rev1.pdf (178 MB) | Bluebeam markups, 112 annotations (Subject = type, Page Label, Length, Depth = wall height, Wall Area); not in git by size |
| RFI_PENDIENTES.md | 25 open RFIs with assumption carried and options A/B/C + delta; 2 closed by the drawings |
| PARA_REVISAR_EN_LA_MANANA.md | Decisions that move quantity, corrections, pending review |
| SEGUIMIENTO.md | Timeline of the run |
| proceso/ | final canon, A/B notes, resolution + correction, gap closure, coverage step 12, process log, sheet map, runner result, markups.json |

## Totals (Material Summary, NET before waste)
| Material | Unit | Net |
|---|---|---|
| 3-5/8" metal stud (all gauges) | LF | 13,491.52 |
| 1-5/8" stud (column wraps) + framed soffits 3-5/8" (F/A10.05, B/A10.03) | LF | 496.50 + 256.92 |
| 6" / 8" / 2-1/2" stud | LF | 123.09 / 56.79 / 16.00 |
| Bottom track (3-5/8" 787.04, 6" 5.56, 1-5/8" 16.86, other 52.70) | LF | 862.16 |
| Top track STANDARD (3-5/8" 741.99, 6" 5.56, 1-5/8" 16.86, other 52.70) | LF | 817.11 |
| DEFLECTION deep-leg slotted slip track 18 ga (INS walls, L/S03.01) | LF | 45.05 |
| Storefront structural framing (S02.01 box beams / posts / head boxes) | LF | 808.87 |
| Door headers (metal stud box beam) | LF | 222.12 |
| Metal stud blocking (wall-mounted items) + edge blocking | LF | 1,468.30 + 38.80 |
| Bracing C.R. channel @ 48" | LF | 1,706.76 |
| 5/8" gypsum board Type X | SF | 18,093.85 |
| 5/8" gypsum board regular (RFID non-sales side, RFI-05) | SF | 545.60 |
| 1/2" moisture resistant gyp at storefront (sheathing row) | SF | 424.00 |
| Cement board (B-13 base strip) / FRP WC-1 | SF | 29.13 / 665.28 |
| Drywall suspension grid: main tee / cross tee / moldings | LF | 2,298.32 / 3,439.49 / 1,223.01 ea |
| Hanger wire 12 ga | LF / PCS | 4,256.39 / 713 |
| Clips (bracing, bridging R/S03.01) | PCS | 1,289 |
| Corner bead + trims / metal reveal / metal FRP trim | LF | 305.11 / 86.27 / 380.64 |
| Joint compound / tape (Level 4, A15.04) | LB / LF | 1,342.04 / 6,896.60 |

Walls by type (LF): STD 83 walls 441.79 · FUR 8 / 211.00 · COL 4 wraps 16.87 · INS 8 / 45.05 · RFID 4 / 59.81 · SF 2 walls 9.64 + 2 piers 25.29 · soffit sides: cashwrap 15.12, beauty valances 6 / 70.50.

## Rules applied
Board not reduced for openings · two track families (standard vs deflection at walls to structure) · printed = carried, RFI only for what is not printed · board heights from dimensions whose ends are board edges · never scaled (lengths from vector geometry are DERIVED with their operation; outlined text) · fasteners EXCLUDED · wood EXCLUDED (incl. RTU support S05.01) · nothing sent to the GC.

## Process
Skill v80v copy + R80e.98-108 (fixed in this run; suite 5/5 OK). Readings A and B independent, comparar.py, directed resolution, orchestrator corrections (A01.01 heights, Type X ceilings), coverage step 12 + gap pass, runner --sin-api 11/11 (reglas.py: only back-check pending). Back-check (step 11) NOT run.
