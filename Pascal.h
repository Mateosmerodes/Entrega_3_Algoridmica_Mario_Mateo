/*
 * Pascal.h — Triangulo de Pascal y aproximacion del numero e
 * -----------------------------------------------------------
 * Funciones exportadas:
 *   siguienteFila(ant)     Construye la fila n a partir de n-1 (PD bottom-up)
 *   imprimirTriangulo(n)   Imprime n filas del triangulo
 *   logProdFila(n)         log( producto de todos los C(n,k) ) en O(n)
 *   aproximarE(n, verbose) Aproxima e usando el proceso del enunciado
 *
 * Tecnica: PD Bottom-Up + calculo en espacio logaritmico para evitar overflow.
 * Coste:   O(n^2) temporal, O(n) espacial.
 */

#pragma once
#include <vector>
#include <cmath>
#include <iostream>
#include <iomanip>
using namespace std;


// ── Construccion de filas (PD bottom-up) ────────────────────

inline vector<long long> siguienteFila(const vector<long long>& ant) {
    int n = (int)ant.size();
    vector<long long> act(n + 1, 1);
    for (int i = 1; i < n; ++i)
        act[i] = ant[i - 1] + ant[i];
    return act;
}


// ── Impresion del triangulo ──────────────────────────────────

inline void imprimirTriangulo(int numFilas) {
    cout << "\nTriangulo de Pascal (" << numFilas << " filas):\n";
    vector<long long> fila = {1};
    for (int i = 0; i < numFilas; ++i) {
        for (int s = 0; s < numFilas - i - 1; ++s) cout << "   ";
        for (long long v : fila) cout << setw(5) << v;
        cout << "\n";
        if (i < numFilas - 1) fila = siguienteFila(fila);
    }
}


// ── Log del producto de una fila ─────────────────────────────
/*
 * log( prod_{k=0}^{n} C(n,k) ) usando la relacion recursiva:
 *   logC(n,k) = logC(n,k-1) + log(n-k+1) - log(k)
 * Coste O(n) por fila; evita desbordamiento para n grande.
 */
inline double logProdFila(int n) {
    if (n == 0) return 0.0;
    double s = 0.0, logCnk = 0.0;
    for (int k = 1; k <= n; ++k) {
        logCnk += log((double)(n - k + 1)) - log((double)k);
        s      += logCnk;
    }
    return s;
}


// ── Aproximacion del numero e ────────────────────────────────
/*
 * Proceso:
 *   1. logProd[i] = log( producto fila i )
 *   2. A[i]  = prod[i] / prod[i-1]  = exp(logProd[i] - logProd[i-1])
 *   3. B[i]  = A[i+1]  / A[i]       calculado directamente en log
 *              = exp( (logProd[i+2]-logProd[i+1]) - (logProd[i+1]-logProd[i]) )
 *   B converge a e cuando i -> infinito.
 */
inline double aproximarE(int numFilas, bool verbose = false) {
    // Construir vector de log(prod) de cada fila
    vector<double> logProds(numFilas + 1);
    for (int i = 0; i <= numFilas; ++i)
        logProds[i] = logProdFila(i);

    // Lista A (para mostrar si verbose)
    vector<double> listaA(numFilas, 1.0);
    for (int i = 1; i < numFilas; ++i) {
        double logA = logProds[i] - logProds[i - 1];
        listaA[i]   = (logA < 700) ? exp(logA) : 1e300;
    }

    // Lista B en espacio log (evita overflow)
    vector<double> listaB(numFilas - 1);
    for (int i = 0; i < numFilas - 1; ++i) {
        double logB = (logProds[i + 2] - logProds[i + 1])
                    - (logProds[i + 1] - logProds[i]);
        listaB[i] = exp(logB);
    }

    if (verbose) {
        int m = min(numFilas, 8);
        cout << "\n--- Lista A (prod[i]/prod[i-1]) ---\n";
        for (int i = 0; i < m; ++i)
            cout << "  A[" << i << "] = " << fixed << setprecision(6)
                 << listaA[i] << "\n";
        cout << "\n--- Lista B (A[i]/A[i-1]) -> converge a e ---\n";
        for (int i = 0; i < m && i < (int)listaB.size(); ++i)
            cout << "  B[" << i << "] = " << fixed << setprecision(8)
                 << listaB[i] << "\n";
    }

    return listaB.empty() ? 2.0 : listaB.back();
}
