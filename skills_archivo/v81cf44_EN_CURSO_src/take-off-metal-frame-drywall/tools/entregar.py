# -*- coding: utf-8 -*-
"""entregar.py -- UNICA puerta de salida del entregable.

Regla que impone (orden de Rodolfo, 2026-09-28):
    "cada vez que halla cambios el excel sheet se tiene que actualizar tambien".

Por que existe este archivo y no solo la regla escrita:
    Una regla escrita se olvida a las 2 de la manana. Aqui regenerar y entregar son EL
    MISMO ACTO: no hay forma de copiar el libro a la carpeta de entrega sin haberlo
    regenerado primero, porque la copia ocurre despues de la compuerta de vigencia y no
    hay otra ruta. Si un cierre cambio, este script lo detecta, regenera, y solo entonces
    copia. Si algo no cuadra, NO copia y dice exactamente que.

Secuencia (no se puede saltar ningun paso):
    1. resumen_total  -> todos los sellos intactos. Un sello roto para todo aqui.
    2. verif_planos   -> el LF ROTULADO en cada plano marcado contra su cierre sellado.
    3. excel.main()   -> regenera, recalcula, audita el libro y sella el manifiesto.
    4. verif_vigencia -> prueba por hash que el .xlsx refleja TODOS los insumos de hoy.
    5. hoja_estado    -> reescribe <PREFIJO>_ESTADO.md LEYENDO el libro (no a mano: se quedaba
                         viejo por la misma razon que el Excel).
    6. hoja_rfi       -> la carta de RFIs, leida de Pending Items.
    7. hoja_detalles  -> el registro de cobertura de detalles, leido de la compuerta
                         verif_detalles. Va aqui y no a mano por la misma razon que el
                         estado: un documento que se escribe a mano se queda viejo y
                         miente. Si se abre un detalle, este documento cambia solo.
   7b. markups (v78, W3) -> el PDF de markups Bluebeam (markups_bluebeam.py) verificado contra el canon
                         vigente; sin el, no se entrega. Viaja a la carpeta de entrega junto al libro.
    8. copia a /mnt/user-data/outputs/entrega/: el libro, su manifiesto Y los scripts.
                         Los scripts se sincronizan aqui y no a mano porque un script que
                         produce un numero y no viaja con el entregable vuelve el trabajo
                         irreproducible.
    9. hoja_indice    -> 00_INDICE_DE_ARCHIVOS.md CONTANDO la carpeta ya poblada. Por eso
                         va despues de la copia: lista lo que hay, no lo que yo creo que
                         hay. Estaba escrito a mano y decia <n> elementos cuando eran <n>,
                         <n> scripts cuando eran <n>, y que la carta de RFIs no existia
                         cuando ya existia.
   11. verif_confirmado -> todo [CONFIRMADO] vale la COTA IMPRESA que cita, no la medicion
                         por pixeles. Una cuenta sobre una cota es [DERIVADO].
   12. verif_caras   -> el room que nombra cada face es uno de los que nombra la ubicacion
                         del wall. Cuando no coinciden hay que ir al plano: ninguno de los
                         dos lados manda por si solo.
   13. verif_reproducible -> cada closer todavia puede volver a generar su cierre. Un sello
                         OK no prueba que el cierre se pueda regenerar, y un cierre que no se
                         puede regenerar no esta verificado: esta congelado.
   14. verif_motivos -> ningun eslabon de ninguna cadena sin motivo declarado y sin dato
                         rastreable en el cierre. Una secuencia que solo trae numeros dice
                         por donde paso la lectura, no que aporto cada paso.
   15. verif_idioma   -> ningun nombre de material en espanol, en los archivos FINALES.
                         Va al final: revisa TODO lo que acaba de escribirse, indice
                         incluido.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, glob, shutil, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verif_vigencia as VV

B = f'{_TW}'
ENTREGA = f'{_TO}/entrega'


def main():
    print('=' * 72)
    print('1/23  SELLOS')
    r = subprocess.run(['python3', B + '/tools/resumen_total.py'],
                       capture_output=True, text=True)
    # Se busca el renglon de sellos POR SU CONTENIDO, no por ser el ultimo: resumen_total
    # sigue imprimiendo materiales despues del TOTAL y tomar la ultima linea daba un
    # falso "sello roto" (error visto 2026-09-28).
    lin = [l for l in (r.stdout or '').splitlines() if 'sellos OK' in l]
    if not lin:
        print('    ' + (r.stderr or r.stdout or '').strip()[-300:])
        print('\n*** resumen_total no reporto sellos: no se regenera ni se entrega nada.')
        return 1
    print('    ' + lin[-1].strip())
    if '/ 0 rotos' not in lin[-1]:
        print('\n*** SELLO ROTO: no se regenera ni se entrega nada.')
        return 1

    print('2/23  PLANOS MARCADOS (el LF rotulado contra el cierre sellado)')
    import verif_planos as VP
    fp = VP.verificar()
    if fp:
        print('\n*** LOS PLANOS MARCADOS NO CUADRAN CON LOS CIERRES -- NO SE ENTREGA:')
        for f in fp:
            print('    -', f)
        return 1
    import resumen_global as _RG0
    print('    OK: the %d sealed walls are marked and their LF matches the closure'
          % len(VP.sellados()))

    print('3/23  REGENERANDO EL EXCEL (siempre, aunque "no haya cambiado nada")')
    import excel
    out = excel.main()

    print('4/23  VIGENCIA')
    fallas = VV.verificar(out)
    if fallas:
        print('\n*** EL LIBRO SIGUE SIN REFLEJAR LOS INSUMOS -- NO SE ENTREGA:')
        for f in fallas:
            print('    -', f)
        return 1
    print('    OK: el .xlsx es el estado sellado de hoy, probado por hash')

    print('5/23  ESTADO (se regenera del libro, nunca a mano)')
    import hoja_estado
    hoja_estado.main(out)

    print('6/23  CARTA DE RFIs (se genera de Pending Items, nunca a mano)')
    import hoja_rfi
    hoja_rfi.main(out)

    print('7/23  COBERTURA DE DETALLES (se genera de la compuerta, nunca a mano)')
    import hoja_detalles
    hoja_detalles.main()

    print('8/23  CALLOUTS (el detalle que el plano SENALA se usa, siempre)')
    import verif_callouts as VC
    fc, uni, _cit = VC.verificar()
    if fc:
        n = sum(len(x[1]) for x in fc)
        print('\n*** EL PLANO SENALA %d DETALLE(S) QUE NINGUN CIERRE USA NI DECLARA -- '
              'NO SE ENTREGA:' % n)
        for h, sin, _c in fc:
            print('    - %-8s %s' % (h, ', '.join(sin)))
        print('    Regla inviolable de Rodolfo (2-oct-2026): si el plano pone una burbuja '
              'sobre un elemento, ESE detalle es su fuente. Abrirlo y citarlo, o declararlo '
              'en verif_callouts.NO_APLICAN con su motivo.')
        return 1
    print('    OK: las %d burbujas de las hojas de planta estan usadas o declaradas'
          % sum(len(v) for v in uni.values()))

    print('9/23  CITAS QUE EXISTEN (todo N/HOJA que yo escribo existe en esa hoja)')
    import verif_citas as VQ
    malas, real = VQ.verificar()
    if malas:
        print('\n*** CITO DETALLES QUE NO EXISTEN -- NO SE ENTREGA:')
        for c in sorted(malas):
            h = c.split('/')[1]
            print('    - %-12s la hoja %s solo rotula %s'
                  % (c, h, sorted(real.get(VQ.CD.real(h)) or [])))
        return 1
    print('    OK: toda cita apunta a un detalle que la hoja rotula')

    print('10/23 CITAS DEL TEMA CORRECTO (el numero existe Y es el del tema)')
    import verif_tema_cita as VT
    mal = VT.verificar()
    if mal:
        print('\n*** PARTIDAS QUE CITAN UN DETALLE DE OTRO TEMA -- NO SE ENTREGA:')
        for f, m, k, cits, tits in mal:
            print('    - %-24s muro %-4s %-14s %s' % (f, m, k, cits))
            for t in tits:
                print('          titulo citado: %s' % (t or '(sin titulo leido)'))
        print('    Origen: el bracing citaba un detalle que EXISTE pero es de otro tema (framing connections); '
              'el bracing vivía en otro sub-detalle de la misma hoja.')
        return 1
    print('    OK: cada partida cita el detalle de su tema')

    print('11/23 [CONFIRMADO] VALE LA COTA IMPRESA QUE CITA, no la medicion)')
    import verif_confirmado as VCO
    malc = VCO.verificar()
    if malc:
        print('\n*** HAY [CONFIRMADO] QUE NO VALEN SU COTA -- NO SE ENTREGA:')
        for et, r, v, cs, t in malc:
            print('    - %-18s %-24s sellado %-9s cota(s) %s' % (et, r[:24], v, cs))
        print('    Regla #0: [CONFIRMADO] es la COTA IMPRESA; una cuenta sobre ella es '
              '[DERIVADO] y obliga a escribir la operacion. Jerarquia: cota impresa > suma '
              'de cadena > pixeles. Origen (7-oct-2026): un muro citaba una cota impresa '
              'y sellaba la medicion por pixeles redondeada.')
        return 1
    print('    OK: todo [CONFIRMADO] vale exactamente la cota impresa que cita')

    print('12/23 FACES CONTRA UBICACION (el room de cada face es el que dice la ubicacion)')
    import verif_caras as VCA
    malf = VCA.verificar()
    if malf:
        print('\n*** LA UBICACION Y LAS FACES NO COINCIDEN -- NO SE ENTREGA:')
        for et, ub, caras, falta in malf:
            print('    - %-12s %s' % (et, (ub or '')[:62]))
            print('          faces %s  |  ningun face nombra %s' % (caras, falta))
        print('    Ir al PLANO: ninguno de los dos lados manda por si solo. Origen (8-oct-2026): '
              'un muro tenia sus dos faces con el mismo room y una era otro room, con otro ceiling '
              '-- faltaba board. Y en otro era al reves: '
              'ahi las faces tenian razon y la ubicacion no.')
        return 1
    print('    OK: cada face nombra uno de los rooms de su ubicacion')

    print('13/23 CIERRES REPRODUCIBLES (su generador todavia los puede volver a generar)')
    import verif_reproducible as VRP
    # LA PREGUNTA RECIPROCA, primero: ¿cada cierre sellado TIENE un generador? La lista de
    # closers esta escrita a mano, asi que sin esto la compuerta solo mide lo que alguien se
    # acordo de anotar -- y habia <n> walls con cierre sellado y NINGUN
    # generador. Un cierre sin generador no esta congelado: esta HUERFANO.
    hu = VRP.huerfanos()
    print('    cierres HUERFANOS (sellados, sin closer que los produzca): %d bloque(s), '
          '%d walls (tope %d, solo baja)'
          % (len(hu), sum(n for _b, n in hu), VRP.TOPE_HUERFANOS))
    for b, n in hu:
        print('       %-26s %d walls -- falta escribir su closer' % (b, n))
    if len(hu) > VRP.TOPE_HUERFANOS:
        print('\n*** UN CIERRE SIN GENERADOR SOLO SE PUEDE CORREGIR EDITANDO EL JSON A MANO, '
              'QUE NINGUNA REGLA PERMITE -- NO SE ENTREGA.')
        return 1
    norep = VRP.verificar()
    print('    %d de %d closers no pueden regenerar su cierre (tope declarado %d, solo baja)'
          % (len(norep), len(VRP.CLOSERS), VRP.TOPE_NO_REPRODUCIBLES))
    for n, m in norep:
        print('       %-26s %s' % (n, m[:90]))
    if len(norep) > VRP.TOPE_NO_REPRODUCIBLES:
        print('\n*** UN CIERRE QUE NO SE PUEDE REGENERAR NO ESTA VERIFICADO, ESTA CONGELADO '
              '-- NO SE ENTREGA. El sello sigue OK y eso es justo lo que lo hace invisible: '
              'el dia que haya que corregir un dato de ese muro, el generador no corre.')
        return 1

    print('14/23 STUDS ADICIONALES (un extra dice que es, y un criterio por condicion)')
    import verif_studs_adicionales as VSA
    if VSA.main():
        print('    Origen: el detalle estructural de interseccion de walls (N/HOJA). Los dos '
              'studs extra van en el muro PASANTE; el que muere contra el se atornilla y no '
              'lleva stud propio.')
        return 1

    print('15/23 ALCANCE DEL CORPUS (ninguna herramienta puede leer un subconjunto)')
    import corpus as CORP
    _vig, _tod = CORP.cierres(), CORP.cierres(todos=True)
    print('    %d cierres VIGENTES en %d archivos (tope minimo %d); %d en el barrido ancho'
          % (len(_vig), len(CORP.archivos()), CORP.TOPE_CIERRES_MIN, len(_tod)))
    if len(_vig) < CORP.TOPE_CIERRES_MIN:
        print('\n*** EL CORPUS ENCOGIO: %d cierres vigentes contra un minimo de %d.'
              % (len(_vig), CORP.TOPE_CIERRES_MIN))
        print('    Un inventario que no declara su alcance es una muestra, y una muestra')
        print('    parcial no prueba que algo falte: prueba que no estaba donde se miro.')
        print('    Origen: un roll-up de blocking que leia solo una parte de los renglones.')
        return 1
    print('    OK: el corpus no encogio')

    print('16/23 BLOCKING POR TAG DE SCHEDULE (cada tag montado en wall tiene su renglon)')
    import verif_blocking_schedule as VBS
    _f = VBS.faltantes()
    if len(_f) > VBS.TOPE_TAGS_SIN_RENGLON:
        print('\n*** %d TAG(S) DE SCHEDULE SIN PARTIDA DE BLOCKING QUE LOS NOMBRE:' % len(_f))
        for sch, t, n, hay in _f:
            print('    %-34s %-8s %d instancia(s), %d renglon(es)' % (sch, t, n, hay))
        print('    Un schedule es una lista cerrada: si el take-off no tiene un renglon por')
        print('    cada linea, el que falta no se ve. Origen: un tag de millwork huerfano entre')
        print('    varios cierres que lo nombran para decir que no es suyo.')
        return 1
    print('    OK: los %d tags de los schedules declarados tienen su renglon'
          % sum(len(v) for v in VBS.SCHEDULES.values()))

    print('17/23 COHERENCIA DE ETIQUETAS (el mismo dato de la misma hoja, una sola etiqueta)')
    import verif_coherencia as VCO
    inc = VCO.revisar()
    if len(inc) > VCO.TOPE_INCOHERENTES:
        print('\n*** %d DATO(S) CON DOS ETIQUETAS PARA LA MISMA FUENTE -- NO SE ENTREGA:'
              % len(inc))
        for (clase, val, hojas), dd in inc:
            print('    %-22s %-10s hoja(s) %s' % (clase, val, ', '.join(hojas)))
            for e, q in sorted(dd.items()):
                print('        [%s] %s' % (e, ', '.join(q)[:80]))
        print('    Una de las dos esta mal: hay que ABRIR el plano, no elegir la comoda.')
        return 1
    print('    OK: ningun dato de la misma hoja lleva dos etiquetas distintas')

    print('18/23 CADA ESLABON CON MOTIVO Y DATO (la secuencia tiene que ser auditable)')
    import verif_motivos as VMO
    sinm, flojo, sind = VMO.verificar()
    if sinm or flojo or sind:
        print('\n*** HAY ESLABONES DE LA CADENA QUE NADIE PUEDE AUDITAR -- NO SE ENTREGA:')
        for e, d in sinm:
            print('    - %-12s sin motivo declarado, en %d cadena(s)' % (e, len(d)))
        for e, d in flojo:
            print('    - %-12s motivo que no dice nada' % e)
        for e, d in sind:
            print('    - %-12s en la cadena y ningun campo del cierre lo cita' % e)
        print('    Origen (6-oct-2026): en la cadena de un muro, varios eslabones no se pudieron '
              'justificar. Una secuencia sin "por que" no se puede auditar.')
        return 1
    print('    OK: los eslabones de todas las cadenas traen motivo declarado y dato sellado')

    print('19/23 HANDOFF (se regenera del sello, nunca a mano)')
    import handoff as HO
    dh, ih = HO.escribir()
    print('    handoff -> %s  (%d walls, %d renglones)' % (dh, ih['walls'], ih['lineas']))

    print('19b/23 MARKUPS BLUEBEAM (W3, R78.24: PDF con una annot por wall, verificado contra el canon)')
    import reglas as _RGL
    import bitacora as _BIT
    import markups_bluebeam as _MB
    _w = None
    for _c in (B, os.path.join(B, 'etapas')):
        if _RGL.buscar_canon(_c):
            _w = _c
            break
    fm = _BIT.markups_fallas(_w, out, out) if _w else ['sin takeoff_canon.json en %s' % B]
    if fm:
        print('\n*** SIN PDF DE MARKUPS VERIFICADO -- NO SE ENTREGA:')
        for f in fm[:20]:
            print('    -', f)
        return 1
    _rm, _ = _MB.resumen_vigente([_w, os.path.join(_w, 'out'), os.path.join(_w, '4_canon'),
                                  os.path.dirname(os.path.abspath(out)), os.environ.get('TAKEOFF_OUT')],
                                 _RGL.buscar_canon(_w))
    print('    OK: %s (%d annots)' % (_rm['pdf'], _rm['annots']))

    print('20/23 COPIA A ENTREGA')
    os.makedirs(ENTREGA, exist_ok=True)
    dst = os.path.join(ENTREGA, os.path.basename(out))
    shutil.copy2(out, dst)
    shutil.copy2(VV._mf_path(out), VV._mf_path(dst))
    # v78 (W3): el PDF de markups viaja con el libro (entregable fijo)
    shutil.copy2(_rm['pdf'], os.path.join(ENTREGA, os.path.basename(_rm['pdf'])))
    # Los scripts viajan con el entregable: un numero cuyo script no esta en la carpeta
    # no se puede volver a producir, y entonces no esta entregado.
    dt = os.path.join(ENTREGA, 'Herramientas')
    os.makedirs(dt, exist_ok=True)
    n = 0
    for f in sorted(glob.glob(B + '/tools/*.py')):
        d = os.path.join(dt, os.path.basename(f))
        if not os.path.exists(d) or os.path.getmtime(f) > os.path.getmtime(d):
            shutil.copy2(f, d)
        n += 1
    print('    ->', dst)
    print('    -> %s  (%d scripts)' % (dt, n))

    print('21/23  INDICE (cuenta la carpeta ya poblada, nunca a mano)')
    import hoja_indice
    hoja_indice.main(out)

    print('22/23  IDIOMA (nombre de material en ingles)')
    # Va DESPUES de regenerar el estado: revisa los archivos FINALES. Corriendo antes leia
    # el <PREFIJO>_ESTADO.md viejo y reportaba una falta que el paso siguiente ya arreglaba.
    import verif_idioma as VI
    fi = VI.verificar(out)
    if fi:
        print('\n*** HAY NOMBRES DE MATERIAL EN ESPANOL (%d) -- NO SE ENTREGA:' % len(fi))
        for d, w, t in fi[:12]:
            print('    - %-26s %-20s %s' % (d, ','.join(w), t[:70]))
        return 1
    print('    OK: no queda ningun nombre de material en espanol')

    # TRINQUETE: el entregable va INTEGRO en ingles. El tope solo baja.
    # Son DOS cuentas con DOS topes, y se imprimen por separado: el libro (redaccion propia,
    # se paga reescribiendo el generador) y la hoja de evidencia `Detail log` (cita literal
    # del cierre sellado, se paga traduciendo el CIERRE -- reescribir la cita la volveria
    # falsa). Ninguna de las dos esta exenta y las dos solo pueden bajar.
    for ev, tope, que in ((False, VI.TOPE_ES, 'libro'),
                          (True, VI.TOPE_ES_LOG, 'hoja de evidencia Detail log'),
                          ('handoff', VI.TOPE_ES_HANDOFF_XLSX, 'hojas Handoff del libro')):
        ce = VI.celdas_espanol(out, ev)
        if len(ce) > tope:
            print('\n*** %d celdas con frase en ESPANOL en el %s, y el tope declarado es '
                  '%d -- NO SE ENTREGA. Una frase nueva en espanol rompe la entrega el '
                  'mismo dia.' % (len(ce), que, tope))
            for d, w, t in ce[:8]:
                print('    - %-22s %-18s %s' % (d, ','.join(w[:3]), t[:60]))
            return 1
        print('    atraso de traduccion, %-30s %4d celdas (tope %d, solo baja)'
              % (que + ':', len(ce), tope))

    # TERCER TRINQUETE: el VOCABULARIO DEL TRADE en prosa (wall, door, dimension, line item...).
    # Lista aparte de glosario.py porque varias de esas palabras son CLAVES del cierre.
    nd, nc, nhx = VI.vocab_pendiente(out)
    for n, tope, que in ((nd, VI.TOPE_VOCAB_DOCS, 'documentos'),
                         (nc, VI.TOPE_VOCAB_LIBRO, 'libro'),
                         (nhx, VI.TOPE_VOCAB_HANDOFF_XLSX, 'hojas Handoff del libro')):
        if n > tope:
            print('\n*** %d termino(s) del trade en ESPANOL en los %s, y el tope declarado es '
                  '%d -- NO SE ENTREGA. Regla inviolable del 7-oct-2026.' % (n, que, tope))
            return 1
    print('    vocabulario del trade pendiente: %d en documentos (tope %d) · %d celdas del '
          'libro (tope %d) · %d celdas de las hojas Handoff (tope %d), los tres solo bajan'
          % (nd, VI.TOPE_VOCAB_DOCS, nc, VI.TOPE_VOCAB_LIBRO, nhx,
             VI.TOPE_VOCAB_HANDOFF_XLSX))

    print('23/23  HANDOFF EN INGLES (su propio trinquete: cita texto sellado palabra por palabra)')
    # CUARTO TRINQUETE, aparte y NO exento. El handoff cita el texto SELLADO de cada wall;
    # reescribir la cita en ingles la volveria FALSA. Y el atraso tiene una causa medida: los
    # terminos en espanol que quedan son EXACTAMENTE los de los 4 bloques HUERFANOS (A5, B,
    # B2K, C1), porque "se traduce el GENERADOR, no la salida" y esos cuatro no tienen
    # generador. Baja cuando se escriban sus closers, no antes.
    nh = VI.handoff_pendiente()
    if nh > VI.TOPE_VOCAB_HANDOFF:
        print('\n*** %d termino(s) del trade en ESPANOL en el handoff, y el tope declarado es '
              '%d -- NO SE ENTREGA. Si subio, es texto NUEVO escrito en espanol: se escribe '
              'en ingles desde el principio.' % (nh, VI.TOPE_VOCAB_HANDOFF))
        return 1
    print('    atraso del handoff: %d terminos (tope %d, solo baja). Bajo de cientos a unos '
          'pocos al escribir los closers que faltaban: la deuda de idioma y la de '
          'cierres huerfanos eran la misma deuda.' % (nh, VI.TOPE_VOCAB_HANDOFF))

    print('=' * 72)
    print('LISTO. Ahora si se puede mandar y copiar a la PC.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
