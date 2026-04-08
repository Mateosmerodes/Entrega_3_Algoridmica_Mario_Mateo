/*
 * ej04_monedas.cpp — Ejercicio 4: Cambio de Monedas (C++)
 * --------------------------------------------------------
 * Programa principal que usa MonedaPD.h para la logica PD.
 * Demuestra el algoritmo con distintas cantidades y conjuntos
 * de monedas, incluyendo la moneda de 8 centimos del enunciado.
 */

#include <iostream>
#include <vector>
#include <string>
#include "../clases/MonedaPD.h"

using namespace std;


void simulacion(const string& nombre,
                const vector<int>& monedas,
                const vector<int>& cantidades)
{
    cout << "\n=== " << nombre << " ===\n";
    cout << "Monedas disponibles: ";
    for (int m : monedas) cout << m << " ";
    cout << "\n";

    for (int cantidad : cantidades) {
        vector<int> minMonedas(cantidad + 1, 0);
        vector<int> monedasUsadas(cantidad + 1, 0);

        int resultado = vueltasProgDin(monedas, cantidad,
                                       minMonedas, monedasUsadas);
        cout << "\nCambio de " << cantidad << " centimos:\n";
        if (resultado == INT_MAX) {
            cout << "  No es posible dar ese cambio exacto.\n";
        } else {
            cout << "  Minimo numero de monedas: " << resultado << "\n";
            imprimirSolucion(monedasUsadas, cantidad);
        }
    }
}


int main() {
    cout << "=====================================================\n";
    cout << " EJERCICIO 4: Cambio de Monedas — Prog. Dinamica\n";
    cout << "=====================================================\n";

    // --- Caso del enunciado: 33 centimos con moneda de 8 ---
    {
        vector<int> monedas = {1, 2, 5, 8, 10, 20, 50, 100, 200};
        int cantidad = 33;
        vector<int> minMonedas(cantidad + 1, 0);
        vector<int> monedasUsadas(cantidad + 1, 0);

        int res = vueltasProgDin(monedas, cantidad, minMonedas, monedasUsadas);

        cout << "\n--- Caso del enunciado: 33 centimos ---\n";
        cout << "Monedas: 1,2,5,8,10,20,50,100,200\n";
        cout << "Minimo de monedas: " << res << "\n";
        imprimirSolucion(monedasUsadas, cantidad);

        // Tabla PD parcial para ilustrar el proceso
        cout << "\nTabla PD (cant | min monedas | ultima moneda usada):\n";
        cout << "Cant | Min | UltMoneda\n";
        for (int i = 0; i <= cantidad; ++i)
            cout << "  " << i << "  |  " << minMonedas[i]
                 << "  |  " << monedasUsadas[i] << "\n";
    }

    // --- Simulacion 1: monedas europeas + 8ct ---
    simulacion(
        "Monedas europeas + 8ct",
        {1, 2, 5, 8, 10, 20, 50, 100, 200},
        {11, 15, 33, 41, 63, 99}
    );

    // --- Simulacion 2: sistema americano ---
    simulacion(
        "Sistema americano {1,5,10,25}",
        {1, 5, 10, 25},
        {11, 30, 41, 63}
    );

    // --- Simulacion 3: fallo del voraz {1,5,10,21,25} ---
    // Para 63ct: voraz da 6 monedas, PD da 3 (3x21)
    simulacion(
        "Fallo del voraz {1,5,10,21,25}",
        {1, 5, 10, 21, 25},
        {63, 41, 30}
    );

    // --- Simulacion 4: sistema con potencias de 2 ---
    simulacion(
        "Sistema {1,8,16,32}",
        {1, 8, 16, 32},
        {33, 48, 55}
    );

    cout << "\n=====================================================\n";
    cout << " Coste temporal: O(C * M)  C=cantidad, M=num.monedas\n";
    cout << " Coste espacial: O(C)\n";
    cout << "=====================================================\n";

    return 0;
}
