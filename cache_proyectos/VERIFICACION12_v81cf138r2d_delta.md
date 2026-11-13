# VERIFICACIÓN 12 — delta CE_PROTOCOLO_3H (3aa8703 -> 25f9fd1), v81cf138r2d

**Veredicto: NO PUBLICAR** (1 hallazgo medio W1 + 1 bajo D1/D2). Alcance: solo RX_EVID_INICIO, RX_EVID_ENTREGA, _rev_clave,
marcas_rev_anterior(desde=), alarma_fallas(previas=, tope=) y proceso_v119 en tools/compuerta_entrega.py.
Candidato /tmp/v138r3/take-off-metal-frame-drywall vs v137 /tmp/v137/take-off-metal-frame-drywall, vía proceso_v119.
Los datos son sintéticos y están en /tmp/verif12/tmp. Los scripts están en /tmp/verif12. Todo se corrió con python3 -I y no se hizo commit.

## Hallazgos

### W1 (MEDIO): una etiqueta actual mal leída vuelve "menor" el propio 'inicio rev21'
- Entrada: entrega "rev21 FINAL PARA REVISAR" con Take-off/Z9_Takeoff_rev21.xlsx más un PDF de planos
  Planos/A-101 Rev 25.pdf más nuevo (mtime). VERSION_PROYECTO: `2026-11-13T18:00:00Z | rev21`. tiempos.log:
  `11-12 17:00 0 Arranque / 11-12 17:30 1 fin / 11-12 18:30 2-3 fin / 11-13 08:00 inicio rev21 / 11-13 08:30 4 fin`.
  TIEMPOS.md cierra 1, 2-3 y 4; la única corrida es la de --paso 4.
- v137: FAIL (paso 1 y paso 2-3 sin su corrida; alarma del 50 %).
- Candidato: **PASS**, con el mensaje "2 paso(s) ... son de una rev anterior". El arranque pasa a 08:30.
- Causa: `_etiqueta_rev` toma el .xlsx/.pdf más nuevo, aceptando incluso 'Rev 25' con espacio, así que la rev actual se lee como 25.
  `_k0_rev` corta entonces después de 'inicio rev21', y esa marca, que es el arranque de la rev ACTUAL, cumple la regla 1
  (21 < 25, hora < arranque, antes de k0) y exime los pasos propios de rev21. El control W0, con la etiqueta bien leída, da FAIL igual que v137.
- Arreglo sugerido: una evidencia no puede tener la etiqueta del Excel de la entrega ni la del renglón de VERSION_PROYECTO de la rev
  actual. O bien, sin coincidencia entre esas fuentes, et = None y no se exime nada.
- Script: /tmp/verif12/adv12_delta.py (casos W0 y W1).

### D1/D2 (BAJO): la alarma quita marcas por VALOR (`set(previas)`), no por posición
- D1: `11-11 08:00 1 inicio / 11-11 08:30 1 fin / 11-11 18:00 rev20 entregada / 11-11 08:30 1 fin (copia exacta) / inicio rev21 ...`.
  La copia está DESPUÉS de la evidencia, así que por la regla 4 no está exenta y por la regla 6 debe quedarse en la alarma, donde exigiría
  la corrida de --paso 1. v137 da FAIL y el candidato **PASS**.
- D2: la misma copia exacta, puesta DENTRO de rev21 (12 h justas hacia atrás, sin problema de orden), también se quita.
  v137 da FAIL y el candidato PASS.
- Como es la misma marca copiada, la gravedad es baja, pero se desvía de la regla 6 ("quita solo esas marcas").
- Arreglo sugerido: quitar por índice (posiciones de ms[:fin]), no por valor.
- Script: /tmp/verif12/adv12_delta.py (casos D1, D1c y D2).

### Observaciones (según la regla tal como está escrita, no bloquean)
- O1 're-inicio rev20' (el guion da \b), O2 'rev20 entregada? no, pendiente' y O3 'falta: rev20 subida' cuentan como evidencia.
  v137 da FAIL y el candidato PASS. La regex no ve negaciones después de la marca ni prefijos con guion.
- La marca de evidencia misma se exime aunque esté a menos de 12 h del arranque, como dice la regla 4. Eso mueve t0 de la alarma
  como máximo hasta esa marca.

## Casos que se comportan bien (adv12_delta.py)
- Siguen en FAIL, igual que v137:
  - etiquetas: 'REV20 entregada', 'Rev20 entregada', 'prev20 entregada', 'rev20 NO entregada', 'rev 20 entregada', 'rev20entregada',
    'rev20 entregadas', 'inicio REV20', 'reinicio rev20', 'rev2026 entregada';
  - revs posteriores: 'rev22 entregada' y 'rev21a entregada' con la rev actual rev21;
  - orden de revs: rev10 contra actual rev9 (N2) y rev20a contra actual rev20 (N3);
  - evidencia exactamente en el arranque (T1);
  - VP rev20 sellado 08:30 PT, después del arranque (T4);
  - dos evidencias con los pasos después de la última (M1).
- Etiqueta no detectable (U1) y misma rev 'rev21 subida' (L12): AMBER en los dos árboles, sin cambio.
- PASS legítimo:
  - C1 (control);
  - N1 rev9 con actual rev10;
  - N4 rev20 con actual rev20a;
  - T2 evidencia 1 min antes del arranque;
  - T3 y T5, VP con Z y con -08:00 antes del arranque (zona horaria correcta);
  - D1c (control).
- Tests del repo (corren al importar test_compuerta_entrega en las corridas existentes): los casos de legitimidad requeridos pasan.

## Corridas (todas rc=0)
| script | resultado |
|---|---|
| /tmp/verif12/adv11_rerun.py (copia de /tmp/verif11/adv11_delta.py con BASE en /tmp/verif12/tmp/a11) | REGRESIONES: 0 |
| /tmp/verif12/adv10_rerun.py (verif10 adv10_delta.py) | 0 marcas de regresión |
| /tmp/verif12/adv9_rerun.py y adv9b_rerun.py (verif9 adv9_protocolo / adv9_protocolo2) | 0 marcas de regresión |
| /tmp/verif12/adv8_rerun.py <tree>/tools (verif8 adv8_pm06.py) | única diferencia: tiempos_desde existe en el candidato (Q1: 0 exentas) |
| verif9 adv9_canones.py | no se corrió: es de cánones (completitud/chequeos_biblioteca) y está fuera del alcance de este delta |
| /tmp/verif12/adv12_delta.py (nuevo, 34 casos) | salida en /tmp/verif12/run_adv12.txt. El contador marca 13 "REGRESION" por cualquier PASS; clasificados arriba: reales W1, D1 y D2; O1-O3 son observaciones; el resto es PASS legítimo |
