# RESUMEN rev7 — CR City Hotel (every quantified ceiling / soffit has its markup)

User question (Bluebeam, A3.04 rev6): "why do some have markups and others don't?". Cause: markups_rcp drew only canon ceilings[]; the 73 ceilings / soffits quantified as separate rows (misc_items CLG / SOF / RS6 / CAN / BW) had NO markup (e.g. L4 Women 417 129 SF, Men 418 94 SF, Elec 421 11 SF). F&B 410 / 411 / 419 without polygon is correct (EXCLUDED).

## What changed
- Quantities: NONE (DELTA_rev6_rev7 empty). Markups only.
- 73 markups added (green): area polygon with /Measure (Bluebeam Area = drawn area; the Contents states layers x area = board SF of the Excel row) or polyline with Length = LF and Depth = developed width (Wall Area = board SF).
- Each markup sits on its RCP (A3.0x) or on the enlarged sheet where it was measured (A7.xx, A6.01), Contents = board · ID · cause · SF / LF · N/SHEET · ID.
- New gate CE_RCP_COMPLETO (Excel -> markup): every ceiling / soffit row with SF > 0 has its markup TO-<id> with the same SF / LF (+-0.5 %); CE_VISTA_BLUEBEAM counts the layers of a multi-layer ceiling.

## The 73 rows that had no markup (how each was drawn)

### measured (48)

CLG-L1-00 (A7.45), CLG-L1-07 (A7.30), CLG-L1-09 (A7.30), CLG-L1-14 (A7.50), CLG-L1-15 (A7.50), CLG-L1-16 (A7.50), CLG-L1-17 (A7.31), CLG-L2-39 (A3.02), CLG-L2-40 (A3.02), CLG-L2-41 (A3.02), CLG-L2-42 (A3.02), CLG-L2-43 (A3.02), CLG-L2-44 (A3.02), CLG-L2-45 (A3.02), CLG-L2-46 (A3.02), CLG-L2-47 (A3.02), CLG-L2-48 (A3.02), CLG-L2-49 (A3.02), CLG-L2-50 (A3.02), CLG-L2-51 (A3.02), CLG-L2-52 (A3.02), CLG-L2-53 (A3.02), CLG-L2-54 (A3.02), CLG-L3-89 (A3.03), CLG-L3-90 (A3.03), CLG-L3-91 (A3.03), CLG-L3-92 (A3.03), CLG-L3-93 (A3.03), CLG-L3-94 (A3.03), CLG-L3-95 (A3.03), CLG-L3-96 (A3.03), CLG-L3-97 (A3.03), CLG-L3-98 (A3.03), CLG-L3-99 (A3.03), CLG-L3-100 (A3.03), CLG-L3-101 (A3.03), CLG-L3-102 (A3.03), CLG-L3-103 (A3.03), CLG-L4-106 (A3.04), CLG-L4-108 (A3.04), CLG-L4-110 (A3.04), CLG-L4-112 (A3.04), CLG-L4-114 (A3.04), CLG-L4-117 (A3.04), CLG-L2-123 (A3.02), CLG-L2-124 (A3.02), CLG-L1-127 (A7.31), RS6-L3 (A3.03)

### measured, scaled to the loaded SF (15)

CLG-L1-01 (A7.45), CLG-L1-08 (A7.30), CLG-L1-10 (A3.01), CLG-L1-12 (A7.31), CLG-L1-18 (A7.50), CLG-L2-56 (A3.02), CLG-L2-58 (A3.02), CLG-L3-87 (A3.03), CLG-L3-88 (A3.03), CLG-L3-104 (A3.03), CLG-L4-118 (A3.04), CLG-L4-119 (A3.04), CLG-L2-122 (A3.02), CLG-L1-125 (A7.31), CLG-L1-126 (A7.50)

### locator (6)

SOF-L1-01 (A7.31), SOF-L4-01 (A6.01), SOF-L4-02 (A3.04), BW-L1-RETAIL (A3.01), CLG-L2-64 (A3.02), CAN-L1-ENTRY (A3.01)

### measured lines (4)

SOF-L2-01 (A3.02), SOF-L2-02 (A3.02), SOF-L3-316 (A3.03), SOF-L3-318 (A3.03)

Locators: the source gives only dimensions (sections / details), so the markup sits at the printed label of the element with the loaded quantity and the cause written in the Contents (no invented plan geometry).

