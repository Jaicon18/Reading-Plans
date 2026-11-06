#!/bin/bash
# CR City Hotel proposal (U-150): re-run whenever the take-off quantities change.
set -e
W=/root/cr/work
P=$W/proposal
OUT=$W/Proposal
TK=$W/etapas/8_excel/CR_City_Hotel_Takeoff_FINAL_rev1.xlsx
N=CR_City_Hotel_Proposal_rev1
mkdir -p $P/out $OUT
cd $P
python3 armar_proposal.py tpl/Proposal_Template.xlsx $TK $W/etapas/4_canon/takeoff_canon.json fbm out/$N.xlsx
cd out && rm -rf recalc && mkdir recalc
# recalculate with LibreOffice (formulas kept, cached values written)
timeout 180 soffice --headless --calc --convert-to xlsx --outdir recalc $N.xlsx >/dev/null 2>&1
cp recalc/$N.xlsx $OUT/$N.xlsx
python3 - "$N" <<'PY'
import sys, openpyxl
n = sys.argv[1]
wb = openpyxl.load_workbook(f'recalc/{n}.xlsx', data_only=True)
for s in ('PRICING', 'FBM_PRICES'):
    wb.remove(wb[s])
ws = wb['PROPOSAL']; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
wb.save('pdf_src.xlsx')
PY
rm -f pdf_src.pdf; timeout 180 soffice --headless --convert-to pdf pdf_src.xlsx >/dev/null 2>&1
mv pdf_src.pdf $OUT/${N}_PROPOSAL.pdf
python3 -c "
import pymupdf as f; d=f.open('$OUT/${N}_PROPOSAL.pdf'); print('PDF pages', d.page_count)
for i,p in enumerate(d): p.get_pixmap(dpi=80).save(f'$P/out/prop_{i}.png')"
# gate U-150 (same call as ce_proposal in compuerta_entrega.py)
python3 - "$OUT/$N.xlsx" "$TK" <<'PY'
import sys, openpyxl
sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import compuerta_entrega as ce
x, tk = sys.argv[1:3]
wb = openpyxl.load_workbook(tk, data_only=True)
ms = [(str(r[0]), r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
sc = [r for r in wb["Scope Checklist"].iter_rows(min_row=2, values_only=True) if r and r[0]]
ev = ce.revisar_proposal(x, ms, sc)
print("revisar_proposal:", len(ev), "faltas"); [print("  -", e) for e in ev]
wb2 = openpyxl.load_workbook(x, data_only=True)
B = wb2['PRICING']
for row in B.iter_rows(values_only=True):
    if row and str(row[0] or '').startswith(('Material total', 'Labor total', 'General conditions', 'OH 12% +', 'Total all', 'Taxes', 'Total including')):
        print(f"  {row[0][:60]:60s} {row[1]:>14,.2f}")
sys.exit(1 if ev else 0)
PY
