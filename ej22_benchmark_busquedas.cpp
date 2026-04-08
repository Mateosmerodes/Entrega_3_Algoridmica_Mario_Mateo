/*
 * ej22_benchmark_busquedas.cpp — Ejercicio 22: Benchmark Busquedas (C++)
 * -----------------------------------------------------------------------
 * Programa principal que importa los algoritmos de Busquedas.h
 * y mide sus tiempos con #include <chrono> en nanosegundos.
 *
 * Diseno del benchmark:
 *   - Lista ordenada de N=10000 enteros (1..N)
 *   - 3 posiciones: inicio (N/8), medio (N/2), final (7N/8)
 *   - NUM_REP=10000 repeticiones por caso -> tiempo medio estable
 *   - volatile int res evita que el compilador elimine la llamada
 */

#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
#include <random>
#include <chrono>
#include <iomanip>
#include <string>
#include "../clases/Busquedas.h"

using namespace std;
using namespace chrono;

// ── Configuracion ────────────────────────────────────────────
const int N       = 10000;
const int NUM_REP = 10000;

typedef int(*BuscFn)(const vector<int>&, int);


// ── Funcion de medicion ──────────────────────────────────────
long long medirNs(BuscFn fn, const vector<int>& v, int val) {
    long long total = 0;
    for (int r = 0; r < NUM_REP; ++r) {
        auto t0          = high_resolution_clock::now();
        volatile int res = fn(v, val);
        auto t1          = high_resolution_clock::now();
        total           += duration_cast<nanoseconds>(t1 - t0).count();
        (void)res;
    }
    return total / NUM_REP;
}


// ── Estructura de resultado ──────────────────────────────────
struct Resultado {
    string    nombre;
    long long ns_inicio, ns_medio, ns_final, ns_promedio;
};

Resultado benchmarkAlgoritmo(const string& nombre,
                              BuscFn fn,
                              const vector<int>& v) {
    int val_inicio = v[N / 8];
    int val_medio  = v[N / 2];
    int val_final  = v[7 * N / 8];

    long long ni = medirNs(fn, v, val_inicio);
    long long nm = medirNs(fn, v, val_medio);
    long long nf = medirNs(fn, v, val_final);

    return {nombre, ni, nm, nf, (ni + nm + nf) / 3};
}


// ── Main ─────────────────────────────────────────────────────
int main() {
    // Generar lista ordenada 1..N
    mt19937 rng(42);
    vector<int> v(N);
    iota(v.begin(), v.end(), 1);
    shuffle(v.begin(), v.end(), rng);
    sort(v.begin(), v.end());

    cout << "=====================================================\n";
    cout << " EJERCICIO 22: Benchmark Busquedas (nanosegundos)\n";
    cout << " N=" << N << " enteros ordenados | " << NUM_REP << " rep/caso\n";
    cout << "=====================================================\n\n";

    // Verificacion de correccion
    int test = v[N / 2];
    cout << "--- Verificacion (buscando " << test << ") ---\n";
    cout << "  Binaria:       " << busquedaBinaria(v, test)       << "\n";
    cout << "  Salto:         " << busquedaSalto(v, test)         << "\n";
    cout << "  Fibonacci:     " << busquedaFibonacci(v, test)     << "\n";
    cout << "  Exponencial:   " << busquedaExponencial(v, test)   << "\n";
    cout << "  Interpolacion: " << busquedaInterpolacion(v, test) << "\n";

    // Benchmark
    vector<Resultado> rs = {
        benchmarkAlgoritmo("Binaria",       busquedaBinaria,       v),
        benchmarkAlgoritmo("Salto",         busquedaSalto,         v),
        benchmarkAlgoritmo("Fibonacci",     busquedaFibonacci,     v),
        benchmarkAlgoritmo("Exponencial",   busquedaExponencial,   v),
        benchmarkAlgoritmo("Interpolacion", busquedaInterpolacion, v),
    };

    // Tabla de resultados
    cout << "\n--- Tiempos medios (nanosegundos) ---\n";
    cout << left  << setw(16) << "Algoritmo"
         << right << setw(12) << "Inicio"
         << setw(12) << "Medio"
         << setw(12) << "Final"
         << setw(14) << "Promedio\n";
    cout << string(66, '-') << "\n";
    for (auto& r : rs)
        cout << left  << setw(16) << r.nombre
             << right << setw(12) << r.ns_inicio
             << setw(12) << r.ns_medio
             << setw(12) << r.ns_final
             << setw(14) << r.ns_promedio << "\n";

    // Ranking
    sort(rs.begin(), rs.end(),
         [](const Resultado& a, const Resultado& b) {
             return a.ns_promedio < b.ns_promedio;
         });
    cout << "\n--- Ranking (menor = mejor) ---\n";
    for (int i = 0; i < (int)rs.size(); ++i)
        cout << "  " << i + 1 << ". "
             << left  << setw(14) << rs[i].nombre
             << right << setw(8)  << rs[i].ns_promedio << " ns\n";

    cout << "\n--- Explicacion de resultados ---\n"
         << "  Interpolacion: O(log log n) para datos uniformes (1..N) -> la mas rapida\n"
         << "  Binaria:       O(log n)     referencia clasica, muy consistente\n"
         << "  Exponencial:   O(log n)     optima si el elemento esta cerca del inicio\n"
         << "  Fibonacci:     O(log n)     sin division, similar a binaria\n"
         << "  Salto:         O(sqrt n)    mas lenta; peor cuando el valor esta al final\n";

    return 0;
}
