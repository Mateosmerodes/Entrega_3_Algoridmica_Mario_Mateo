"""
Class_QuickSelect.py
----------------------
Algoritmo QuickSelect (Divide y Venceras) para encontrar el
elemento que ocuparia la posicion k-esima si la lista estuviera
ordenada, SIN modificar la lista original.

Funciones exportadas:
  kEsimo(V, k)   -> valor en posicion k (1-indexado) si V ordenado
  mediana(V)     -> valor en la posicion central

Coste:
  Mejor caso : O(n)    el pivote cae en posicion k directamente
  Promedio   : O(n)    pivote aleatorio reduce el problema a ~n/2
  Peor caso  : O(n^2)  pivote siempre extremo (muy improbable)
  Espacio    : O(log n) pila de recursion promedio
"""

import random


def _particion(arr, izq, der):
    """
    Particiona arr[izq..der] usando arr[der] como pivote.
    Devuelve la posicion final del pivote.
    """
    pivote = arr[der]
    i      = izq - 1
    for j in range(izq, der):
        if arr[j] <= pivote:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[der] = arr[der], arr[i + 1]
    return i + 1


def _quickselect(arr, izq, der, k):
    """
    Devuelve el elemento en la posicion k (0-indexado) de arr[izq..der]
    como si estuviera ordenado. Modifica arr in-place (trabaja sobre copia).
    """
    if izq == der:
        return arr[izq]

    # Pivote aleatorio -> evita el peor caso O(n^2)
    pivot_idx        = random.randint(izq, der)
    arr[pivot_idx], arr[der] = arr[der], arr[pivot_idx]

    pos = _particion(arr, izq, der)

    if pos == k:
        return arr[pos]
    elif k < pos:
        return _quickselect(arr, izq, pos - 1, k)
    else:
        return _quickselect(arr, pos + 1, der, k)


def kEsimo(V, k):
    """
    Devuelve el valor que ocuparia la posicion k (1-indexado)
    si V estuviera ordenado. NO modifica V.

    Parametros:
      V : lista de elementos comparables
      k : posicion deseada (1 = minimo, len(V) = maximo)

    Raises ValueError si k esta fuera de [1, len(V)].
    """
    if k < 1 or k > len(V):
        raise ValueError(f"k={k} fuera de rango [1, {len(V)}]")
    copia = V[:]    # copia para no modificar V
    return _quickselect(copia, 0, len(copia) - 1, k - 1)


def mediana(V):
    """
    Devuelve la mediana de V (posicion (n+1)//2 si V estuviera ordenado).
    Para n par devuelve el elemento central inferior.
    """
    n = len(V)
    return kEsimo(V, (n + 1) // 2)
