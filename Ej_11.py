# Elabora estrategias alternativas para elegir el valor pivote en el ordenamiento rápido. Reimplementa el
# algoritmo y haz un Benchmark de las mismas en conjuntos de datos aleatorios. ¿Bajo qué criterios estas
# estrategias funcionan mejor o peor que la estrategia de los apuntes?
# Tema4_17 - Ordenación rápida

from Ej_11_2 import QuikSort
from Ej_11_2 import QuikSortAleatorio
from Ej_11_2 import QuikSortMedio
from Ej_11_2 import QuikSortUltimo

import time
import random
import sys

# Aumentamos el límite de recursión de Python. 
# En su peor caso (lista ya ordenada y pivote en el extremo), Quicksort 
# hace una llamada recursiva por cada elemento. Con listas de >1000, Python fallaría sin esto.
sys.setrecursionlimit(10000)

def ejecutar_benchmark():
    # Tamaños de lista a evaluar
    tamanos = [1000, 2000, 3000]
    
    # Lista de tuplas con el nombre y la clase a instanciar
    algoritmos = [
        ("Base (Primero)", QuikSort),
        ("Último", QuikSortUltimo),
        ("Medio", QuikSortMedio),
        ("Aleatorio", QuikSortAleatorio)
    ]

    print("="*60)
    print(" INICIANDO BENCHMARK DE QUICKSORT ".center(60, "="))
    print("="*60)

    for n in tamanos:
        print(f"\n[+] Evaluando listas de {n} elementos:")
        
        # Generamos los dos casos de prueba
        lista_aleatoria = [random.randint(0, 10000) for _ in range(n)]
        lista_ordenada = list(range(n)) # Lista 0, 1, 2, 3...
        
        # Imprimir encabezado de la tabla
        print(f"{'Algoritmo (Pivote)'.ljust(20)} | {'Aleatoria (seg)'.ljust(15)} | {'Ordenada (seg)'.ljust(15)}")
        print("-" * 58)

        for nombre_algo, ClaseQuicksort in algoritmos:
            # OJO: Es vital pasar una COPIA de la lista (.copy()), 
            # de lo contrario el primer algoritmo la ordenaría y 
            # los siguientes algoritmos recibirían una lista ya ordenada.
            prueba_aleatoria = lista_aleatoria.copy()
            prueba_ordenada = lista_ordenada.copy()

            # --- Medir tiempo con lista Aleatoria ---
            inicio_aleat = time.perf_counter()
            ordenador = ClaseQuicksort(prueba_aleatoria)
            ordenador.ordenamientoRapido()
            fin_aleat = time.perf_counter()
            tiempo_aleat = fin_aleat - inicio_aleat

            # --- Medir tiempo con lista Ordenada ---
            inicio_ord = time.perf_counter()
            ordenador_ord = ClaseQuicksort(prueba_ordenada)
            ordenador_ord.ordenamientoRapido()
            fin_ord = time.perf_counter()
            tiempo_ord = fin_ord - inicio_ord

            # Mostrar resultados formateados a 5 decimales
            print(f"{nombre_algo.ljust(20)} | {tiempo_aleat:15.5f} | {tiempo_ord:15.5f}")

# Ejecutar la prueba
if __name__ == "__main__":
    ejecutar_benchmark()