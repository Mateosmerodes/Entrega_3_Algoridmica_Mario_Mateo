/*
 * MonedaPD.h — Programacion Dinamica para cambio de monedas
 * -----------------------------------------------------------
 * Funciones exportadas:
 *   vueltasProgDin(monedas, cantidad, minMonedas, monedasUsadas)
 *       Rellena los vectores y devuelve el minimo numero de monedas.
 *   imprimirSolucion(monedasUsadas, cantidad)
 *       Reconstruye e imprime las monedas usadas.
 *
 * Ecuacion de Bellman:
 *   minMonedas[c] = min{ 1 + minMonedas[c - m] }  para cada moneda m <= c
 *
 * Coste temporal: O(C * M)  C = cantidad, M = num. monedas
 * Coste espacial: O(C)
 */

#pragma once
#include <vector>
#include <climits>
#include <iostream>
using namespace std;


inline int vueltasProgDin(const vector<int>& monedas,
                           int cantidad,
                           vector<int>& minMonedas,
                           vector<int>& monedasUsadas) {
    minMonedas[0] = 0;
    for (int c = 1; c <= cantidad; ++c) {
        minMonedas[c] = INT_MAX;
        for (int m : monedas) {
            if (m <= c && minMonedas[c - m] != INT_MAX) {
                int candidato = 1 + minMonedas[c - m];
                if (candidato < minMonedas[c]) {
                    minMonedas[c]    = candidato;
                    monedasUsadas[c] = m;
                }
            }
        }
    }
    return minMonedas[cantidad];
}


inline void imprimirSolucion(const vector<int>& monedasUsadas, int cantidad) {
    cout << "  Monedas utilizadas: ";
    int c = cantidad;
    while (c > 0) {
        cout << monedasUsadas[c] << " ";
        c -= monedasUsadas[c];
    }
    cout << "\n";
}
