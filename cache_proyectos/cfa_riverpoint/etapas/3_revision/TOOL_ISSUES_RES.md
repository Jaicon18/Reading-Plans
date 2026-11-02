# TOOL_ISSUES — resolver (CFA #2284)

1. Same as A/B: no 6" joist system in `ceilings[]` -> S-241 dropped ceilings stay in misc_items (6" stud / 6" track / 5/8" board / bridging as 'bracing C.R. channel'). Data not bent.
2. M2.1 2" Z channel reports under family '1-1/2" Z-furring' (F_ZF label hard-coded); LF 96.0 is right.
3. No '8" track' family: the pin & sleeve recess head/sill runners (8") are loaded as 'sill track' (8.0 LF). M3.5 walls with stud_size 8" get their runners in the generic bottom/top track families.
4. demo_geom is not validated by canon.py; its lf/h/sf were kept equal to the DEMO-* misc_items.
5. rfis[] has no schema check; added 'status' (closed - estimator decision option A / open - conservative value loaded) per R-ALC-10/11.
