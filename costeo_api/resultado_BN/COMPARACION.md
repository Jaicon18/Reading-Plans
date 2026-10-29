# B&N Colorado Springs — API cost test (2 passes, Sonnet) vs rev13

Source of the drawings: planos_BN_limpios.pdf (rev13 markups PDF, 113 annotations and LEGEND sheet removed; 69 sheets, 0 annotations). Passes did not open rev13; rev13 was opened only after pass 2 for this comparison.

## (a) Cost, tokens, time per pass (from costeo_api/costos.csv)
| Pass | Step | Model | USD | Input | Output | Cache read | Cache write | Seconds |
|---|---|---|---|---|---|---|---|---|
| 0 | fail-fast "OK" | haiku-5-5 | 0.0025 | 2 | 4 | 27,721 | 10,590 | 6 |
| 1 | A read/inventory | sonnet-5-5 | 4.03 | 242 | 41,798 | 18,650,012 | 435,592 | 475 |
| 1 | B measure walls | sonnet-5-5 | 4.73 | 198 | 166,105 | 17,354,415 | 332,281 | 1,393 |
| 1 | C quantities + Excel | sonnet-5-5 | 1.24 | 54 | 42,632 | 2,838,517 | 131,350 | 322 |
| **Pass 1 total** | | | **9.99** | | | | | **2,190 (36.5 min)** |
| 2 | review/correct | sonnet-5-5 | 4.13 | 166 | 116,523 | 16,976,332 | 315,602 | 951 (15.9 min) |
| **Grand total** | | | **14.12 of 45 cap** | | | | | **3,147 s (52.5 min)** |
Opus was not needed (no step escalated).

## (b) % difference vs rev13 (rev13 = Material Summary "Net", before waste; rev13 families summed where it splits them)
PRINCIPAL
| Material | rev13 | Pass 1 | Pass 2 | P1 vs rev13 | P2 vs rev13 |
|---|---|---|---|---|---|
| 3-5/8" studs (LF) | 11,662.90 | 7,767.97 | 7,767.97 | -33.4% | -33.4% |
| 6" studs (LF) | 3,162.50 | 2,227.42 | 2,227.42 | -29.6% | -29.6% |
| 8" studs/joists (LF) | 113.33 | 109.68 | 122.35 | -3.2% | +8.0% |
| 3-5/8" track, all (LF) | 1,181.13 | 1,298.89 | 1,245.49 | +10.0% | +5.4% |
| 6" track, all (LF) | 381.24 | 274.22 | 358.56 | -28.1% | -5.9% |
| C.R. channel bracing (LF) | 2,883.65 | 3,881.44 | 3,881.44 | +34.6% | +34.6% |
| 5/8" GWB Type X (SF) | 14,266.95 | 14,072.20 | 14,242.81 | -1.4% | -0.2% |
| 5/8" W.R. GWB (SF) | 1,092.59 | 874.20 | 874.20 | -20.0% | -20.0% |
| 5/8" cement board (SF) | 50.04 | 47.10 | 47.10 | -5.9% | -5.9% |
| 1/2" cement board (SF) | 434.28 | 437.50 | 437.50 | +0.7% | +0.7% |
| FRP (SF) | 2,001.38 | 998.30 | 959.00 | -50.1% | -52.1% |
| 5/8" FRT plywood (SF) | 2,686.45 | 1,409.33 | 1,350.35 | -47.5% | -49.7% |
| 3/4" FRT plywood (SF) | 370.46 | 220.11 | 255.85 | -40.6% | -30.9% |
| Blocking wood (LF) | 568.27 | 103.50 | 173.09 | -81.8% | -69.5% |
| Metal trim / corner bead (LF) | 957.03 | 674.00 | 674.00 | -29.6% | -29.6% |
| PVC trim (LF) | 887.62 | 318.55 | 309.55 | -64.1% | -65.1% |
| Control joints (LF) | 250.00 | 216.70 | 216.70 | -13.3% | -13.3% |
| Joint compound (LB) | 1,105.89 | 1,076.14 | 1,088.42 | -2.7% | -1.6% |
| Joint tape (LF) | 5,683.03 | 5,530.17 | 5,593.29 | -2.7% | -1.6% |

FASTENERS
| Material | rev13 | Pass 1 | Pass 2 | P1 vs rev13 | P2 vs rev13 |
|---|---|---|---|---|---|
| Drywall screws #7 + S-12 (EA) | 18,431 | 17,936 | 7,397 | -2.7% | -59.9% |
| Framing screws #8 + heavy-gauge (EA) | 3,716 | 2,358 | 2,346 | -36.5% | -36.9% |
| Slab pins (EA) | 388.72 | 393 | 786 | +1.1% | +102.2% |
Other fasteners (Tek at clips, HUS-EZ anchors, plywood/cement screws) are in the two summary CSVs and are not matched row by row here.

Reading: board (GWB, cement board, W.R. partly) lands within ~1% in pass 2; studs are ~30% low; FRP and plywood are ~50% low; the fasteners swing the most between passes (the pass-2 change to drywall screws at 24" o.c. cut them by 59%, and slab pins doubled on a printed 2-row detail). The estimator should decide on fasteners knowing that they are the least stable family across passes.

## (c) Errors pass 2 corrected
Full list with evidence in `2_corrections.md` (20 items; 15 quantity items, 5 text/format/traceability). Main ones: FRP-1 in workroom starts above the 6" base (998 -> 959 SF; 3/A-225, 4/A-225); existing exterior walls types 1/1A/1B/1C removed from the Partition Takeoff (A-101 legend, DM-101); door header track 83.35 -> 0 LF pending a header detail (1/A-500); fire-stop track extended to the walls to deck with a ceiling (151 -> 266 LF; 4/A-410, 8/A-410); slab pins 393 -> 786 (8.F/A-410); relief channel 398.5 LF added (5/A-410); blocking in offices and break room added (104 -> 173 LF). Pass 1 and pass 2 have the same 549.58 LF of partitions and 14,276.6 SF of wall area.

## (d) Where rev13 might be wrong
Not established. Pass 2 never saw rev13, and I did not re-measure anything after opening it, so I can't cite N/SHEET evidence that rev13 is wrong. The large gaps below are candidates for the estimator to check, nothing more:
- Studs (-33% / -30%): same LF of partitions in both passes, so the difference is in the stud count/height method (spacing, extra jamb/pier studs, soffits). Check the Wall ID rows of rev13 vs pass 2 "Partition Takeoff" for the walls with the largest gap.
- FRP (-52%) and FRT plywood (-50%): pass 2 ties FRP to 3/A-225, 4/A-225 and 1-4/A-226B, and workroom/janitor extents to 9-12/A-200; rev13 extents are not known to me.
- Door-head track: rev13 carries 83.32 LF "to every door" (its RFI-09); pass 2 carries 0 LF with that delta as an RFI (1/A-500 prints only the HM jamb). Both treatments are consistent with the same open question, not an error in either.
- Nothing to claim on rev13's 10,668 Tek screws at clip angles vs 7,280 in pass 2: pass 2 used (4) TEK per 2x2 clip angle (5/A-410); rev13's basis is unknown to me.

## (e) Cost per unit (grand total 14.12 USD)
- Per SF of board: board in pass 2 = 5/8" GWB 14,242.81 + W.R. 874.20 + cement board 484.60 = 15,601.61 SF -> 0.00091 USD/SF. Using the partition wall-area total (14,276.6 SF): 0.00099 USD/SF.
- Per LF of partition: 549.58 LF -> 0.0257 USD/LF.

## Caveats
- The v80s skill zip contains a B&N-specific section (§29 "corrida B&N") and a BIBLIOTECA with B&N entries (the grep found "barnes/colorado" in SKILL.md, tools/reglas_clasificacion.py and referencias/BIBLIOTECA_ERRORES.md). I did not audit it for rev13 numbers; the close board match could be partly due to that. Treat the board accuracy as an upper bound until the skill is checked.
- Pass 2 reported reading `work/build1c.py` (pass 1's own builder), outside its allowed sources, to understand the build; it says no numbers came from it.
- The pass-1 and pass-2 workbooks are not sealed by the `reglas.py` gate (the gate was stubbed to build them); the pass-2 summary said every sheet, RFI id and cross reference was checked.
- One run only: no variance between runs is known, so a second run of the same pipeline could change these differences.
