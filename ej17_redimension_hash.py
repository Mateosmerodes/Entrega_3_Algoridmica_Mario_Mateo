"""
ej17_redimension_hash.py — Programa principal Ejercicio 17
----------------------------------------------------------
Importa TablaHashDinamica de Class_TablaHash_Abierta.
Demuestra la redimension automatica al siguiente primo >= 2*tamano
cuando el factor de carga supera el umbral.
"""

import sys
sys.path.insert(0, '../clases')

from Class_TablaHash_Abierta import TablaHashDinamica, _siguiente_primo


if __name__ == "__main__":
    print("=" * 60)
    print(" EJERCICIO 17: Redimension automatica de Tabla Hash")
    print("=" * 60)

    # --- Siguiente primo al doble ---
    print("\n--- Siguiente primo al doble del tamano ---")
    for t in [11, 23, 47, 97, 197]:
        sp = _siguiente_primo(2 * t)
        print(f"  tamano={t:4} -> doble={2*t:4} -> siguiente primo={sp}")

    # --- Insercion progresiva con redimension ---
    print("\n--- Insercion progresiva (umbral=0.75) ---")
    th     = TablaHashDinamica(tamano_inicial=11, umbral=0.75)
    claves = list(range(5, 45, 3))   # 13 claves distintas
    for k in claves:
        th[k] = f"val{k}"
        print(f"  Insertado clave={k:3}  |  {th.info()}")

    print(f"\nTabla final:\n{th}")

    # --- Verificacion post-redimension ---
    print("\n--- Verificacion: todos los elementos accesibles ---")
    errores = sum(1 for k in claves if th[k] != f"val{k}")
    print(f"  Errores: {errores}  (debe ser 0) ✓" if errores == 0
          else f"  ERRORES: {errores}")

    # --- Eliminacion y reinsercion tras redimension ---
    print("\n--- Eliminacion y reinsercion post-redimension ---")
    th.eliminar(claves[0]); th.eliminar(claves[2])
    print(f"  Eliminados: {claves[0]}, {claves[2]}")
    th[999] = "nuevo"
    print(f"  Insertado 999='nuevo'  |  {th.info()}")
    print(f"  obtener(999)         = {th[999]}")
    print(f"  obtener({claves[0]}) = {th[claves[0]]}  (debe ser None)")

    # --- Multiples redimensiones ---
    print("\n--- Multiples redimensiones (100 elementos) ---")
    th2 = TablaHashDinamica(tamano_inicial=7, umbral=0.7)
    for i in range(1, 101):
        th2[i * 7] = f"e{i}"
    print(f"  Tras 100 inserciones: {th2.info()}")
    errores2 = sum(1 for i in range(1, 101) if th2[i*7] != f"e{i}")
    print(f"  Errores de acceso: {errores2}  (debe ser 0) ✓"
          if errores2 == 0 else f"  ERRORES: {errores2}")

    print("\n" + "=" * 60)
    print(" ANALISIS DE COSTE:")
    print("  Agregar (amortizado): O(1)")
    print("  Redimension:          O(n) puntual, O(1) amortizado")
    print("  Siguiente primo:      O(sqrt(n))")
    print("  __len__:              O(1)  (contador separado)")
    print("=" * 60)
