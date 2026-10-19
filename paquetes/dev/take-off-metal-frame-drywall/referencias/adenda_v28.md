# ADENDA v28 — 28-sep-2026 · la compuerta de COBERTURA

## De dónde salió

Rodolfo preguntó por qué dos walls G idénticos tenían distinto número de studs. **No era error** — pero revisando para contestarle apareció un hueco de verdad.

## No era error: los studs de abertura

| | wall A | wall B |
|---|---|---|
| length | [valor retirado E24] LF | idéntico |
| height · O.C. · rows | [valor retirado E24] · 16" · 2 | idénticos |
| campo `(floor([valor retirado E24]×12/16)+1) × 2` | [valor retirado E24] | [valor retirado E24] |
| terminación (2 extremos × 2 rows) | 4 | 4 |
| **studs de abertura enmarcada de MEP** | **0** | **[valor retirado E24]** |
| **total** | **[valor retirado E24]** | **[valor retirado E24]** |

El wall B tiene **[valor retirado E24] penetraciones** de ducto en M01.01, cada una con dos studs por row: penetraciones × 2 × rows.

El wall A tuvo **un solo impacto y fue descartado con motivo**: en E02.01 el rótulo a 17 pt es `OS` con su `A` — un occupancy sensor montado en el wall, no una penetración. Una línea de lineweight bajo que muere en la face no atraviesa nada.

El gyp es idéntico y está bien: [valor retirado E24] × [valor retirado E24] × 2 layers = **[valor retirado E24] SF por face** en los dos. Los huecos de ducto (de área despreciable) no se deducen — está declarado en el cierre del cruce MEP, no escondido.

**REGLA:** antes de dudar de dos elementos iguales con distinto conteo, comparar **campo / terminación / studs por separado**. La diferencia casi siempre está en un solo sumando, y ese sumando tiene nombre.

## El hueco de verdad

`cruzar_mep.py` hacía:

```python
if ori == 'D':
    continue
```

El wall **40** —el inclinado a 30° entre el 24 HR VESTIBULE [room] y el ATM ROOM [room], [valor retirado E24] LF— se saltaba **en silencio**. No aparecía ni en la lista de "con penetración", ni en la de "sin penetración", ni en la de falsos positivos.

**Nunca se evaluó, y nada lo decía.** Los sellos verificaban, las cantidades cuadraban, la auditoría adversarial no lo vio.

## REGLA — Un elemento que no aparece en ninguna lista no es "sin nada": es SIN REVISAR

**Todo cruce, barrido o clasificación por lista termina con una compuerta de cobertura que exige que cada elemento del universo esté en EXACTAMENTE UNA de las listas. Si alguno no está en ninguna, el cierre no se emite.**

Y el cierre guarda la frase de cobertura, para que se vea de un vistazo:

> *los [valor retirado E24] walls del proyecto están cubiertos: [valor retirado E24] con penetración, [valor retirado E24] declarados sin penetración, [valor retirado E24] con falso positivo descartado*

## REGLA — Un `continue` por tipo de geometría es una bomba

Si una herramienta no sabe tratar un caso —banda diagonal, caja, elemento curvo— tiene que **fallar o registrarlo como pendiente**. Nunca saltárselo callada.

Un `continue` no deja rastro: ni en el resultado, ni en el log, ni en el sello. Es la única clase de error que ninguna verificación de cantidad puede encontrar, porque la cantidad que falta **no existe en ningún lado para compararla**.

## Cómo se cerró

`cruzar_diagonal.py` cruza el wall inclinado aplicando el **MISMO criterio** que `mep.cruces`, no uno inventado:

1. lineweight ≥ 0.5
2. la línea tiene que **atravesar** el wall y sobresalir 3.0 pt por los **dos** lados (una línea que muere en la face no penetra nada)
3. si la misma línea existe en la arquitectónica, es fondo copiado
4. las paralelas muy juntas se agrupan: un ducto viene en pareja y la separación **es** el width del ducto

**Resultado: cero penetraciones.** Las 5 líneas que cortan el eje en crudo se descartan una por una — dos de lw 0.24 (leaders de rótulo, por debajo del mínimo) y tres de lw 0.72 que son ejes de grid del fondo.

**El hueco del proceso era real; la cantidad no se movió.** Las dos cosas se reportan. Que no haya cambiado nada no convierte el hueco en un no-problema: la próxima vez puede tocarle a un wall con tres ducts.

## Probado viéndolo fallar

Quitando el wall 40 de la lista, el cierre se niega:

```
CRUCE MEP INCOMPLETO: los muros [40] no estan ni en PEN, ni en SIN_PEN, ni en FALSOS.
Un muro que no aparece en ninguna lista no es un muro sin penetraciones: es un muro
sin revisar. No se emitio nada.
```

---
