#!/bin/bash
# SessionStart: recuerda las órdenes del usuario y verifica que la versión vigente del skill
# contenga TODAS las reglas acumuladas (BE-115). No modifica nada.
cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0
echo "OBLIGATORIO: cargar el skill jc-hunter-ordenes (.claude/skills/jc-hunter-ordenes) y leer ORDENES_DEL_USUARIO.md antes de cualquier take-off."
V=$(grep -oE 'VERSIÓN VIGENTE[^:]*: [^(]*\(hoy (v[0-9a-z]+)' skills_archivo/INDICE.md | grep -oE 'v[0-9]+[a-z0-9]*$' | tail -1)
Z=$(ls -t skills_archivo/take-off-metal-frame-drywall_${V}_*.zip 2>/dev/null | head -1)
if [ -n "$Z" ]; then
  echo "Versión vigente del skill de take-off: $V ($Z)"
  python3 -I .claude/skills/jc-hunter-ordenes/verificar_version.py "$Z" skills_archivo cache_proyectos 2>&1 | head -2 | cut -c1-400
  echo "Si faltan reglas: NO arrancar un proyecto nuevo hasta unirlas (BE-115)."
fi
exit 0
