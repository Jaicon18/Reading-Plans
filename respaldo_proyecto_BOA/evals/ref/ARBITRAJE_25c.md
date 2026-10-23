# ARBITRAJE #25c y PAQUETE v77c — 2026-10-21 (decisiones del usuario U1–U11)

Material de arbitraje: lleva números de BOA. **NO viaja con el paquete** (E24). Autoridad: decisiones del usuario
(Bluebeam, 2026-10-20) > plano > rangos > reglas.

## 1. U1–U11: regla, compuerta, test
| U | Regla (SKILL §25) | Compuerta | Test |
|---|---|---|---|
| U1 ATM | R77.11 (reemplaza R77.1/D1): el framing del recess de ATM / equipo empotrado está en la wall que lo contiene; extra framing ATM = 0; framing adicional impreso explícito → `atm_recess.extra_printed` = RFI con delta, no suma | canon `_atm_wall` (la wall del ATM en studs_nodos + corridas); accesorios (`extra_framing` de ATM a mano / fórmula vieja / extra_printed sin texto impreso = error); chequeos_v72 R72.11 | test_v77.py (2 casos U1), test_v72.py R72.11, test_accesorios*.py |
| U2 A1 | ya es R77.10 (largo a través de doors) | chequeos_v77 `r77_10` | test_v77.py R77.10 |
| U3–U6 | valores del proyecto (sin regla nueva; R77.10 + R77.3) | — (solo referencia v7 y rangos v24) | grader contra v7 |
| U7 3-5/8" | R77.16 = R60.1: posiciones @ O.C. + 1 + L + T | studs_nodos (cada extremo en un nodo) | test_v77c.py U7 |
| U8 acoustical sealant | R77.12: EXCLUIDO en todos los proyectos; sealant at base of gypsum (exterior) sigue con familia propia | canon `_sealant` + `excluidas`; alcances ALC-19 `EXCLUIDOS`; plantilla_excel `acoustical_err` (validar + verificar) y fusionar sobrescribe el alcance; familias.py; grader modo "excluir" | test_v77c.py (grader, alcances, fusionar), test_plantilla_v68.py (Excel malo con renglón), test_canon*.py |
| U9 preguntas | R77.13: anunciar el total, una por turno; PARA REVISAR n/N con total | `revisar_err`, `verificar_v77c` | test_v77c.py U9/U10 x2 |
| U10 orden | R77.14: floor plan por type A→Z, luego detalles en el orden del plano | `ordenar_revisar`, `revisar_err`, `verificar_v77c` | test_v77c.py |
| U11 mensajes | R77.15 (proceso) | — (G_PROCESO) | test_v77c.py (texto en SKILL) |

## 2. Referencia v7 vs v6 (`BOA_Broomfield_REFERENCIA_v7.xlsx`, hoja "CAMBIOS v7"; v4/v5/v6 sin tocar)
| Item | v6 | v7 | Operación |
|---|---|---|---|
| extra framing ATM | 109.87 | **0** | U1. 109.87 = 49.87 (EXT-6CFMF #65, drive-up sistered + furring) + 60.00 (columna AD de G/G1) |
| 1-5/8" stud | 3,860.10 | **3,981.60** | +60.00 (AD de G/G1 vuelve a su type, U1) + G #48 y #52: (ROUNDUP(12.333/1.3333) − ROUNDUP(11.625/1.3333)) × 2 rows = +2 pcs × 15.375 = +30.75 c/u. G1 #51/#53: +0 pcs |
| 3-5/8" stud (familia) | 6,227.89 | **6,690.00** | U7; renglón = 6,690.00 − CSR 104.77 = 6,585.23 |
| 6" stud | 4,525.47 | **4,494.72** | U6 norte 14.95 → 13.19: (10 − 12) pcs × 15.375 = −30.75; U5 B2K @ 24": +0 |
| bottom / top track 6" | 293.04 | **291.79** | B2K +0.51, norte −1.76 |
| bottom / top track 1-5/8" | 285.97 | **291.50** | G +1.42 +1.42, G1 +1.67 +1.02 (doble row) |
| 5/8" gyp regular | 17,450.60 | **17,609.24** | board del renglón / LF × ΔL: G +43.54 ×2, G1 +51.48 +31.37, B2K +15.77, norte −27.06 |
| bracing | 2,624.23 | **2,637.07** | igual, +12.84 |
| ballistic / 3/8" gyp | 74.00 / 57.04 | **78.10 / 60.82** | U5: 10.08/1.26 × 0.513; 9.29/1.26 × 0.513 |
| FRT + polyiso | 3,754.28 | **3,727.22** | U6: 229.86/14.95 × −1.76 |
| acoustical sealant | 957.52 | **sin renglón** | U8; exclusión en Clarifications #14b; columna Sealant de Partition Takeoff en blanco |
| types | G 80.875 · G1 17.11 · B2K 1.26 · EXT 217.64 | **G 82.291 · G1 18.457 · B2K 1.773 · EXT 215.88** | U3 12.333 ×2 · U4 3.507 + 3.18 · U5 1.773 · U6 13.19 |
| A1 | 82.23–84.04 | sin cambio | U2 |

Verificado: los 60.00 de G/G1 no se pierden (pasan a 1-5/8" stud).

## 3. RFIs / PARA REVISAR
1/2. **RFI-ATM-DU:** 6/A08.11 imprime "2 1/2" METAL STUD SISTERED TO 6" METAL STUD" y "FURRING ON 5/8" FRT PLYWOOD"
   (img `img/U1_A0811_6_DU_ATM_sistered_furring.png`, reabierta: rojo sobre los dos rótulos, azul sobre el título 6/A08.11).
   U1 = 0; si se cargara: +49.87 LF. La regla genérica lo manda a RFI, no lo suma.
2/2. **Parapet norte:** U6 cambia solo la wall de 6" CFMF; el parapet norte (#160, 14.95) quedó igual. Si sigue a la
   wall: −1.76 LF de parapet track c/u. Ballistic: las pruebas dan 85.31 vs 87.65 (base del contorno, rango 85.31–87.65).

Detalles de A08.11 revisados: 1 WU ATM ELEVATION (R.O.), 4 WU ATM SECTION, 6 DU ATM SECTION (sistered + furring
impresos → RFI), 7 ATM ROOM PLAN; 2 bollard, 3 plinth (Div. 06), 5 DU elevation, 8–9 elevaciones: sin framing extra.

## 4. Paquete v77c
| Archivo | md5 |
|---|---|
| take-off-metal-frame-drywall_v77c-dev.zip | 93d2ed3fc48b2f870646dde430e995da |
| take-off-metal-frame-drywall_v77c-ciego.zip | 6f7ad5e71b133f43b64ada9821ed550f |

SKILL.md md5: dev 2cf728c76e7ba0fd03fdca3dc4592046; ciego def2b9647bdae33dfce37a885c2395ec.
Suite dev desde carpeta limpia (zip descomprimido, `correr_suite.py`): **57/57 OK** (nuevo test_v77c.py).
test_smoke_ciego OK; test_ciego.py modo prueba OK. Ciego: `armar_ciego.py` con rutas absolutas;
test_ciego_tools --estricto 0 hallazgos (y 0 con 246 valores externos de v7, `anexos/valores_v7_25c.json`);
canon.py del ciego = dev sobre canon77b A y B.

## 5. Antes / después (grader completo)
Antes = Excel entregado por la prueba vs ref v6 + rangos v23 (grader v77b). Después = takeoff.json de la prueba migrado
(sin acoustical; revisar con fase) + familias_out de tools v77c sobre su canon, armado con plantilla v77c
(`anexos/regenerar_excel_v77c.py`, sin la compuerta reglas.py que pide la carpeta de trabajo completa) vs ref v7 +
rangos v24 (grader v77c).

| | 25A antes | 25A después | 25B antes | 25B después |
|---|---|---|---|---|
| extra framing ATM | FALTA (ref 109.87) | 0 IGUAL | FALTA | 0 IGUAL |
| acoustical sealant | 1,193.62 IGUAL | EXCLUIDA OK | 1,437.39 CERCA | EXCLUIDA OK |
| B2K | 1.773 MAL | IGUAL | 1.773 MAL | IGUAL |
| G1 | 17.945 CERCA | CERCA (stub 2.667 vs 3.18) | 18.458 CERCA | IGUAL |
| **Total** | **89.3** | **95.6** | **87.5** | **96.5** |

Excel original de la prueba vs v7 (sin regenerar): 25A 93.1, 25B 93.9.
