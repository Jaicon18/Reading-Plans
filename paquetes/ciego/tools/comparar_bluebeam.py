# -*- coding: utf-8 -*-
"""comparar_bluebeam.py -- RETIRADA en v66 (2026-10-17, regla E24 protocolo ciego).

Contenía tablas y textos de UN proyecto de examen (coordenadas de walls, cantidades, notas por detalle).
Una tool que reciben las pruebas no puede traer respuestas. El Excel del take-off se arma SOLO con
plantilla_excel.py (52.4) desde familias_out.json; la geometría sale del plano de cada proyecto
(inventario.py, canon.py). La versión anterior queda archivada fuera del paquete de pruebas.
"""
import sys

if __name__ == "__main__":
    sys.exit("comparar_bluebeam.py RETIRADA (E24): usar plantilla_excel.py / canon.py / inventario.py")
raise ImportError("comparar_bluebeam.py RETIRADA en v66 (E24): contenía datos de un proyecto de examen")
