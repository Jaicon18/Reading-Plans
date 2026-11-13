import sys, os; sys.path.insert(0, "/tmp/v139p/take-off-metal-frame-drywall/tools"); import compuerta_entrega as CE
for n in ("W2_vp_rev22", "W2c_control", "X1_linea_dos_tablas"):
    w = "/tmp/verif13/tmp/a13/" + n; e = os.path.join(w, "rev21 FINAL PARA REVISAR"); p = CE._tiempos_log(w); ms = CE.marcas_tiempos_log(p)
    k0 = CE._k0_rev(ms, w, e, p); ini, pr = CE.inicio_rev_info(w, e); d = CE.arranque_rev_desde(w, e, ini)
    prev, tope, idx = CE.marcas_rev_anterior(w, e, con_tope=True, desde=d)
    print(n, "etiqueta=", CE._etiqueta_rev(w, e), "k0=", k0, "et=", CE._rev_actual_proyecto(w, ms, k0), "desde=", d, "tope=", tope, "idx=", idx)
    if n.startswith("X1"):
        tt = open(os.path.join(w, "_TIEMPOS.md")).read(); t2, nn = CE.tiempos_desde(tt, d, prev, tope); print("  filtrado:\n" + t2)
