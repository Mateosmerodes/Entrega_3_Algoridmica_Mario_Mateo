"""
Class_Ordenacion.py
--------------------
Algoritmos de ordenacion de los apuntes (Tema 4).
Todos reciben una lista y devuelven una nueva lista ordenada
sin modificar la original.

Algoritmos incluidos:
  burbuja(lst)        O(n^2)     siempre
  burbuja_corta(lst)  O(n)       mejor caso (lista ordenada)
  seleccion(lst)      O(n^2)     siempre
  insercion(lst)      O(n)       mejor / O(n^2) peor
  shell(lst)          O(n^1.25)  promedio
  mezcla(lst)         O(n log n) siempre
  rapida(lst)         O(n log n) promedio / O(n^2) peor
"""

import random


# ── Burbuja ──────────────────────────────────────────────────

def burbuja(lst):
    """Ordenacion burbuja basica. O(n^2) en todos los casos."""
    a = lst[:]
    n = len(a)
    for i in range(n - 1, 0, -1):
        for j in range(i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def burbuja_corta(lst):
    """
    Burbuja con parada anticipada (early stop).
    O(n) mejor caso (lista ya ordenada): detecta que no hubo
    intercambios en una pasada y para.
    """
    a           = lst[:]
    intercambios = True
    paso        = len(a) - 1

    while paso > 0 and intercambios:
        intercambios = False
        for j in range(paso):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                intercambios   = True
        paso -= 1
    return a


# ── Seleccion ────────────────────────────────────────────────

def seleccion(lst):
    """
    Ordenacion por seleccion. O(n^2) comparaciones, maximo n-1
    intercambios (mas rapido que burbuja en la practica).
    """
    a = lst[:]
    n = len(a)
    for i in range(n - 1, 0, -1):
        max_idx = 0
        for j in range(1, i + 1):
            if a[j] > a[max_idx]:
                max_idx = j
        a[i], a[max_idx] = a[max_idx], a[i]
    return a


# ── Insercion ────────────────────────────────────────────────

def insercion(lst):
    """
    Ordenacion por insercion. O(n) mejor caso (lista ordenada),
    O(n^2) peor caso (lista inversa). Desplazamientos en lugar
    de intercambios -> mas rapido que burbuja/seleccion.
    """
    a = lst[:]
    for i in range(1, len(a)):
        val = a[i]
        pos = i
        while pos > 0 and a[pos - 1] > val:
            a[pos] = a[pos - 1]
            pos   -= 1
        a[pos] = val
    return a


# ── Shell ────────────────────────────────────────────────────

def _brecha_insercion(a, inicio, brecha):
    """Insercion con brecha (gap) para Shell sort."""
    for i in range(inicio + brecha, len(a), brecha):
        val = a[i]
        pos = i
        while pos >= brecha and a[pos - brecha] > val:
            a[pos] = a[pos - brecha]
            pos   -= brecha
        a[pos] = val


def shell(lst):
    """
    Ordenacion de Shell. Mejora la insercion usando brechas
    decrecientes (n/2, n/4, ..., 1). O(n^1.25) promedio.
    """
    a   = lst[:]
    gap = len(a) // 2
    while gap > 0:
        for start in range(gap):
            _brecha_insercion(a, start, gap)
        gap //= 2
    return a


# ── Mezcla ───────────────────────────────────────────────────

def _mezcla(izq, der):
    """Combina dos listas ordenadas en una sola ordenada."""
    res  = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            res.append(izq[i]); i += 1
        else:
            res.append(der[j]); j += 1
    res.extend(izq[i:])
    res.extend(der[j:])
    return res


def mezcla(lst):
    """
    Ordenacion por mezcla (Merge Sort). Divide y Venceras.
    O(n log n) en todos los casos. Requiere O(n) memoria extra.
    """
    if len(lst) <= 1:
        return lst[:]
    mid = len(lst) // 2
    return _mezcla(mezcla(lst[:mid]), mezcla(lst[mid:]))


# ── Rapida ───────────────────────────────────────────────────

def _particion_rapida(a, izq, der):
    """
    Particiona a[izq..der] con pivote aleatorio.
    Llama recursivamente a las dos mitades.
    """
    pivote = a[izq + random.randint(0, der - izq)]
    i, j   = izq, der
    while i <= j:
        while a[i] < pivote: i += 1
        while a[j] > pivote: j -= 1
        if i <= j:
            a[i], a[j] = a[j], a[i]
            i += 1; j -= 1
    if izq < j: _particion_rapida(a, izq, j)
    if i < der:  _particion_rapida(a, i, der)


def rapida(lst):
    """
    Ordenacion rapida (Quick Sort) con pivote aleatorio.
    O(n log n) promedio, O(n^2) peor caso (muy improbable
    con pivote aleatorio). Sin memoria extra (in-place).
    """
    a = lst[:]
    if len(a) > 1:
        _particion_rapida(a, 0, len(a) - 1)
    return a
