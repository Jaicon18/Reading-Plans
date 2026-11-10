# BITÁCORA rev15 — CR City Hotel

- 13:42 (10-nov): orden del usuario "revisa todo otra vez" (vía COORDINACIÓN, 18 puntos; hallazgos en cache_proyectos/.../revision_completa_rev14, commit 4cfc4da). Versión v81cf71 reservada en VERSION_EN_CURSO.md (U-144).
- Verifiqué en vectores antes de cargar: A0.06 GN 6 (set_texto); A2.04 cara del corridor x=853.6 continua 608.9-625.7; A7.50 caras x=1060.08 (8.77) y x=1070.16 (9.89).
- 3 forks de solo lectura en paralelo: (a) cajas de closet L2 / L3 unidad por unidad (24 con stipple, 168.92 SF); (b) evidencia ELEC / shafts / cove / 118B / ALC-E12 / BAR; (c) geometría RCP (offsets de vista por voto de segmentos, polígonos de exclusión, duct chases, offset doble de corridors, barrido de cobertura).
- Hallazgo propio: el "offset" de CLG-L2-56 no faltaba, sobraba (contorno ya en coordenadas del RCP, sumado dos veces). Hallazgo propio: la cobertura de borde contra el PDF de markups da 1.0 en todo (los trazos de los markups están en el contenido): la compuerta mide contra el plano LIMPIO y solo líneas paralelas al borde (el stipple cruza).
- Punto 4 refutado por los code plans (1HR FP en ELEC 221/321/421); punto 14 decidido por R-ALC-01 (+ cripples para que el soffit metálico esté completo); punto 12 W.R. refutado por A0.06 GN 13.
- Errores del método -> reglas R80e.165.25-.34 + compuertas CB_CR_R15_BARRIDO, CE_RCP_CONTORNO, CE_RCP_CUARTOS endurecida, guia_cambios_fallas + tests (U-124); BE-151 / BE-152.
- Cadena rev15 OK (2 corridas + markups desde el paso 37 tras ajustar la caja del texto para que no tape notas impresas). Delta: Type X +133.12, Type C +168.92, sheathing +58.98, C-H +371.31 LF, cripples +664.97 LF, CBU mesh +1,366.92 LF.
