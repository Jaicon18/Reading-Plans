# PROCESO_CORRIDA - Xfinity - Interquest, Colorado Springs, CO (BCI National) - stages 6-8, rev1 (2026-11-11)

Chain: `bash /root/xf/work/scripts/cadena.sh` (every tool through `bitacora.py run`, stops at the first rc != 0) -> CHAIN-OK.

1. Canon re-built by program: `scripts/resolver.py` (A / B resolution) + `scripts/formato.py` (format for canon.py, F1-F6 gate data).
2. Sheet map: `etapas/SHEET_MAP.json` (title blocks of the 17 pages) -> `scripts/preparar.py` -> `etapas/0_mapa/SHEET_MAP.md`; `arranque.py`.
3. Inventory re-run (`inventario_tags.py`, `contar_tags.py A2.0@p5 W1 W2 W2A W3 W4`), `runner/evidencia.py` (img per wall / RFI).
4. `scripts/alturas_img.py`: circled height sources (2/A2.0 W2 note, 5/A2.0, A3.0 tags 12'-0" / 10'-0" / 9'-0"), re-opened.
5. `canon.py` -> `out/familias_out.json`; `insumos_canon.py fo / alcance`; `inventario.py`; `framed_openings.py`; `alcance_filtro.py`;
   `vigas_sobre_walls.py NONE A2.0@p5` (no structural sheet).
6. `scripts/sellar_y_marcar.py`: closer.py seals W2-01, W2-02, CF-01, CF-02; planmark PNG per sheet / type (etapas/7_imagenes/planmark).
7. Bluebeam markups: `markups_bluebeam.py` (A2.0 walls) -> `scripts/demo_geom.py` (A1.0 polylines from the DEMO bands, checked on
   etapas/4_canon/img/demo_check.png) -> `demo_geom_markups.py` -> `demo_cruce.py` (DEMO_CRUCE.md) -> `markups_demo.py` -> verificar.
8. RCP: `scripts/rcp_polys.py` measures the 6 A3.0 rooms on the vectors (rcp_cuartos.json, check image etapas/4_canon/img/rcp_check.png)
   and the SOF-01 header line (rcp_polys.json) -> `markups_rcp.py` (SOF-01-BOARD) -> `scripts/excluded_rcp.py` (EXCLUDED x 6,
   rotation-aware, unique /NM) -> `scripts/verificar_final.py`.
9. `scripts/imagenes_hoja.py`: A1.0 / A2.0 walls, A3.0 ceilings PNG (U-158 names).
10. Scope ledger: `alcances.py escanear / renglones` -> `scripts/registro_renglones.py` -> `registro.py crear` (54 rows).
11. `scripts/takeoff_json.py` (project data, RFI-01 open with full-set grep, RFI-02..05 closed, 6 Review Items with circled crops,
    ALC-01..24 + 16 extra rows, 17 sheets reviewed, not-drawn sweep) + `scripts/evidencias_reglas.py`.
12. `plantilla_excel.py validar / armar (reglas.py sealed) / verificar` -> etapas/8_excel/XF_Takeoff_FINAL_rev1.xlsx.
13. `scripts/registro_marcar.py` (54 rows verified) -> `registro.py entregable` -> `alcances.py compuerta`.
14. Final PDF `etapas/8_excel/XF_markups_rev1 - OPEN IN BLUEBEAM.pdf` (Page Labels, /VP, DepthUnit /C 1, unique /NM without '/',
    no signatures) -> `verificar_final.py` -> `verificar_markups_excel.py` (20 / 20 OK) -> etapas/VERIFICACION_MARKUPS.md.

Tool limits and fixes: etapas/TOOL_LIMITS_CALC.md.
