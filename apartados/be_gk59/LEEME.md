# BE-GK59: check, helper and test (for Xfinity, v131)

Error (Grand Kia rev3b, 13-nov): the gate rewrites `<workdir>/ENTREGA_OK.json` on EVERY run.
- rev3b was uploaded with the VERDE from v81cf129 (run 60914f5fc798).
- It was later re-run with v81cf130 (run 7819a4ce749e). That run came out ROJA because of the run count, and it overwrote the local ENTREGA_OK.
- The VERDE that was actually delivered survived only in `compuerta_corridas.jsonl`.

Rule:
- Every gate run also keeps `ENTREGA_OK_<corrida>.json`, which is never overwritten.
- Once `SUBIDA_OK.json` exists, `ENTREGA_OK.json` stays as the one from the uploaded run.
- Any run after the upload writes only its own `ENTREGA_OK_<corrida>.json`.

Files:
- `be_gk59.py::guardar(w, corrida)`: the gate calls it when it writes ENTREGA_OK.
- `be_gk59.py::fallas(w)`: the check. CLI: `python3 be_gk59.py <workdir>`.
- `test_be_gk59.py`: the real case.
  - Run kept + current ENTREGA_OK is the uploaded run's = PASS.
  - Overwritten after the upload = FAIL.
  - ENTREGA_OK of the uploaded run missing = FAIL.

On the real GK rev3b: FAIL, as expected; this is the case that motivated the rule.
