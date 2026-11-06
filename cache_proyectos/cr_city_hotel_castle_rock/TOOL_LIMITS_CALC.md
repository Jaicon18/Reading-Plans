# TOOL LIMITS found in this run (fixed in the tool with test, U-084)
- BE-CR01 inventario_tags.py: types with a dot (W.62, XW.6.3), schedule titled 'WALL ASSEMBLIES', sheet numbers of the index never types, title under 'SHEET TITLE:' ('LVL 2' = plan), own sheet number not a candidate. Test test_cr_city_hotel.py::test_cr01_regex.
- BE-CR02 canon.py / familias.py / plantilla_excel.py / accesorios.py: families 5/8" Type C, 1" shaftliner, 5/8" exterior gyp sheathing Type X, 5/8" cement board, C-H stud / J-runner by size. Test test_cr02_familias.
- BE-CR03 canon.py: ceiling system resilient_channel (board on RC under wood joists). Test test_cr03_rc.
- BE-CR04 canon.py: board-only project (no metal walls) no longer stops with "'runs' vacío". Test test_cr04_board_only.
- Reader band transposed (A L1: c0/c1 = extent): normalized by program in comparar_AB.py / build_canon.py (narrow span = faces).
