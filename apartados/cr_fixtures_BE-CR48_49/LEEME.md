# CR City Hotel rev20d: real-case fixtures for BE-CR48 / BE-CR49

Written on 14-nov ~00:50 UTC from the project canon (CR-main session).

## Files
- **fixture_cr_rev20d_ANTES.json**: the canon BEFORE the fix.
  - Run with v81cf138i, 13-nov 23:54 UTC.
  - Result: U-199 (7) FAIL on 4/A4.03:FW.2-L3-06, section 9.8958 vs take-off 8.875.
  - Result: CE_A2_ALTURAS FAIL on 8'-10 1/2" and 11'-6".
- **fixture_cr_rev20d_DESPUES.json**: the canon AFTER the fix (chain with v81cf138j, 14-nov).

## BE-CR48: head FW lowers a face → replace the old U-199 (7) dispositions
**Before**
- u199.secciones 4/A4.03 FW.2-L3-06 has altura_ft 9.8958. That value is derived (structure line of 4/A5.05); the section prints only 11'-0".
- There is no disposition for it.
- 12/A6.00:FW.2-L2-06 and 6/A6.00:FW.2-L2-02 keep the R5 disposition "take-off 9.8958 correct".
- The canon now has 8.875 and 9.4167.

**After**
- Each re-headed face has a control-7 disposition from revisor rev20d_fw_head.
- Its nhoja is the N/HOJA of the room C.H.: 1/A7.23, or 7/A7.23 for the corridor.
- It quotes the rev20c text it replaces in 'reemplaza'.
- Its img is the A0.06 FURRED WOOD HEAD crop.

## BE-CR49: height derived from a room C.H. → Source in ft-in plus the sheet where it is printed
**Before**
- FW.2-L3-06 height_source:
  `... room '317 Lobby' C.H. 8.375 (ALTURAS_CUARTOS, blind readings A / B): 8.375 + 0.5 = 8.875`
- CE_A2_ALTURAS cannot find 8'-10 1/2" or the operation on any sheet.

**After**
- FW.2-L3-06 height_source:
  `... room '317 Lobby' C.H. 8'-4 1/2" printed on 1/A7.23 (...): 8'-4 1/2" + 6" = 8'-10 1/2"`
- FW.4-L1-03:
  `C.H. 11'-0" printed on A3.01: 11'-0" + 6" = 11'-6"`

Project code: /root/cr/work/scripts/rev20d_fw_head.py, functions _ftin and the block "U-199 (7)".
