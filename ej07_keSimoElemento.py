"""
ej07_keSimoElemento.py — Programa principal Ejercicio 7
-------------------------------------------------------
Importa kEsimo y mediana de Class_QuickSelect.
Demuestra el algoritmo QuickSelect (Divide y Venceras) para
encontrar el elemento k-esimo sin modificar el vector original.
"""

import sys
import random
sys.path.insert(0, '../clases')

from Class_QuickSelect import kEsimo, mediana


def verificar(V, k):
    """Comprueba el resultado contra sorted() y devuelve estado."""
    resultado = kEsimo(V, k)
    esperado  = sorted(V)[k - 1]
    ok        = "✓" if resultado == esperado else "✗"
    return resultado, esperado, ok


if __name__ == "__main__":
    print("=" * 60)
    print(" EJERCICIO 7: Elemento k-esimo - Divide y Venceras")
    print("=" * 60)

    # --- Ejemplo basico ---
    V = [7, 2, 10, 9, 1, 8, 3, 11, 6, 5, 4]
    print(f"\nVector V = {V}")
    print(f"V ordenado = {sorted(V)}")
    print(f"Longitud n = {len(V)}")

    print("\n--- Buscar posicion k-esima ---")
    for k in [1, 3, 6, 9, 11]:
        res, esp, ok = verificar(V, k)
        print(f"  k={k:2}: resultado={res:3}  esperado={esp:3}  {ok}")

    k_med = (len(V) + 1) // 2
    print(f"\nMediana (posicion {k_med} de {len(V)}): {mediana(V)}")
    print(f"Verificacion con sorted: {sorted(V)[k_med-1]}")

    # --- Vector con duplicados ---
    V2 = [4, 1, 3, 4, 2, 4, 1]
    print(f"\nVector con duplicados: {V2}  ->  ordenado: {sorted(V2)}")
    for k in range(1, len(V2) + 1):
        res, esp, ok = verificar(V2, k)
        print(f"  k={k}: {res} {ok}")

    # --- Estabilidad ---
    print("\n--- Estabilidad (10 ejecuciones del mismo caso) ---")
    resultados = {kEsimo([5, 3, 8, 1, 9, 2, 7], 4) for _ in range(10)}
    print(f"Resultados distintos: {resultados}  (debe ser un solo valor)")

    # --- Prueba exhaustiva ---
    print("\n--- Prueba exhaustiva (vector aleatorio de 50 elementos) ---")
    random.seed(42)
    Vgrande = random.sample(range(1, 200), 50)
    errores = sum(1 for k in range(1, len(Vgrande)+1)
                  if kEsimo(Vgrande, k) != sorted(Vgrande)[k-1])
    print(f"  Errores en {len(Vgrande)} posiciones: {errores}  (debe ser 0) ✓"
          if errores == 0 else f"  ERRORES: {errores}")

    print("\n" + "=" * 60)
    print(" ANALISIS DE COSTE:")
    print("  Mejor caso : O(n)    pivote cae en posicion k")
    print("  Promedio   : O(n)    pivote aleatorio -> ~n/2 por nivel")
    print("  Peor caso  : O(n^2)  pivote siempre extremo (muy improbable)")
    print("  Espacio    : O(log n) pila de recursion promedio")
    print("=" * 60)
