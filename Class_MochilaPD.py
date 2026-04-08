"""
Class_MochilaPD.py
-------------------
Implementaciones de Programacion Dinamica para el problema
de la Mochila Discreta 0/1 (0-1 Knapsack Problem).

Funciones exportadas:
  mochila_pd(pesos, beneficios, capacidad)
      -> (valor_maximo, lista_seleccion)
      Tabla completa O(n*W) para recuperar que items se eligieron.

  mochila_pd_optimizada(pesos, beneficios, capacidad)
      -> valor_maximo
      Solo 2 filas O(W) de espacio; no puede recuperar la seleccion.

Ecuacion de Bellman:
  t[i][m] = max( t[i-1][m],  b[i] + t[i-1][m-p[i]] )  si p[i] <= m
  t[i][m] = t[i-1][m]                                   si p[i] > m

Coste:
  Temporal : O(n * W)   n = num. items, W = capacidad
  Espacial : O(n * W)   version tabla completa
             O(W)       version optimizada
"""


def mochila_pd(pesos, beneficios, capacidad):
    """
    PD Bottom-Up con tabla completa.
    Devuelve (valor_maximo, lista_binaria) donde lista_binaria[i]=1
    indica que el item i fue seleccionado.

    Coste temporal: O(n * W) | Coste espacial: O(n * W)
    """
    n = len(pesos)
    # t[i][m]: maximo beneficio con items 0..i-1 y capacidad m
    t = [[0] * (capacidad + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for m in range(capacidad + 1):
            if pesos[i - 1] <= m:
                t[i][m] = max(t[i - 1][m],
                              beneficios[i - 1] + t[i - 1][m - pesos[i - 1]])
            else:
                t[i][m] = t[i - 1][m]

    # Recuperar que items se seleccionaron recorriendo la tabla atras
    seleccion = [0] * n
    m         = capacidad
    for i in range(n, 0, -1):
        if t[i][m] != t[i - 1][m]:
            seleccion[i - 1] = 1
            m -= pesos[i - 1]

    return t[n][capacidad], seleccion


def mochila_pd_optimizada(pesos, beneficios, capacidad):
    """
    PD Bottom-Up con solo 2 filas (O(W) espacio).
    Solo devuelve el valor maximo; no puede recuperar la seleccion.

    Coste temporal: O(n * W) | Coste espacial: O(W)
    """
    n   = len(pesos)
    ant = [0] * (capacidad + 1)

    for i in range(n):
        act = [0] * (capacidad + 1)
        for m in range(capacidad + 1):
            if pesos[i] <= m:
                act[m] = max(ant[m], beneficios[i] + ant[m - pesos[i]])
            else:
                act[m] = ant[m]
        ant = act

    return ant[capacidad]
