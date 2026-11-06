CR City Hotel — rev2 FINAL: informe punto por punto (orden de 10:12Z)

1) ERROR → REGLA + COMPUERTA (U-124), BE-CR25, va en v81cf56 PUBLICADA
- B.walls() presenta los board-only de existing_walls como walls con sus caras. Cada cara se arma por cuarto y:
  · si dos entradas caen en la misma cara, las capas se suman;
  · el liner y el exterior se comparan con la cara de su misma clase del schedule;
  · el cement board es un overlay de la cara.
- Chequeo nuevo canon_no_vacio: canon con 0 walls y Partition Takeoff con más de 0 filas = FAIL.
- en_vacio(): un "N/A sin walls / sin canon" con el Partition Takeoff lleno = FAIL. Corre en correr() y en el wrapper de compuerta_entrega.
- Test test_be_cr25: repite rev1 (778 filas, 0 walls) y debe dar FAIL. También prueba BOTH SIDES con cara faltante = FAIL y con motivo N/HOJA = AMBER.
- Chequeos que en rev1 pasaban en vacío y ahora corren de verdad: BOTH SIDES, U-114, U-117, U-118, CC-R12, BE-08, BE-49, U-058, BE-03 y BE-82.
- Skill:
  · suite 51/51;
  · verificar_version 0 faltantes (788 reglas);
  · banco 0 familias distintas en 5 proyectos;
  · zip de 199 archivos;
  · INDICE: VIGENTE.

2) COMPUERTA OTRA VEZ, BOTH SIDES y alturas por cara
- Primera corrida con walls reales: 28 FAIL. Hoy: 169 PASS / 3 AMBER / 0 FAIL, con conteos plausibles: 493 walls con board impreso, 886 filas de markups y 804 filas en el Partition Takeoff.
- Los 3 AMBER, con motivo:
  · CE_ALTURA_IMPRESA: 15 alturas vectoriales de stairs en L4.
  · CE_MATERIALES_SCHEDULE: el schedule no imprime el dato en W.4-0, W.6-x, W.62-1 y FW.1-0.
  · BOTH SIDES: caras sin board, cada una con faces_none_reason, N/HOJA verificada e imagen:
    - F&B: nota "INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE", impresa en Kitchen 100 en 1/A7.45, en 1/A2.04 y en 3/A7.50;
    - retail: nota de 1/A2.01;
    - DW.4: cavidad (1/A2.03).
- Correcciones reales:
  · caras de baño (W.R. en toilet/lavatory según la GN 4 de A2.0x);
  · 213/313 completos;
  · demising por tramo;
  · imágenes circuladas por wall (493) y por fuente de altura (21) en Auditoria/evidencia_walls;
  · Status de fila = el número más débil;
  · operaciones de altura cerradas con "=".

3) LOS 15 AMBER DE CE_ALTURA_IMPRESA (U-140)
- Busqué la fuente impresa en 5/A6.02 y 11/A6.01 (imágenes en etapas/4_canon/img/alturas). Está impreso lo siguiente:
  · los datums LEVEL 4 6233.75' y ROOF 6247.75';
  · la nota "RATED WALL CONTINUOUS TO UNDERSIDE OF ROOF SHEATHING. TYP.".
- La cota de LEVEL 4 al underside del roof sheathing no está impresa en ninguna de las dos vistas. Queda la medida vectorial: es un AMBER real.

4) AUDITORÍA ADVERSARIAL U-138 #2
La hizo un subagente que no participó en el take-off. Muestra: 10 walls por piso, 3 a 8 baños por piso, 7 cadenas de burbujas, todos los RFIs y 4 filas del Material Summary recalculadas.
Hallazgos (13; todos aplicados después de verificarlos yo en el plano):
- F1+F2 (ALTA) Cement board en caras enteras de muro o faltante en showers. Lo rehice por programa (banos_cbu.py):
  · 33 cajas de shower medidas en vectores;
  · cement board solo en los lados sólidos (6/A7.02 y 8/9/A7.03 marcan tile solo en el shower);
  · L2 3,325.6 → 1,582.6 SF, L3 1,086.5 → 1,480.3 SF, L4 1,240.5 → 530.4 SF.
- F3 (ALTA) Shafts 2-HR de 7/A9.03 y 8/A9.03 ("W419, U497"). Agregué CH.6-2 en L3 (norte y sur) y en L4 norte: +374.19 SF de shaftliner, +351.31 LF de C-H y +72.40 LF de J-runner. RFI-09 queda cerrado.
- F4 Altura de la cara interior de los muros exteriores en L3: 9'-10 3/4" (4/A5.05).
- F5 Sheathing de L2: 11'-0" floor to floor (4/A5.06).
- F6 En muros non-rated, el cement board va en lugar del board (RFI-11).
- F7 y F8 Demising DW.4 por tramo y medidos a caras: 22.76 ft.
- F9 XW.6.2-L1-03: la cara retail queda excluida (RFI-05) y la cara exterior pasa a sheathing.
- F10 RFI-20 acotado con S1.02.
- F11 RFI-21 con la alternativa "PRE-FABRICATED ROOF CANOPY BY OTHERS"; se mantiene la decisión del usuario.
- F12 FW.2-L4-11: 4.99 LF, hasta la cara del CMU.
- F13 Cita W419/U497.
- Además encontré yo, al aplicarla, el error de cadena BE-CR26: vanos_puertas y esquinas_cb trabajaban sobre el canon final de la corrida anterior. Los arreglos de vanos de la auditoría #1 nunca llegaron al canon, tampoco en rev1. Ya está corregido, con un candado (assert) en finalizar.

5) DELTA POR MATERIAL vs rev1 (NET)
- Type X +732.42 SF (84,274.87 → 85,007.29)
- Type X W.R. −1,690.74 SF (28,802.47 → 27,111.73)
- Cement board −1,715.04 SF (5,308.33 → 3,593.29)
- Exterior sheathing +797.57 SF (16,309.09 → 17,106.66)
- Shaftliner +374.19 SF (943.15 → 1,317.34)
- C-H stud 6" +351.31 LF (799.02 → 1,150.33)
- J-runner +72.40 LF (184.50 → 256.90)
- Trim (corner bead) +77.99 LF (3,794.00 → 3,871.99)
- Control joints −17.88 LF (849.36 → 831.48)
- Joint compound −69.00 lb
- Tape −354.58 LF
- Type C, RC, suspension, hanger, carrying channel y soffit track: sin cambio.

6) rev2 FINAL
- Drive: Claude outputs › CR City Hotel - Castle Rock, CO (Owen-Ames-Kimball) 11-12-26 › "rev2 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR".
- La proposal y la guía están actualizadas, y PARA_REVISAR lleva los puntos 7 y 8 (cambios de rev2 y de la auditoría #2).
- rev1 quedó renombrada a "rev1 — REPLACED BY rev2 (NO USAR)" y tiene dentro la nota "00 REPLACED BY rev2 - NO USAR ESTA VERSION.md".
- Listado de Drive: (ver abajo)
- Todo está con commit y push en la rama claude/gifted-pasteur-x2sfzs.

TIEMPOS: rev1 387 min (6 h 27) + rev2 (ver TIEMPOS.md)
