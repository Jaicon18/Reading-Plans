# TOOL_LIMITS_CALC - Consumer Cellular - Centennial, CO

| # | Limit found | Program fix (this run) |
|---|---|---|
| 1 | inventario_tags.py does not read the 1/A500 type legend (types are section titles with diamond keys A#, C#, D, E#, H) nor single-letter tags (D) | types verified by the independent schedule reader (fichas.json); D tag located by both readings |
| 2 | Bubble detector of set_texto read 0 bubbles on A100 / A400-A402 (rotated pages, 2-line text bubbles, level markers counted as rings) | scripts/barrido_burbujas.py text-pair sweep + eye verification of every ring and candidate (burbujas_verificadas.json) |
| 3 | canon.py family parser reads stud size '3 5/8"' (space) as 8" | ajustes_canon.py step 25: label normalized to '3-5/8"' |
| 4 | Reading nodes did not cover every wall end after the resolution | ajustes_canon.py step 10: node topology generated from the A100 bands |
| 5 | mep.py registration M101 / P101 vs A100 returned None (< 25 votes) | declared registro.no_usable with its reason (ducts EXCLUDED by standing order) |
| 6 | Sources with prose fail RX_SRC (N/SHEET) | ajustes_canon.py step 15: prose to source_info, N/SHEET tokens kept |
