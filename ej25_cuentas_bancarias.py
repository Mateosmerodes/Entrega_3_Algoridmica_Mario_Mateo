"""
ej25_cuentas_bancarias.py — Programa principal Ejercicio 25
-----------------------------------------------------------
Importa TablaHashCuentas de Class_TablaHash_Cuentas.
Implementa la verificacion de digitos de control y demuestra
el sistema de busqueda de cuentas bancarias de Caixabank Lugo.
"""

import sys
import random
import time
sys.path.insert(0, '../clases')

from Class_TablaHash_Cuentas import TablaHashCuentas


# ── Calculo de digitos de control ───────────────────────────

MULTIPLICADORES = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]  # 2^n % 11, n=0..9


def calcular_dc(diez_digitos):
    """
    Calcula el digito de control para 10 digitos.
    dc = 11 - (suma % 11) ; si 10->1, si 11->0
    """
    suma = sum(int(diez_digitos[i]) * MULTIPLICADORES[i] for i in range(10))
    dc   = 11 - (suma % 11)
    if dc == 10: return 1
    if dc == 11: return 0
    return dc


def verificar_cuenta(cuenta_20):
    """Verifica si una cuenta de 20 digitos es valida."""
    dc1 = calcular_dc("00" + cuenta_20[:8])
    dc2 = calcular_dc(cuenta_20[10:])
    return dc1 == int(cuenta_20[8]) and dc2 == int(cuenta_20[9])


def generar_cuenta_valida(entidad="2100", oficina="0418"):
    """Genera una cuenta bancaria valida con los DC correctos."""
    nnnn = str(random.randint(0, 9_999_999_999)).zfill(10)
    dc1  = calcular_dc("00" + entidad + oficina)
    dc2  = calcular_dc(nnnn)
    return f"{entidad}{oficina}{dc1}{dc2}{nnnn}"


def formatear(cuenta_20):
    """Formatea 20 digitos como EEEE OOOO CC NNNNNNNNNN."""
    return f"{cuenta_20[:4]} {cuenta_20[4:8]} {cuenta_20[8:10]} {cuenta_20[10:]}"


if __name__ == "__main__":
    print("=" * 65)
    print(" EJERCICIO 25: Busqueda de Cuentas Bancarias — Tabla Hash")
    print("=" * 65)

    # --- Verificacion del ejemplo del enunciado ---
    print("\n--- Verificacion del ejemplo del enunciado ---")
    cuenta_ej = "1234567806" + "1234567890"
    dc1 = calcular_dc("00" + cuenta_ej[:8])
    dc2 = calcular_dc(cuenta_ej[10:])
    print(f"Cuenta:        {formatear(cuenta_ej)}")
    print(f"DC1 calculado: {dc1}  (esperado: 0)")
    print(f"DC2 calculado: {dc2}  (esperado: 6)")
    print(f"Cuenta valida: {verificar_cuenta(cuenta_ej)}")

    # --- Generar 200 cuentas ---
    print("\n--- Generando 200 cuentas validas (Caixabank, oficina 0418) ---")
    random.seed(2024)
    cuentas = []
    while len(cuentas) < 200:
        c = generar_cuenta_valida("2100", "0418")
        if c not in cuentas:
            cuentas.append(c)

    print("Primeras 5 cuentas:")
    for c in cuentas[:5]:
        print(f"  {formatear(c)}  valida={verificar_cuenta(c)}")
    todas_validas = all(verificar_cuenta(c) for c in cuentas)
    print(f"Todas las 200 cuentas son validas: {todas_validas}")

    # --- Cargar en tabla hash ---
    print("\n--- Cargando en tabla hash ---")
    th       = TablaHashCuentas(tamano=211)
    clientes = [f"Cliente_{i:03d}" for i in range(200)]
    for c, cli in zip(cuentas, clientes):
        th.insertar(c, cli)
    print(f"Tabla: {th.info()}")

    # --- Busquedas con tiempo ---
    print("\n--- Busquedas (10000 repeticiones para tiempo medio) ---")
    NUM_REP = 10000
    for cuenta in [cuentas[0], cuentas[99], cuentas[199]]:
        t0 = time.perf_counter()
        for _ in range(NUM_REP):
            r = th.buscar(cuenta)
        ns = (time.perf_counter() - t0) / NUM_REP * 1e6
        print(f"  buscar({formatear(cuenta)[:20]}...) = {r}  ({ns:.2f} us)")

    cuenta_falsa = "2100041800" + "9999999999"
    t0 = time.perf_counter()
    for _ in range(NUM_REP):
        r = th.buscar(cuenta_falsa)
    ns = (time.perf_counter() - t0) / NUM_REP * 1e6
    print(f"  buscar(cuenta inexistente) = {r}  ({ns:.2f} us)")

    # --- Cuenta con DC invalido ---
    print("\n--- Cuenta con DC invalido ---")
    cuenta_mala = "2100041899" + "1234567890"
    print(f"  {formatear(cuenta_mala)}: valida={verificar_cuenta(cuenta_mala)}")

    # --- Eliminar y reinsertar ---
    print("\n--- Eliminar y reinsertar ---")
    th.eliminar(cuentas[0])
    print(f"  Tras eliminar {cuentas[0][:10]}...: len={len(th)}")
    print(f"  buscar eliminada: {th.buscar(cuentas[0])}")
    th.insertar(cuentas[0], "Cliente_000_nuevo")
    print(f"  Tras reinsertar: len={len(th)}, cliente={th.buscar(cuentas[0])}")

    print("\n" + "=" * 65)
    print(" ANALISIS:")
    print("  Estructura: TABLA HASH -> busqueda O(1) promedio")
    print("  Alternativa: arbol BST -> O(log n) pero con orden")
    print("  Verificacion DC: O(1) siempre (10 multiplicaciones fijas)")
    print("=" * 65)
