# RESOLUTION BRIEF (step 5, A vs B) — CR City Hotel, floor {PISO}

You resolve every difference between reading A and reading B of floor {PISO}. You did NOT do either reading.
Never average and never pick a reading silently: every decision cites N/SHEET + a red-circled crop you re-opened.
A printed dimension that matches one reading wins over the other (CONFIRMADO > DERIVADO, U-017).

Inputs
- PDF /root/cr/work/plans/bidset_SIN_MARKUPS.pdf (python3 -I -W ignore, import fitz). Page map in /root/cr/work/BRIEF_LECTURA.md.
- Readings: /root/cr/work/etapas/2_lectura/A/{PISO}.json and /root/cr/work/etapas/2_lectura/B/{PISO}.json (crops listed inside).
- Program comparison: /root/cr/work/etapas/3_revision/comparacion_AB.json → key "{PISO}": pares (A id, B id, dif),
  solo_A, solo_B. NOTE: some bands are transposed in the readings (c0/c1 = extent): the narrow span is the faces.
- Types: /root/cr/work/indep/fichas.json (A0.06 / A0.07 / A0.08 rows, layers per face per rating).

Fixed rules (from the printed set; apply, cite, do not re-ask)
R1 FW.x tags printed without a rating digit = FW.x-0 (every FW row in A0.06 has rating "--"). "W4." = W.4-0.
R2 Tag "W.6.1 | n" (not a row of A0.06) = W.6-n (same family/width, printed rating n; W notes: 1 layer per HR each
   side, rating 0 = 1 layer each side). Mark rfi "RFI-CR-01 W.6.1". Any other tag not in the schedules (XW.6.6-0,
   XW.6.3-1, XW.6.4-1, FW.4-1, FW.4-2, FM.1, XM.0.1 ...) = the closest schedule row of the same family with the
   printed rating; mark rfi "RFI-CR-02 <tag>" with the alternative's layers.
R3 Heights (board to underside of the floor / roof structure above, A0.06 GN 4 / GN 21, WOOD head detail "line of
   structure"): use the PRINTED section of the zone: L2 and L3 room zone 9'-2 7/8" (4/A5.05: 11'-0" floor to
   floor, 1'-9 1/8" floor zone); corridor / exterior shallow zone 11'-0" minus the printed shallow floor zone
   (1'-1 1/4" on 4/A5.05, 1'-1 3/8" on 7/A7.23 — use the one printed for that location); L4 per 1/A5.06 / 3/A5.07
   / A4.0x as printed; L1 per the A5.0x / A4.0x section of that bay (floor to floor L1-L2 = 14'-0"). If a reading
   used a value not traceable to a printed dimension (e.g. floor-to-floor minus a guessed sheathing), it loses.
   Faces with height 0 in a reading = not read; take the other reading if its source is printed.
R4 Length differences > 2 %: re-measure the centerline between the faces of the walls met from the vector
   geometry at the printed scale of that view (show "(hi-lo)/scale = x"), or use a printed dimension string if one
   covers the wall (CONFIRMADO). Record the value and why.
R5 solo_A / solo_B walls: open the plan at the band; keep the wall if it exists and carries our board (in scope,
   not in the grey "separate permit" area, not a CMU / concrete face without furring); otherwise discard with reason.
R6 Faces / layers: BOTH SIDES per the type (U-127). A face against a cavity of another wall still gets its board if
   the type section draws it. Wet rooms (toilet, shower, janitor) = moisture-resistant board on that face (A0.06 GN 11
   / plan note 4); tile walls = cement board where the enlarged plans / elevations show tile (GN 13).
R7 Ceilings (only A read them): keep A's ceilings; spot-check 5 of them against the RCP / unit RCP and note it.

Output (write before finishing; save progressively)
- /root/cr/work/etapas/4_canon/resuelto_{PISO}.json = {"floor", "walls": [final wall records in the reading schema
  (base = A record, corrected fields, plus "resolution": {"item", "decision", "source", "img"} when anything
  changed or was chosen)], "ceilings": [...], "soffits": [...], "discarded": [{id, reader, reason, img}],
  "rfis": [{id, item, sheets_searched, terms, assumption_loaded, delta}]}
- /root/cr/work/etapas/3_revision/resolucion_{PISO}.md (English): numbered list item → decision → N/SHEET → image.
Final message: under 120 words (walls final count, LF by type, how many differences resolved by each rule).
