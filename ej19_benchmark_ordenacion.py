"""
ej19_benchmark_ordenacion.py — Programa principal Ejercicio 19
-------------------------------------------------------------
Importa todos los algoritmos de Class_Ordenacion.
Benchmark con 500 enteros, 3 escenarios y 30 repeticiones.
"""

import sys
import random
import time
sys.path.insert(0, '../clases')

from Class_Ordenacion import (burbuja, burbuja_corta, seleccion,
                               insercion, shell, mezcla, rapida)

NUM_EJECUCIONES = 30
N               = 500

ALGORITMOS = {
    "Burbuja":      burbuja,
    "BurbujaCorta": burbuja_corta,
    "Seleccion":    seleccion,
    "Insercion":    insercion,
    "Shell":        shell,
    "Mezcla":       mezcla,
    "Rapida":       rapida,
}


def medir(algoritmo, datos):
    """Ejecuta NUM_EJECUCIONES veces y devuelve tiempo medio en microsegundos."""
    tiempos = []
    for _ in range(NUM_EJECUCIONES):
        t0 = time.perf_counter()
        algoritmo(datos[:])
        t1 = time.perf_counter()
        tiempos.append((t1 - t0) * 1e6)
    return sum(tiempos) / len(tiempos)


def benchmark():
    random.seed(42)
    lista_aleatoria = random.sample(range(1, 10_001), N)
    lista_ordenada  = sorted(lista_aleatoria)
    lista_inversa   = lista_ordenada[::-1]

    escenarios = {
        "Aleatorio (promedio)": lista_aleatoria,
        "Ordenado  (mejor)":   lista_ordenada,
        "Inverso   (peor)":    lista_inversa,
    }

    print(f"\n{'='*70}")
    print(f" BENCHMARK — {N} enteros, {NUM_EJECUCIONES} rep. por caso")
    print(f"{'='*70}")
    print(f"{'Algoritmo':<16} {'Aleatorio (us)':>16} {'Ordenado (us)':>16} {'Inverso (us)':>14}")
    print("-" * 64)

    resultados = {}
    for nombre, func in ALGORITMOS.items():
        ts = {esc: medir(func, datos) for esc, datos in escenarios.items()}
        resultados[nombre] = ts
        print(f"{nombre:<16} "
              f"{ts['Aleatorio (promedio)']:>16.1f} "
              f"{ts['Ordenado  (mejor)']:>16.1f} "
              f"{ts['Inverso   (peor)']:>14.1f}")

    print(f"\n--- Ranking (caso aleatorio) ---")
    ranking = sorted(resultados.items(), key=lambda x: x[1]['Aleatorio (promedio)'])
    for pos, (nombre, ts) in enumerate(ranking, 1):
        print(f"  {pos}. {nombre:<14} {ts['Aleatorio (promedio)']:>8.1f} us")

    return resultados


if __name__ == "__main__":
    print("=" * 70)
    print(" EJERCICIO 19: Benchmark Algoritmos de Ordenacion (500 enteros)")
    print("=" * 70)
    benchmark()
    print(f"""
ANALISIS:
  O(n^2):     Burbuja, Seleccion, Insercion -> lentos en general
  O(n log n): Mezcla, Shell, Rapida        -> los mas rapidos

  Mejor caso (lista ordenada):
    BurbujaCorta e Insercion -> O(n) (parada / 1 comparacion por paso)
    Seleccion -> O(n^2) siempre (busca el maximo aunque ya este ordenado)

  Peor caso (lista inversa):
    O(n^2) para burbuja/seleccion/insercion
    O(n log n) para shell/mezcla/rapida (rapida usa pivote aleatorio)

  Conclusiones:
    Rapida y Shell: mejores en caso general
    Mezcla: mas estable (O(n log n) siempre, O(n) memoria extra)
    Insercion: muy buena para listas casi ordenadas
""")
