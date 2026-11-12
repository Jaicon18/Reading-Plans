# v81cf114 APARTADA (NO publicada: versiones congeladas por orden de COORDINACIÓN, 12-nov)

Base: v81cf113 (skills_archivo/take-off-metal-frame-drywall_v81cf113_U192-tasas-proposal_2026-11-12.zip).
Aplicar: descomprimir v81cf113 en /tmp/v114 y `patch -p1 -d /tmp/v114/take-off-metal-frame-drywall < v81cf114_desde_v81cf113.patch`.

Contenido (auditoría U-138 del 12-nov, BE-AUD05..09):
- (a) BE-AUD05 CB_U_191_REF: chequeos_biblioteca.falta_cita_u191 — listing UL ('L546' suelto o 'UL Lxxx') exige 'Item N'; en RC / furring /
  channel además 'N in. o.c.'; revisa también la fuente del Material Summary.
- (b) BE-AUD06 CB_RCP_APILADOS: rcp_tags o DOBLE_CIELO.csv con filas y 0 cuartos evaluados = FAIL (DOBLE_CIELO.csv entra a b.textos).
- (c) BE-AUD07 CE_RCP_COMPLETO: esperados vacío + cielo / soffit en el Excel (cielos_en_excel) o contornos RCP (contar_contornos_rcp) = FAIL
  (AMBER en entregas subidas antes de FECHA_V114).
- (d) BE-AUD08 CE_RESUMEN_EXCEL (nuevo): tablas de material de RESUMEN_revN.md / BITACORA_revN.md (rev más alta), columna 'revN' o
  Net / Total = Material Summary del Excel (+-0.01); deltas y revs viejas no se comparan.
- (e) BE-AUD09 CE_VERSION_ENTREGA (nuevo) + arreglo de _skill_version: lee '**VERSION: v81cfNNN**' (arriba de SKILL.md) en vez de la
  primera 'v81cf' del archivo (era la causa de 'v101' en ENTREGA_OK de GK rev3); FAIL si la línea VERSION es más vieja que lo que cita
  SKILL.md o si LEEME / README / TIEMPOS declaran otra versión de compuerta.
- Fechas: CB_RCP_APILADOS y CB_U_191_REF pasan a FECHA_V114 en U189_CB (lo endurecido no re-abre entregas ya subidas).
- Registro: BE-AUD05..09 (programa) + BE-GK49 unido. SKILL.md: línea VERSION + párrafo BE-AUD05..09. ORDENES: U-177 ampliación.
- AL PUBLICAR: subir la línea '**VERSION: v81cfNNN**' de SKILL.md a la versión que se publica (si se renumera).

Pruebas del candidato (12-nov): suite 47/47, banco 0 distintas en 8 proyectos (v113 vs v114), reglas.py 0 sin clasificar, 199 archivos,
verificar_version OK. Xfinity rev1b, CE_RCP_COMPLETO: v113 PASS 'N/A sin cielos'; v114 FAIL (4 renglones del Material Summary con
SOF-01 + 1 contorno RCP).
