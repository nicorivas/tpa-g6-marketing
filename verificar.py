#!/usr/bin/env python3
"""Verifica que reporte_propuesto.csv no rompa algunas reglas duras. Uso: python3 verificar.py [archivo.csv]
Columnas fijas (8): canal, desde, hasta, gasto, leads, cpl, dias_excluidos, regla_aplicada.
Columnas extra que tolera: cpl_semana_anterior (todas las opciones) y cpl_sin_anomalos (solo la opción 3).
Debe haber una fila por canal y una fila TOTAL. Con cero leads, el cpl es «sin leads»."""
import csv, sys
from datetime import date
from pathlib import Path
AQUI = Path(__file__).resolve().parent
canales = {r["canal"]: r for r in csv.DictReader(open(AQUI / "datos/canales.csv"))}
ruta = sys.argv[1] if len(sys.argv) > 1 else "reporte_propuesto.csv"
if not Path(ruta).exists(): print(f"0 filas revisadas, 1 problema\n - no existe el archivo {ruta}"); sys.exit(1)
lector = csv.DictReader(open(ruta))
filas = list(lector)
errores = []
FIJAS = ["canal", "desde", "hasta", "gasto", "leads", "cpl", "dias_excluidos", "regla_aplicada"]
faltan = [x for x in FIJAS if x not in (lector.fieldnames or [])]
if faltan:
    print(f"0 filas revisadas, 1 problema\n - faltan columnas: {', '.join(faltan)}"); sys.exit(1)
por_canal = {f["canal"].strip(): f for f in filas}
for c in canales:
    if c not in por_canal: errores.append(f"{c}: no aparece en el reporte")
if "TOTAL" not in por_canal: errores.append("TOTAL: falta la fila de total")
suma_total = 0
for f in filas:
    c = f["canal"].strip()
    if c != "TOTAL" and c not in canales: errores.append(f"{c}: no es un canal conocido"); continue
    try:
        desde, hasta = date.fromisoformat(f["desde"]), date.fromisoformat(f["hasta"])
        if desde > hasta: errores.append(f"{c}: el período empieza después de terminar")
    except ValueError: errores.append(f"{c}: fecha mal escrita")
    try: gasto, leads = int(f["gasto"]), int(f["leads"])
    except ValueError: errores.append(f"{c}: gasto o leads no son números enteros"); continue
    cpl = f["cpl"].strip()
    if leads == 0 and cpl != "sin leads": errores.append(f"{c}: regla 1, con cero leads el CPL debe decir «sin leads» y dice «{cpl}»")
    if leads > 0:
        try:
            if abs(float(cpl) - gasto / leads) > 0.01 * gasto / leads: errores.append(f"{c}: regla 2, el CPL {cpl} no es gasto entre leads ({gasto / leads:.0f})")
        except ValueError: errores.append(f"{c}: el CPL «{cpl}» no es un número")
    for extra in ("cpl_semana_anterior", "cpl_sin_anomalos"):          # columnas opcionales: solo se mira que sean un número, «sin leads» o vacío
        v = (f.get(extra) or "").strip()
        if v and v != "sin leads":
            try: float(v)
            except ValueError: errores.append(f"{c}: {extra} debe ser un número o «sin leads» y dice «{v}»")
    if not f.get("regla_aplicada", "").strip(): errores.append(f"{c}: regla 10, falta la regla aplicada")
    if c != "TOTAL" and canales[c]["estado"] != "prueba": suma_total += gasto
if "TOTAL" in por_canal:
    try:
        if int(por_canal["TOTAL"]["gasto"]) != suma_total:
            errores.append(f"TOTAL: regla 6, el gasto total es {por_canal['TOTAL']['gasto']} y los canales que no están en prueba suman {suma_total}")
    except ValueError: pass
print(f"{len(filas)} filas revisadas, {len(errores)} problemas")
for x in errores: print(" -", x)
sys.exit(1 if errores else 0)
