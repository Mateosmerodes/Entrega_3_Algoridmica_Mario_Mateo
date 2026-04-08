/*
 * Busquedas.h — Algoritmos de busqueda sobre vector<int> ordenado
 * -----------------------------------------------------------------
 * Funciones exportadas:
 *   busquedaBinaria(v, val)      O(log n)
 *   busquedaSalto(v, val)        O(sqrt n)
 *   busquedaFibonacci(v, val)    O(log n)
 *   busquedaExponencial(v, val)  O(log n)
 *   busquedaInterpolacion(v, val) O(log log n) uniforme / O(n) peor
 *
 * Todas devuelven el indice del elemento encontrado, o -1 si no existe.
 * El vector debe estar ordenado ascendentemente.
 */

#pragma once
#include <vector>
#include <cmath>
#include <algorithm>
using namespace std;


// ── 1. Busqueda Binaria Iterativa ── O(log n) ───────────────
inline int busquedaBinaria(const vector<int>& v, int val) {
    int izq = 0, der = (int)v.size() - 1;
    while (izq <= der) {
        int mid = izq + (der - izq) / 2;
        if      (v[mid] == val) return mid;
        else if (v[mid] < val)  izq = mid + 1;
        else                    der = mid - 1;
    }
    return -1;
}


// ── 2. Busqueda por Salto ── O(sqrt n) ──────────────────────
inline int busquedaSalto(const vector<int>& v, int val) {
    int n     = (int)v.size();
    int salto = (int)sqrt((double)n);
    int izq   = 0, dcha = 0;

    while (dcha < n - 1 && v[min(dcha + salto, n - 1)] <= val) {
        izq  = dcha;
        dcha = min(dcha + salto, n - 1);
        if (v[dcha] == val) return dcha;
    }
    for (int i = izq; i <= dcha && i < n; ++i)
        if (v[i] == val) return i;
    return -1;
}


// ── 3. Busqueda de Fibonacci ── O(log n) ────────────────────
inline int busquedaFibonacci(const vector<int>& v, int val) {
    int n = (int)v.size();
    int fibM2 = 0, fibM1 = 1, fibM = 1;
    while (fibM < n) {
        fibM2 = fibM1; fibM1 = fibM; fibM = fibM1 + fibM2;
    }
    int idx = -1;
    while (fibM > 1) {
        int i = min(idx + fibM2, n - 1);
        if      (v[i] < val) { fibM = fibM1; fibM1 = fibM2; fibM2 = fibM - fibM1; idx = i; }
        else if (v[i] > val) { fibM = fibM2; fibM1 -= fibM2; fibM2 = fibM - fibM1; }
        else return i;
    }
    if (fibM1 && idx + 1 < n && v[idx + 1] == val) return idx + 1;
    return -1;
}


// ── 4. Busqueda Exponencial ── O(log n) ─────────────────────
inline int busquedaExponencial(const vector<int>& v, int val) {
    int n = (int)v.size();
    if (v[0] == val) return 0;
    int i = 1;
    while (i < n && v[i] <= val) i *= 2;
    int izq = i / 2, der = min(i, n - 1);
    while (izq <= der) {
        int mid = izq + (der - izq) / 2;
        if      (v[mid] == val) return mid;
        else if (v[mid] < val)  izq = mid + 1;
        else                    der = mid - 1;
    }
    return -1;
}


// ── 5. Busqueda de Interpolacion ── O(log log n) uniforme ───
inline int busquedaInterpolacion(const vector<int>& v, int val) {
    int izq = 0, der = (int)v.size() - 1;
    while (izq <= der && val >= v[izq] && val <= v[der]) {
        if (izq == der) {
            return (v[izq] == val) ? izq : -1;
        }
        int pos = izq + (int)(((double)(val - v[izq]) / (v[der] - v[izq]))
                              * (der - izq));
        if      (v[pos] == val) return pos;
        else if (v[pos] < val)  izq = pos + 1;
        else                    der = pos - 1;
    }
    return -1;
}
