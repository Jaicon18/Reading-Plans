# adv8_cf04: CB_BE_CF04 be_cf04 — v137 vs candidato
import sys; sys.path.insert(0, sys.argv[1]); import chequeos_biblioteca as CB
def r(**w):
    base = {"id": "W-01", "stud_size": "3-5/8\"", "gauge": "20"}; base.update(w)
    x = CB.be_cf04(CB.B(canon={"walls": [base]})); return x[0], str(x[1:])[:110]
casos = [
 ("M0 control metal", {}),
 ("(b) stud_size 'lumber 2-by-6'", {"stud_size": "5-1/2\" lumber (2-by-6)", "gauge": "n/a"}),
 ("(b) stud_size 'Hem-Fir 2 by 6'", {"stud_size": "Hem-Fir 2 by 6", "gauge": "#2"}),
 ("(b) stud_size 'SYP 5-1/2\"'", {"stud_size": "SYP 5-1/2\"", "gauge": "-"}),
 ("(b) stud_size 'LVL'", {"stud_size": "1-3/4\" LVL", "gauge": "-"}),
 ("(b) 'framing' con madera y 'excluded' de otra cosa", {"framing": "2x6 DF studs @ 16\" o.c.; insulation excluded"}),
 ("(c) metal con 'framing' que menciona blocking de madera", {"framing": "3-5/8\" 20 ga @ 16\" o.c. w/ 2x6 wood blocking at casework"}),
 ("(c) metal con gauge '20 ga (2 x 4 blocking by GC)'", {"gauge": "20 ga (2 x 4 blocking by GC)"}),
 ("(c) metal 'SPF' no aparece; stud_size '6\" 16 ga' con framing dict {'type':'CFMF'}", {"stud_size": "6\"", "gauge": "16", "framing": {"type": "CFMF"}}),
 ("(a) v137 marcaba '2x6' en gauge", {"gauge": "2x6"}),
 ("(a) v137 marcaba 'wood' en gauge", {"gauge": "wood"}),
]
for n, w in casos: print(n, "->", r(**w))
