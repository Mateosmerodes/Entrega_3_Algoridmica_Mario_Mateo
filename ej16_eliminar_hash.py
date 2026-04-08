"""
ej16_eliminar_hash.py — Programa principal Ejercicio 16
-------------------------------------------------------
Importa TablaHashEncadenamiento y TablaHashAbierta de sus clases.
Responde a las preguntas del enunciado y demuestra el borrado
en ambas implementaciones.
"""

import sys
sys.path.insert(0, '../clases')

from Class_TablaHash_Encadenamiento import TablaHashEncadenamiento
from Class_TablaHash_Abierta        import TablaHashAbierta


def probar_encadenamiento():
    print("\n" + "=" * 60)
    print(" ENCADENAMIENTO — Eliminacion")
    print("=" * 60)
    th    = TablaHashEncadenamiento(tamano=7)
    datos = [(10,"diez"), (17,"diec"), (3,"tres"),
             (24,"venti"), (31,"treinta"), (38,"treintaocho")]

    print("\n--- Insercion (colisiones intencionales mod 7) ---")
    for k, v in datos:
        th[k] = v
        print(f"  Insertado ({k}, '{v}')  hash={k%7}")
    print(f"\nTabla ({len(th)} elementos):\n{th}")

    print("\n--- Eliminacion ---")
    for k in [17, 99]:
        ok = th.eliminar(k)
        print(f"  eliminar({k}) = {'OK' if ok else 'No encontrado'}")
    print(f"\nTabla tras eliminar ({len(th)} elementos):\n{th}")

    print("\n--- Verificacion busqueda post-eliminacion ---")
    for k in [10, 17, 24]:
        print(f"  obtener({k}) = {th[k]}")


def probar_abierta():
    print("\n" + "=" * 60)
    print(" DIRECCIONAMIENTO ABIERTO — Eliminacion con Tombstone")
    print("=" * 60)
    th    = TablaHashAbierta(tamano=11)
    datos = [(54,"A"), (26,"B"), (93,"C"), (17,"D"),
             (77,"E"), (31,"F"), (44,"G")]

    print("\n--- Insercion ---")
    for k, v in datos:
        th[k] = v
        print(f"  Insertado ({k}, '{v}')  slot={k%11}")

    # Colision: 65%11=10 == 54%11=10
    th[65] = "H"
    print(f"\n  Insertado (65,'H') -> slot={65%11} (colisiona con 54%11={54%11})")
    print(f"\nTabla ({len(th)} elementos):\n{th}")

    print(f"\n--- Antes de eliminar 54: obtener(65) = {th[65]} ---")
    th.eliminar(54)
    print(f"  Eliminado 54 (slot marcado como <ELIMINADO>)")
    print(f"  Tabla:\n{th}")
    print(f"  obtener(65) = {th[65]}  <- debe seguir funcionando")

    print("\n--- Eliminar varios y reinsertar ---")
    th.eliminar(26); th.eliminar(93)
    print(f"  Eliminados 26 y 93. len={len(th)}")
    th[26] = "B_nuevo"
    print(f"  Reinsertado (26,'B_nuevo') reutilizando tombstone")
    print(f"  Tabla ({len(th)} elementos):\n{th}")


if __name__ == "__main__":
    print("=" * 60)
    print(" EJERCICIO 16: Eliminar en Tablas Hash")
    print("=" * 60)
    print("""
RESPUESTA A LAS PREGUNTAS DEL ENUNCIADO:

Encadenamiento:
  Eliminar = quitar el nodo de la lista enlazada del slot.
  Sin efectos secundarios: la busqueda en ese slot sigue ok.
  Coste: O(1 + lambda)

Direccionamiento abierto:
  NO se puede poner None: romperia las cadenas de sondeo.
  Solucion: centinela ELIMINADO (tombstone).
    - Busqueda: salta tombstones, continua sondeando.
    - Insercion: reutiliza un slot tombstone.
  Circunstancias especiales:
    * Tombstones ocupan espacio -> degradan el rendimiento.
    * Si hay muchos tombstones, conviene rehashear la tabla.
    * El factor de carga debe contar tombstones como ocupados.
""")
    probar_encadenamiento()
    probar_abierta()

    print("\n" + "=" * 60)
    print(" COSTE:")
    print("  Encadenamiento:   O(1 + lambda)")
    print("  Dir. abierto:     O(1/(1-lambda)) promedio")
    print("=" * 60)
