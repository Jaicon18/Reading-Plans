# Reader A — task A-GEN (general canon: everything that is not a wall of an enlarged / overall plan)

Read BRIEF_COMUN.md and BRIEF_A_EXTRA.md first. Output: `/tmp/chuze/work/etapas/2_lectura/A/general.json` (no "walls"
key unless you find an element that no plan task covers — then declare it with element per SKILL §5).

Sheets to read COMPLETELY: G001, G002, G003, G004, G005, AD101, AD102, AD103, A000.A, A000.B, A001, A002, A010, A102,
A103, A111, A121, A131, A201, A301, A501, A502, A503–A503.C (blocking only), A504, A505.A, A505.B, A506, A601, A602,
A610, A611, S100, S101, S200, S300, and the enlarged RCPs (A421.A, A422.A, A423.A, A424.A, A425.A, A427, A428, A429,
A431, A435) for ceilings / soffits. Specs (Project Manual) sections 05 40 00 / 09 21 16 / 09 22 16 / 09 29 00 for
gauges, O.C., deflection track, control joints, finish levels.

Write these keys (SKILL §4 schema; every number with source):
- `details`: one entry per N/SHEET opened, e.g. "INTERIOR PARTITION TYPE A/A301", "HEAD DETAIL (D)/A301",
  "BASE DETAIL (V)/A301", "B/S200": {source, title, layers_per_face, layers_source, board, stud_size, oc_in, gauge,
  notes, sealant_none_reason: "acoustical sealant EXCLUDED (estimator standing order)"}. Include EVERY type of the
  A301 schedule tables (A2-3D, A3C, A6C, A6D, B2E, C3C, C3D, C3G, D3F, D3G, D6F, D6G, X6D) with stud size, insulation
  (EXCLUDED), head detail, sill detail, fire rating, and what each type is (interior / furring at existing exterior /
  tube steel low wall support / 1 HR).
- `types_none_reason`: schedule types that appear on no plan (with the sheets swept).
- `ceilings[]`: every GYP BD ceiling, soffit, bulkhead and framed ceiling element (room, system per its detail, area_sf,
  perimeter_ft, height_ft, board, detail + source). ACT is EXCLUDED (list only as note). A502 soffit / ceiling details.
- `deck_breaks` or `deck_breaks_none_reason` (S300 / sections: one B.O. deck height or zones?) and the B.O. deck /
  B.O. joist height(s) with source — walls with head D/E go to structure.
- `deflection_clips`: head details B, D, E show 2" slip track → {note_source, slip_track_source} or none_reason.
- `misc_items[]`: members and fasteners printed by details: S200 (600T250-54 track, #10 TEK, #12-24 TEK, Hilti X-U
  PAF @ 16" per bottom track anchorage schedule), A131 600S162-33 stud frame @ 12" O.C. (RTU / signage), etc.
- `access_panels[]` (A131 24"x24" signage access panel where required; RCP markers on GWB), `level5_tags` (A610 / A611
  finish schedule: any Level 5 / special finish), `trim_items[]` (corner bead, J-metal / L-bead at ACT and GWB edges
  ("J-METAL EDGE TRIM" head A, "METAL EDGE" head F), control joints: A101 general note 27 "control joints in gypsum
  board at all runs over 30'-0"" → record as trim rule with source).
- `blocking_items[]` from A103 / G002 / A010 notes / millwork details: label literal; wood → EXCLUDED note; metal →
  quantity with source.
- `tile_base` / `frp` / `edge_blocking`: none reasons (FRP and tile are other trades) with N/SHEET.
- `accesorios_none[]` and `accesorios_rfi[]` per SKILL §12 where the plan gives no data.
- `mep_sweep`: {sheets: [M110, M401, M402, P110, P111, P401, P402, E111 ...], registro: "...", source} — ducts / fire
  dampers crossing GWB walls (count, wall, xy) or explicit 0 + reason.
- `scope_notes[]`: every general note / keynote that touches framing or drywall with its destination:
  "QUANTIFIED in <key>", "EXCLUDED - <reason>", or "RFI" (this feeds the Scope Checklist and the step-12 coverage).
- `rfis[]`: SKILL R80e.50 format {id, question, options {A: {texto, source, delta}, B: {texto, cita, delta}, C: ""}} —
  do NOT stop to ask; load the conservative assumption and write the RFI.
- `demo_summary`: AD101 / AD102 / AD103: what is removed (walls, furring, ceilings) and what remains, with keynotes.
