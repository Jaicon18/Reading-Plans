# Xfinity - Inter Quest, CO TI Improvement Project — caché del take-off (skill v81cf77)
- GC único (Gmail estimating@jchunter.us revisado 10-nov 8:25 PM PT, U-091): BCI National Construction & Facilities (Kyle McGee, Estimating Lead; Morgan Fergus, Assistant Estimator). BuildingConnected opportunity 6aed6ad3afb7ca85c2b332e1 "Drywall & Framing"; también ACT (6aed6a9b934f0dc6ba8b695d) y Painting (6aed6bc0f2d63c4f3e746ff8) = no son nuestro alcance. Bid Nov 13, 2026 end of day; cotizar como day work.
- 1333 Interquest Parkway, Lot 11, Colorado Springs, CO 80921. 1,798 SF TI, 1 story, IBC 2021, Type V-B sprinklered. Architect: Robert F. Vanney.
- BC Files: "Xfinity BP_Colorado Springs, CO_Interquest_Complete PDF Set_10-08-26_R0.pdf" (17 hojas: A0.1-A5.0, E0.0-E3.0, M0.0-M2.0, P1.0) + "Interquest Concrete Rough layout.png". Sin addenda. Specs en hoja A0.3.
- Copia limpia = original (1,589 anotaciones, TODAS "AutoCAD SHX Text" en E/M/P = texto del dibujo, se conservan R80f.1; 0 markups de take-off).
- Drive bid set: Projects › "Xfinity - Interquest, Colorado Springs, CO (BCI National) 11-13-26" (id 1j-XN0BxYIHRUtkQm1fxaCFgVqRmostin).
- Descarga: cache_proyectos/herramientas/bc_descargar.js (BE-XF01: Download All por URL S3 interceptada + curl).
- Reporta a COORDINACIÓN (session_01BLzQaGL6Hvg3oNXm79RWvR).
- BE-XF02 (10-nov, error mío en el brief de lectura): dije que get_pixmap(clip=) va en espacio sin rotar (multiplicar por derotation_matrix). Falso: en hojas con rotation 270 PyMuPDF toma el clip en pt VISIBLES (prueba: 'STORAGE' de A2.0, clip visible = texto, clip derotado = blanco). Lo encontró el subagente de burbujas. Arreglo: brief corregido y aviso a las lecturas A/B para regenerar recortes; regla para todos los proyectos: el brief común dice "clip = rect visible" y todo recorte se reabre y se verifica (U-118). Va al registro con la próxima versión del skill.

## rev1b (10-nov, COORDINACIÓN BE-XF07)
- Leyenda del PDF de markups con Subject LEGEND (antes 'W2' / 'CF' sin /Measure en página sin /VP: inflaban los grupos de Bluebeam).
- Drive › rev1 FINAL PARA REVISAR › Planos marcados: 'XF_markups_rev1b - OPEN IN BLUEBEAM.pdf'; el anterior = 'zz NO USAR - XF_markups_rev1 old.pdf'. 12 archivos con contenido distinto renombrados 'zz old …' (drive_renombrados.json); nada borrado. Cantidades del Excel idénticas (0 celdas distintas).
- Compuerta VERDE 203 PASS / 2 AMBER / 0 FAIL; skill v81cf84.

## RFI-01 cerrado (11-nov, decisión del usuario, opción A — U-174)
- 26'-0" de A0.1 ("1 STORY - 26 FT") queda como decisión del usuario; 0 RFI abiertos. Cantidades sin cambio (Partition Takeoff y Material Summary idénticos).
- Actualizados: Pending Items (vacío), Review Item 4/8, Scope Checklist, SEGUIMIENTO, PARA_REVISAR, GUIA, RESUMEN, CHECKLIST, proposal (cláusula RFI-01 = decisión del usuario, total igual).
- Drive: 18 anteriores renombrados "zz old U-174 …" (el PDF = "zz NO USAR - XF_markups_rev1b old (antes de U-174).pdf"), nuevos subidos con subir_entrega.py; nada borrado.
- Compuerta VERDE 204 / 2 / 0 (CB_U_174 PASS). Skill v81cf85.

## U-175 + U-176 alturas (11-nov, orden COORDINACIÓN)
- Dos lecturas ciegas de alturas (H-A en alturas/A, H-B en alturas/B; ninguna vio el Excel ni la otra): 16 alturas iguales + 5 cuartos iguales (21/21).
- comparar_alturas: 20/20 markups OK (Bluebeam Depth = Excel Height = altura impresa) -> Auditoria/COMPARACION_ALTURAS.csv; CHECKLIST B2 con el N/N y la muestra al azar (5 walls, 3/3 alturas).
- alturas_extremo: cierre 16/16, reglas físicas 15/15, 3 cuartos / 6 pares cuarto-wall, ALTURAS_REVISADAS.pdf (3 alturas + sección) y capa 'HEIGHTS (U-176)' en el PDF de markups.
- Compuerta VERDE 206 / 2 / 0. Drive: 5 anteriores 'zz old U-176 …' / 'zz NO USAR - XF_markups_rev1b old (antes de U-176).pdf', 40 nuevos. Skill v81cf86.

## Auditoría U-138 (11-nov) — U-177
- Material Summary con gauge y N/HOJA en cada renglón de stud / track / header / brace: 362S125-33 (W2 + SOF-01, 250.67 LF), 362S162-54 (16 ga de 8/A2.0, 125 LF; ala 1-5/8" no impresa, confirmar), 250S125-43 / 250T125-43 (CF), 362T125-33 tracks.
- Blocking: '6" sheet metal blocking strapping' 14.5 LF (A5.0 EV-44 / EV-45, coil LF) y '16 ga x 6" x 1-1/2" unpunched track' 32.88 LF (8/A2.0).
- Patch & repair W1 / W4: U-064 no aplica tal cual (no dice 'replace'); conservador cargado (RFI-06 A): caras del tenant a C.H. + 6" = 2,589.62 SF de 5/8" Type X (misc PR-*); B = -2,589.62 SF (solo allowance), C = +1,937.32 SF (W1 a estructura 26'-0").
- Compuerta VERDE 211 / 0 / 0; Drive: 18 'zz old U-177' + 18 nuevos; `subir_entrega.py --vigente` PASS. Proposal $17,192 con impuesto (antes $8,814).

## U-178 (11-nov): RFI-06 'Verificar a mano'
- A conservador (+2,589.62 SF) sigue cargado; RFI-06 = PENDING - user manual verification en Pending Items, SEGUIMIENTO, PARA_REVISAR y GUIA (hojas A2.0, A0.1 nota 3, A1.0). Compuerta v81cf91 211/0/0; Drive 16 'zz old U-178' + 16 nuevos; --vigente PASS.
