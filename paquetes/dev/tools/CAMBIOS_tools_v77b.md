# CAMBIOS tools v77b

- canon.py `_atm_wall`: el extra framing del ATM = la partición interior que contiene el ATM de lobby (studs_nodos +
  bottom + top runner de corridas), sin restar de las familias de stud / track; atm_recess en wall exterior = error;
  la wall exige `to_deck: true`; deja `rfi_una_vez` con el delta de contarla una sola vez.
- accesorios.py: suma la wall de `_atm_wall` y emite el RFI "counted once"; mensajes v77b.
- chequeos_v72.py R72.11: atm_recess en una wall exterior (tag EXT*, location exterior) = falla.
- chequeos_v77.py `r77_10`: R.O. de una door fuera del largo del wall (band + xy_pt) = falla.
- reglas.py A_TRACK_RUNS: sin el salto `moved_to`; comentario del rótulo F.R.T. sin N/HOJA de un set.
- reglas_clasificacion.py: R77.10 en vigencia.
- test_v77.py (D1 v77b, R77.10) y test_v72.py (R72.11 v77b) actualizados.
