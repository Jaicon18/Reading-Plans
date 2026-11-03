# CAMBIOS FINAL4 - Chuze Fitness Austin Bluffs (FINAL3 -> FINAL4, 2026-11-03)

Built with the current skill line: v81cf10 (CFA #2284 rev4) + v81cf11 (this run, tools/CAMBIOS_tools_v81cf11.md). FINAL3 kept untouched. Same canon (FINAL3) - no measured data changed; ported only the fields the newer tools read: takeoff `proyecto_datos` / `hojas_revisadas` (R80e.121 / R80e.122), `barrido_no_dibujado` (R80f.3), canon `constants.type_order` (R80f.9).

## 1. Quantity diff FINAL3 -> FINAL4 (Material Summary NET identical; every change explained by a v81 rule)

| Row / item | FINAL3 | FINAL4 | Rule |
|---|---|---|---|
| Ceiling perimeter track row name | 'Ceiling perimeter track at GWB ceilings (size not printed, RFI)' 567.58 LF | 'Ceiling / soffit track (size per source, see Where it comes from)' 567.58 LF | R80e.112 (VS Downey, v80x) row name |
| Metal stud blocking at wall-mounted items | one row 253.31 LF / 15 pcs | backing (per source) 247.31 LF / 15 + stud blocking (per source) 6.0 LF / 1 (10/A505.B AV niche studs) | R80e.112 backing track vs stud blocking split (one product per purchase line) |
| Alkali-resistant mesh tape | 447.61 LF NET, 475 pcs (6 % waste) | 447.61 LF NET, 448 (0 %) | v81cf8 T4 / BE-CF17: yield rows carry no waste |
| Partition Takeoff OTHER FRAMING | no subtotal | SUBTOTAL OTHER FRAMING 220.24 LF / 1,692.40 SF | v81cf8 T5 |
| Partition Takeoff existing walls block | 'EXISTING WALLS TO REMAIN - BOARD ONLY', stud 'none (existing wall, board only)' | 'BOARD-ONLY WALLS' block, stud 'none (board only; framing not in scope)', same 669.62 LF / 27,973.17 SF | R80f.1 (board-only walls) label |
| Workbook | 7 sheets (hidden _reglas seal) | 6 sheets + <excel>.sello.json | v81cf8 T6 / BE-CF18 |
| Markups | Contents SF = LF x H; 6 runs > 0.5 % Length vs LF; legend on the last page only; DETAIL '3D/A301' for A2-3D | Contents SF = board SF of the row; Length = LF; legend on every marked sheet; DETAIL 'A2-3D/A301' | v81cf11 R80f.8 / R80f.9 |

## 2. Gates of v81cf10 / v81cf11

reglas.py (850 rules incl. A_RFI_BARRIDO, A_NO_DIBUJADO, A_STRUT_STUD, A_BARRIDO_NO_DIBUJADO, A_PROYECTO_DATOS): only the back-check (S:§1:2fab33, the auditor registers it); plantilla validar / armar / verificar OK; markups verificar OK; registro entregable OK; alcances OK; etapas PASA; bitacora: only the back-check. BE-117 delivery audit (auditoria_entrega.py): before the fixes 83 failures (74 annot vs Excel row: SF one face vs board SF and DETAIL '3D/A301'; 7 Length vs LF > 0.5 %; 1 missing AD101 PNG; 1 README first line); after: 414 checks, 0 failures (AUDITORIA_ENTREGA_FINAL4.md).

## 3. Tool changes (v81cf11, prepared in /tmp/chuze/skill_v81cf11/ + zip; not pushed)

R80f.7 plantilla_excel.py verificar (PROJECT DATA block language) + markups_bluebeam.py resumen_vigente (newest summary of the canon); R80f.8 markups (Length = LF within TOL_PT, SF = board SF, hyphenated DETAIL); R80f.9 markups legend per sheet in schedule order; R80f.10 auditoria_entrega.py (new BE-117 tool). Tests: test_project_data_idioma.py, test_markups_vigente_reciente.py, test_markups_be117.py, test_auditoria_entrega.py (each fails with v81cf10). Suite 48/48, test_ciego_tools OK, verificar_version.py 0 faltantes.
