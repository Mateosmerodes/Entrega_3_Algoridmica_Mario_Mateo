"""
ej05_mochila.py — Programa principal Ejercicio 5
-------------------------------------------------
Importa las funciones PD de Class_MochilaPD.
Demuestra el problema de la mochila discreta 0/1 con
distintas capacidades y conjuntos de items.
"""

import sys
sys.path.insert(0, '../clases')

from Class_MochilaPD import mochila_pd, mochila_pd_optimizada


def imprimir_tabla(pesos, beneficios, capacidad, etiqueta=""):
    """Imprime la tabla PD completa para ilustrar el proceso."""
    n = len(pesos)
    t = [[0] * (capacidad + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for m in range(capacidad + 1):
            if pesos[i-1] <= m:
                t[i][m] = max(t[i-1][m], beneficios[i-1] + t[i-1][m - pesos[i-1]])
            else:
                t[i][m] = t[i-1][m]

    print(f"\n{etiqueta}")
    print(f"Tabla PD (filas=items, columnas=capacidad 0..{capacidad})")
    header = "Item\\Cap |" + "".join(f"{c:4}" for c in range(capacidad + 1))
    print(header)
    print("-" * len(header))
    print("   0     |" + "".join(f"{0:4}" for _ in range(capacidad + 1)))
    for i in range(1, n + 1):
        fila  = f"   {i} p={pesos[i-1]},b={beneficios[i-1]:2} |"
        fila += "".join(f"{t[i][m]:4}" for m in range(capacidad + 1))
        print(fila)


def simular(nombre, pesos, beneficios, capacidad):
    """Ejecuta la mochila PD y muestra resultados detallados."""
    print(f"\n{'='*60}")
    print(f" {nombre}")
    print(f"{'='*60}")
    print(f"Capacidad mochila: {capacidad}")
    print(f"{'Item':>5} {'Peso':>6} {'Beneficio':>10}")
    for i, (p, b) in enumerate(zip(pesos, beneficios), 1):
        print(f"{i:>5} {p:>6} {b:>10}")

    imprimir_tabla(pesos, beneficios, capacidad,
                   "--- Construccion de la tabla PD ---")

    valor, sel   = mochila_pd(pesos, beneficios, capacidad)
    valor_opt    = mochila_pd_optimizada(pesos, beneficios, capacidad)
    peso_total   = sum(p * s for p, s in zip(pesos, sel))
    ben_total    = sum(b * s for b, s in zip(beneficios, sel))

    print(f"\n--- Resultado ---")
    print(f"Valor maximo:          {valor}")
    print(f"Valor (version O(W)):  {valor_opt}  (verificacion)")
    print(f"Items seleccionados:   {sel}")
    print(f"Peso total usado:      {peso_total} / {capacidad}")
    print(f"Beneficio total:       {ben_total}")


if __name__ == "__main__":
    print("=" * 60)
    print(" EJERCICIO 5: Problema de la Mochila Discreta - PD")
    print("=" * 60)

    simular("Ejemplo del enunciado (capacidad=20)",
            pesos=[2, 3, 4, 5, 9], beneficios=[3, 4, 8, 8, 10], capacidad=20)

    simular("Ejemplo clasico (capacidad=10)",
            pesos=[2, 5, 3, 6, 1], beneficios=[28, 33, 5, 12, 20], capacidad=10)

    simular("Caso donde el voraz falla (capacidad=5)",
            pesos=[3, 4, 5], beneficios=[4, 5, 6], capacidad=5)

    simular("Caso grande (capacidad=50)",
            pesos=[5, 10, 15, 7, 3, 12, 8, 4, 9, 6],
            beneficios=[10, 20, 30, 14, 6, 24, 16, 8, 18, 12], 
            capacidad=50)

    print("\n" + "=" * 60)
    print(" ANALISIS DE COSTE:")
    print("  Coste temporal:                O(n * W)")
    print("  Coste espacial tabla completa: O(n * W)")
    print("  Coste espacial version opt.:   O(W)")
    print("=" * 60)
