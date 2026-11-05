set -e
cd /root/cc/work/proposal
python3 armar_proposal.py tpl/Proposal_Template.xlsx /root/cc/work/etapas/8_excel/Consumer_Cellular_Centennial_Takeoff_FINAL_rev4.xlsx /root/cc/work/etapas/4_canon/takeoff_canon.json fbm out/Consumer_Cellular_Centennial_Proposal_rev4.xlsx
cd out && rm -rf recalc && mkdir recalc && timeout 180 soffice --headless --calc --convert-to xlsx --outdir recalc Consumer_Cellular_Centennial_Proposal_rev4.xlsx >/dev/null 2>&1
python3 - <<'PY'
import openpyxl
wb=openpyxl.load_workbook('recalc/Consumer_Cellular_Centennial_Proposal_rev4.xlsx',data_only=True)
for n in ('PRICING','FBM_PRICES'): wb.remove(wb[n])
ws=wb['PROPOSAL']; ws.page_setup.fitToWidth=1; ws.page_setup.fitToHeight=0; ws.sheet_properties.pageSetUpPr.fitToPage=True
wb.save('pdf_src.xlsx')
PY
rm -f pdf_src.pdf; timeout 180 soffice --headless --convert-to pdf pdf_src.xlsx >/dev/null 2>&1; mv pdf_src.pdf Consumer_Cellular_Centennial_Proposal_rev4_PROPOSAL.pdf
python3 -c "
import pymupdf as f;d=f.open('Consumer_Cellular_Centennial_Proposal_rev4_PROPOSAL.pdf');print('pages',d.page_count)
for i,p in enumerate(d): p.get_pixmap(dpi=60).save(f'/tmp/claude-0/-home-user/d2b6b434-1017-52fc-8c0e-204720c3b7f4/scratchpad/prop_{i}.png')"
