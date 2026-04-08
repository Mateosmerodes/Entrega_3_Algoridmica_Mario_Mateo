"""
ej23_tad_mapa.py — Programa principal Ejercicio 23
--------------------------------------------------
Importa MapaAbierto y MapaEncadenado de Class_Mapa,
y ListaOrdenadaMapa de Class_ListaOrdenada_Mapa.
Demuestra ambas implementaciones del TAD Mapa.
"""

import sys
sys.path.insert(0, '../clases')

from Class_Mapa               import MapaAbierto, MapaEncadenado
from Class_ListaOrdenada_Mapa import ListaOrdenadaMapa


def demo_lista_ordenada():
    print("\n" + "=" * 60)
    print(" DEMO ListaOrdenadaMapa (metodos requeridos)")
    print("=" * 60)
    lst = ListaOrdenadaMapa()
    for k, v in [(5,"e"), (2,"b"), (8,"h"), (1,"a"), (6,"f"), (3,"c")]:
        lst.insertar(k, v)
    print(f"Lista ordenada: {lst}")
    print(f"tamano() = {lst.tamano()}  [O(1)]")
    print(f"indice(0) = {lst.indice(0)}")
    print(f"indice(2) = {lst.indice(2)}")
    print(f"extraer(pos=1) = {lst.extraer(1)}")
    print(f"Lista tras extraer pos=1: {lst}")
    print(f"borrar(5) = {lst.borrar(5)}")
    print(f"Lista tras borrar 5: {lst}")
    print(f"extraer() [primero por defecto] = {lst.extraer()}")
    print(f"Lista final: {lst}")


def demo_abierto():
    print("\n" + "=" * 60)
    print(" a) MAPA CON DIRECCIONAMIENTO ABIERTO")
    print("=" * 60)
    m = MapaAbierto(tamano=7)

    print("\n--- Insercion (lambda umbral=90%) ---")
    datos = [(10,"diez"), (17,"diec"), (3,"tres"), (24,"venti"),
             (31,"treinta"), (38,"treintaocho"), (45,"cuarentacinco")]
    for k, v in datos:
        m[k] = v
        print(f"  [{k}]='{v}'  | {m.info()}")

    print(f"\nTabla:\n{m}")
    print(f"len(m) = {len(m)}  [O(1)]")

    print("\n--- Acceso ---")
    for k in [10, 17, 99]:
        print(f"  m[{k}] = {m[k]}")

    print("\n--- Eliminar ---")
    for k in [17, 99]:
        print(f"  eliminar({k}) = {m.eliminar(k)}")
    print(f"Tabla tras eliminar:\n{m}")
    print(f"m[17] = {m[17]}  (debe ser None)")
    print(f"m[24] = {m[24]}  (debe seguir accesible)")

    print("\n--- Redimension al 90% ---")
    m2 = MapaAbierto(tamano=7)
    for i in range(8):
        m2[i * 7] = f"val{i}"
        print(f"  Insertado {i*7}: {m2.info()}")
    errores = sum(1 for i in range(8) if m2[i*7] != f"val{i}")
    print(f"Errores post-redimension: {errores}  (debe ser 0) ✓"
          if errores == 0 else f"ERRORES: {errores}")


def demo_encadenado():
    print("\n" + "=" * 60)
    print(" b) MAPA CON ENCADENAMIENTO (ListaOrdenadaMapa)")
    print("=" * 60)
    m = MapaEncadenado(tamano=7)

    print("\n--- Insercion con colisiones ---")
    datos = [(10,"diez"), (17,"diec"), (3,"tres"), (24,"venti"),
             (31,"treinta"), (4,"cuatro"), (11,"once")]
    for k, v in datos:
        m[k] = v
        print(f"  [{k}]='{v}'  slot={k%7}  | {m.info()}")

    print(f"\nTabla (listas ordenadas):\n{m}")
    print(f"len(m) = {len(m)}  [O(1)]")

    print("\n--- Acceso ---")
    for k in [10, 31, 99]:
        print(f"  m[{k}] = {m[k]}")

    print("\n--- indice(slot, pos) ---")
    for slot in range(7):
        lst = m._slots[slot]
        for p in range(lst.tamano()):
            print(f"  slot={slot}, pos={p}: {m.indice(slot, p)}")

    print("\n--- extraer_de_slot ---")
    slot_test = 10 % 7
    print(f"  extraer slot={slot_test} pos=0: {m.extraer_de_slot(slot_test, 0)}")
    print(f"  Tabla tras extraer ({len(m)} elementos):\n{m}")

    print("\n--- Eliminar ---")
    for k in [17, 99]:
        print(f"  eliminar({k}) = {m.eliminar(k)}")
    print(f"Tabla final:\n{m}")


if __name__ == "__main__":
    print("=" * 60)
    print(" EJERCICIO 23: TAD Mapa — Dir. Abierta y Encadenamiento")
    print("=" * 60)
    demo_lista_ordenada()
    demo_abierto()
    demo_encadenado()

    print("\n" + "=" * 60)
    print(" COSTE OPERACIONES:")
    print("  Dir. Abierta: insertar/buscar/eliminar O(1/(1-lambda)) amort.")
    print("  Encadenam.:   insertar/buscar/eliminar O(1 + lambda)")
    print("  __len__:      O(1) en ambas (contador separado)")
    print("  Redimension:  O(n) puntual (MapaAbierto al 90%)")
    print("=" * 60)
