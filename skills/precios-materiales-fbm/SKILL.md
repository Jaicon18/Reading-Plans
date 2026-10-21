---
name: "precios-materiales-fbm"
description: "Extraer la lista de precios de FBM (myfbm.com) para metal frame, gypsum board y todos sus accesorios (trims, taping, tornillería, pines), verificada y en Excel."
---

# Lista de precios FBM — Metal Frame, Gypsum Board y accesorios

Fuente: https://myfbm.com (Foundation Building Materials). Sucursal por defecto: **Denver, CO (86)**, salvo que el usuario diga otra.
La exactitud manda: ningún precio se lee a ojo ni se reescribe a mano.

## ALCANCE (no interpretarlo de forma estrecha)
"Metal frame y gypsum board con sus accesorios" SIEMPRE significa todo lo que se necesita para instalar y terminar:

| Bloque | Categorías FBM (código /c/) |
|---|---|
| Metal Frame | SteelFraming (completa: Interior, Exterior estructural, Steel Framing Accessories, Clips & Connectors) |
| Gypsum Board | Drywall (completa) |
| Trims | DrywallBead (completa: vinyl, paper-faced, metal, expansion joint, reveal, trim adhesives) |
| Taping | JointCompound, DrywallTape, DrywallAccessories, DrywallPatch |
| Tornillería | DrywallScrews, FramingScrews |
| Fijación de track | PowderActuated, GasFasteningSystem (pines/cargas; marcar herramientas vs consumibles) |

Fuera de alcance salvo que lo pida: texture, adhesives & bonders, caulking/sealants, access doors, anchors, firestop, insulation, ceilings.
ERROR PASADO (2026-09-29): se entregó solo SteelFraming + Drywall y quedaron fuera corner bead, taping y tornillería. No repetir.

## PASOS (en orden, sin saltarse ninguno)

1. **Abrir myfbm.com en el navegador integrado** y fijar la sucursal (banner "Find my branch" → Branch Selector → Save). Confirmar que el header dice la sucursal correcta.
2. **Fuente de datos:** las páginas de categoría `/all-products/x/c/<CODIGO>?sort=name-asc&page=N` traen el JSON de productos embebido en `self.__next_f.push([1,"..."])`. Concatenar esos strings (JSON.parse de cada literal) y extraer por conteo de llaves los bloques `"pagination":{` y `"products":[`. pageSize fijo = 16.
3. **Extraer** en un loop asíncrono en segundo plano (window.__x), con 3 reintentos por página. Campos: code, name, brandName, manufactureId, productCategory, isBaseProduct, price.value, unitLabel, specialPrice.value, specialPriceUnit, stockLevelStatus, specialMessage, minOrderQuantity, url.
4. **Sacar los datos al workspace sin reescribirlos:** devolver el TSV completo desde javascript_tool; al exceder el límite se guarda solo en tool-results/*.txt → leerlo con python (json.load, luego json.JSONDecoder().raw_decode del texto).
5. **Verificar (obligatorio, todo documentado en la hoja Resumen):**
   - Conteo: filas extraídas = totalResults de cada categoría, sin códigos duplicados, todos con precio.
   - Doble lectura: segunda pasada completa; 0 diferencias de precio.
   - Coherencia por longitud: productos BASE_ (studs/track por largo) → price = $/MLF ÷ 100 (pieza de 10 ft). Piezas de largo fijo → price = $/MLF ÷ 1000 × largo (tolerancia $0.01).
   - Coherencia hojas: price/hoja = $/MSF ÷ 1000 × SF. Parsear ancho×largo buscando primero el patrón `N ft x N ft [N in]` (NO confundir el espesor `5/8 in. x` con el ancho).
   - En vivo: abrir una muestra al azar de páginas de producto y leer el precio del bloque principal (el primer precio; los siguientes suelen ser de productos relacionados).
6. **Excel** (skill xlsx): hoja Resumen y verificación + una hoja por bloque. Azul = dato de FBM, negro = fórmula, amarillo = input. Studs/track por longitud: $/MLF, $/LF (=MLF/1000), pieza 10 ft, columna amarilla "Longitud deseada" → precio de pieza. Incluir mínimo de pedido, stock, entrega estimada y link `https://myfbm.com/all-products/x/p/<code>`. Correr recalc.py → 0 errores.

## DATOS DE FBM A RECORDAR
- Precio mostrado = precio de visitante de la sucursal; el de cuenta de contratista puede ser distinto. Decirlo siempre.
- FBM cobra el mismo $/MLF para cualquier largo de stud/track.
- Muchos clips/tornillos exigen mínimo o múltiplo de pedido (ej. RCA en múltiplos de 75).
- El sitio a veces responde "Failed to fetch" en una página: reintentar, nunca aceptar huecos.