# v81cf139 candidate = v81cf138 + strict CE_PROTOCOLO_3H (COORDINACIÓN 13:35)

Steps of a PREVIOUS rev are exempted (not judged again with the new rev) ONLY with validated evidence:
- a tiempos.log mark 'inicio revN' or 'revN entregada|subida' (lowercase rev glued to N, no hyphenated prefix, no negation / question mark on the line) with N LOWER than the current rev,
  time < start and placed before the start in FILE order; otherwise a VERSION_PROYECTO line with rev < current and ts < start;
- the CURRENT rev comes only from the project ('inicio revN' mark at the start / last VERSION_PROYECTO line; if they disagree = nothing exempt), never from drawing PDFs (W1);
- tope = min(evidence, start - 12 h); a row is exempt if it closes >= 12 h before the start AND (its mark is among the previous ones OR it closes before the tope);
- the alarm drops by POSITION only the previous rev's marks and its evidence; the rev's own start stays (R6, D1/D2).
Without valid evidence nothing is exempt (= v137 / v138). FECHAS_PUBLICACION v81cf138 = 2026-11-13T15:22:27+00:00 (commit 88707bb).
Tests: the v138 / v138r2 / v139 protocol tests (verif. 8-12 cases: Q1-Q4, Q4res, C1, B1, R1-R6, W1, D1, O1-O3, CR case).
Verification 13 = independent reviewer over the FULL CE_PROTOCOLO_3H function, <= 30 min. If it finds anything: report and stop.
