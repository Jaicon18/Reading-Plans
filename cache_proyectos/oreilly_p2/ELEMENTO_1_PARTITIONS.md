# ELEMENTO 1 — PARTITIONS (O'Reilly Evans CO #1, pasada 2)
Método: skill v80u (R80e.37). inventario_tags.py → hojas A/S raster (NO INVENTARIABLE, barrido manual con tag_manual) · lectura A y lectura B (subagentes independientes, sin verse) · comparar.py (12 coinciden, 11 difieren, 2 solo A, 0 solo B; 16 alertas "type no inventariado" = schedule raster, no son diferencias) · resolución dirigida desde B (36 resueltas, 1 RFI nuevo: RFI-13 gauge vestibule heads 600S162-43 en 3/A3.1 kn8 vs 16 ga en S4.1 kn3) · canon.py / partition_types.py (modo eje). Tiempo elemento 1: ~61 min.
**Decisiones del estimador (RESPUESTAS_RFI_ESTIMADOR.md) todavía NO aplicadas** (van en el overlay, paso 7).

Fuentes: schedule INTERIOR WALL TYPES S21/S24/S41/S42/S43/S61 en A1.1 (p.37); planta 1/A1.1; alturas 1-3/A3.1–A3.4, 4/A4.2, 5-7/A4.2, A1.2; exteriores 1/S5.3, 3/S5.3, 2-3/A3.1; detalle por wall en ELEMENTO_1_PARTITIONS.json (length_source / height_source / faces).

| Type | Wall ID | LF | H (ft) | Wall SF (LF×H) | Board SF (caras) | Caras / board |
|---|---|---|---|---|---|---|
| S21 | S21-N | 85.000 | 15.511 | 1,318.43 | 1,222.65 | 1 cara 5/8" X (int.) |
| S21 | S21-E | 84.646 | 14.625 | 1,237.95 | 820.68 | 1 cara 5/8" X; 28.53 LF sin board (detrás de S24) |
| S21 | S21-S | 85.000 | 15.511 | 1,318.43 | 1,096.81 | 1 cara 5/8" X; 9.36 LF sin board (detrás de S24) |
| S21 | S21-W1 | 9.156 | 16.396 | 150.12 | 150.12 | 1 cara 5/8" X |
| S21 | S21-W2 | 24.823 | 16.396 | 407.00 | 407.00 | 1 cara 5/8" X |
| **S21 subtotal** | 5 | **288.62** | | **4,431.93** | **3,697.26** | |
| S24 | S24-OF | 11.708 | 8.5 | 99.52 | 99.52 | 1 cara 5/8" X |
| S24 | S24-RR | 16.823 | 8.5 | 143.00 | 142.99 | 1 cara 5/8" X W.R. |
| S24 | S24-RRS | 8.854 | 8.5 | 75.26 | 75.26 | 1 cara 5/8" X W.R. |
| **S24 subtotal** | 3 | **37.38** | | **317.78** | **317.77** | |
| S41 | S41-B1V / B1H / B2H / B2V | 2.167 / 1.313 / 1.667 / 1.313 | 12.0 | 77.52 | 77.52 | 1 cara 5/8" X (box-outs kn5) |
| **S41 subtotal** | 4 | **6.46** | | **77.52** | **77.52** | |
| S42 | S42-01+S42-02 | 57.407 | 12.941 (pond.) | 742.93 | 1,303.76 | 2 caras 5/8" X (A 12.0/5.167, B 15.172/8.339) |
| S42 | S42-03+S42-04 | 58.500 | 9.908 (pond.) | 579.61 | 937.68 | 2 caras 5/8" X (A 5.167/12.0, B 8.869/16.311) |
| **S42 subtotal** | 2 | **115.91** | | **1,322.54** | **2,241.44** | |
| S43 | S43-OF-W | 8.000 | 8.5 | 68.00 | 140.00 | 2 caras 5/8" X (9.0 / 8.5) |
| S43 | S43-OF-E | 8.000 | 8.5 | 68.00 | 140.00 | 2 caras 5/8" X |
| S43 | S43-OF-S | 11.708 | 8.5 | 99.52 | 157.11 | 2 caras 5/8" X |
| S43 | S43-RR-W | 8.500 | 8.5 | 72.25 | 148.75 | X / X W.R. |
| S43 | S43-RR-S | 16.521 | 8.5 | 140.43 | 193.56 | X / X W.R. |
| **S43 subtotal** | 5 | **52.73** | | **448.20** | **779.42** | |
| S61 | S61-RR | 8.500 | 8.5 | 72.25 | 144.50 | 2 caras 5/8" X W.R. |
| **S61 subtotal** | 1 | **8.50** | | **72.25** | **144.50** | |
| EXT-8CFMF | EXT-MS1-8 / EXT-MS2-8 | 6.0 / 6.0 | 20.667 | 248.00 | 156.84 | 1 cara int. 5/8" X (12.0; MS2 parcial 16.396) |
| EXT-6CFMF | EXT-MS1-6 / EXT-MS2-6 / CORN-S | 6.0 / 6.0 / 36.0 | 20.667 / 20.667 / 7.969 | 534.88 | 0 | sin board |
| OTHER FRAMING | HEAD-A-8 / HEAD-A-6 (storefront_cripples) | 38.667 c/u | 9.333 | 721.76 | 25.79 | |
| OTHER FRAMING | VH-C / VH-B1 / VH-B2 (vestibule_head) | 8.75 / 5.667 / 5.667 | 4.953 | 99.48 | 13.40 | 6" 18 ga (RFI-13) |

Interior partitions (S21–S61): 509.60 LF · Wall SF 6,670.22 · Board SF 7,257.91.
Avisos de partition_types (R11, solape de esquina 0.35–0.47 ft): S21-S↔S24-RR, S24-OF↔S43-OF-W/E, S24-RR↔S43-RR-W, S24-RRS↔S43-RR-S — pendiente corrección dirigida antes del Excel.
