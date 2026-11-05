# BUBBLE VERIFICATION BRIEF (rules U-113 / U-137 / U-141) — CR City Hotel

PDF: /root/cr/work/plans/bidset_SIN_MARKUPS.pdf (148 p, rotation 0, page 2592 x 1728 pt; coordinates = page pt).
Python: python3 -I -W ignore, import fitz (PyMuPDF), PIL.
Detector output to verify: /root/cr/work/etapas/1_inventario/inventario.json → ocurrencias.detail_bubble (617, each with
sheet, page, center_pt, ref "N/SHEET") and /root/cr/work/set_texto.json → burbujas[<sheet>] (rings / indep counts).
Sheet → page map: inventario.json "sheets" (page, sheet). Pages with NO text (45-48, 50-52, 54-56, 58-59, 61-63, 73-74)
must be swept VISUALLY (render dpi 100-150, look for section / detail / elevation bubbles = circle with a divider line,
number ABOVE, sheet BELOW).

Task for YOUR sheet group: for every sheet, (1) verify each detector bubble by eye on a rendered crop (it is a real
bubble → keep {x, y, n, hoja, img, dibujo (what it points at / where)}; not a bubble → {x, y, img, no_es_burbuja: why});
(2) sweep the sheet by eye for bubbles the detector missed (add them with "ojo": true); (3) for every DISTINCT target
N/SHEET, open the destination sheet, find the detail / section / elevation titled N, record its position and title in
_destinos {"N/SHEET": {detalle_existe: true|false, x, y, x1, y1, img, title}} and list the bubbles INSIDE that
destination detail that point further (follow the chain to the end, also if the further target is outside your group);
(4) write what each chain governs for METAL FRAMING / GYPSUM BOARD (board layers, shaft wall, J-track, resilient
channel, deflection, control joint, soffit framing, blocking (wood = excluded), fire-rated intersections...) or
"not our trade: why".
Make contact sheets: images with numbered red circles (#0, #1 ...) so each entry's img = "img_verif/<file>.png #k".

Output (folder /root/cr/work/burbujas/{GRUPO}/, write before finishing):
- burbujas_verificadas.json = {"_nota": "...", "_frame": "page pt, rotation 0", "<SHEET>": [entries], ...,
  "_destinos": {...}}
- CADENA.md (English or Spanish, numbered: origin bubble → destination → bubbles inside → what it governs)
- callouts_no_aplican.json = {"<destination sheet>": {"<detail n>": "reason it is not our trade"}}
- img_verif/*.png
Final message: under 120 words (bubbles verified / rejected / added by eye per sheet, destinations found / missing).
