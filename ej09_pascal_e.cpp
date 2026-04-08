/*
 * ej09_pascal_e.cpp — Ejercicio 9: Triangulo de Pascal + Numero e (C++)
 * -----------------------------------------------------------------------
 * Programa principal que usa Pascal.h para la logica del triangulo
 * y la aproximacion del numero e.
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include "../clases/Pascal.h"

using namespace std;


int main() {
    cout << "=====================================================\n";
    cout << " EJERCICIO 9: Triangulo de Pascal + Numero e\n";
    cout << "=====================================================\n";

    // --- Parte A: imprimir el triangulo ---
    imprimirTriangulo(7);
    imprimirTriangulo(10);

    // --- Parte B: aproximacion del numero e ---
    cout << "\n=====================================================\n";
    cout << " APROXIMACION DEL NUMERO e\n";
    cout << " Valor real: e = " << fixed << setprecision(10) << M_E << "\n";
    cout << "=====================================================\n";

    // Detalle con 8 filas mostrando listas intermedias
    cout << "\n--- Detalle con 8 filas (listas A y B del enunciado) ---\n";
    double a8 = aproximarE(8, true);
    cout << "\nAprox. con 8 filas: " << fixed << setprecision(8) << a8
         << " | Error: " << abs(a8 - M_E) / M_E * 100.0 << "%\n";

    // Tabla de convergencia con distintos numeros de filas
    cout << "\n--- Tabla de convergencia ---\n";
    cout << setw(8)  << "Filas"
         << setw(16) << "Aprox. e"
         << setw(20) << "Error (%)\n";
    cout << string(44, '-') << "\n";

    for (int n : {5, 10, 20, 50, 100, 200, 500, 1000, 2000}) {
        double a = aproximarE(n, false);
        cout << setw(8)  << n
             << setw(16) << fixed << setprecision(8) << a
             << setw(20) << scientific << setprecision(4)
             << abs(a - M_E) / M_E * 100.0 << "\n";
    }

    cout << "\n=====================================================\n";
    cout << " ANALISIS DE COSTE:\n";
    cout << "  Construccion filas: O(n^2) temporal, O(n) espacial\n";
    cout << "  Log del producto:   O(n) por fila\n";
    cout << "  Total:              O(n^2) temporal, O(n) espacial\n";
    cout << "  Con n=2000: error < 0.025% respecto a e real\n";
    cout << "=====================================================\n";

    return 0;
}
