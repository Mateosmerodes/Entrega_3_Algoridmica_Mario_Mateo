"""
Class_TablaHash_Encadenamiento.py
----------------------------------
Tabla hash con encadenamiento (chaining).
Cada slot almacena una lista enlazada de NodoClave(clave, dato).

Operaciones:
  agregar / __setitem__ : O(1 + lambda)
  obtener / __getitem__ : O(1 + lambda)
  eliminar              : O(1 + lambda)
  __len__               : O(1)
"""


class NodoClave:
    """Nodo de lista enlazada que almacena un par (clave, dato)."""

    def __init__(self, clave, dato):
        self.clave     = clave
        self.dato      = dato
        self.siguiente = None


class TablaHashEncadenamiento:
    """
    Tabla hash con encadenamiento.
    Cada slot contiene una lista enlazada de NodoClave ordenada
    por orden de insercion.

    Coste: insercion/borrado/busqueda O(1 + lambda) promedio,
           donde lambda = num_elementos / tamano_tabla.
    """

    def __init__(self, tamano=11):
        self.tamano = tamano
        self.slots  = [None] * self.tamano
        self._count = 0          # contador para __len__ en O(1)

    # ── hash ────────────────────────────────────────────────

    def _hash(self, clave):
        return clave % self.tamano

    # ── operaciones publicas ────────────────────────────────

    def agregar(self, clave, dato):
        """Inserta o actualiza la clave en la lista del slot correspondiente."""
        idx  = self._hash(clave)
        nodo = self.slots[idx]

        # Buscar si la clave ya existe -> actualizar
        while nodo:
            if nodo.clave == clave:
                nodo.dato = dato
                return
            nodo = nodo.siguiente

        # Insertar al frente de la lista
        nuevo           = NodoClave(clave, dato)
        nuevo.siguiente = self.slots[idx]
        self.slots[idx] = nuevo
        self._count    += 1

    def obtener(self, clave):
        """Devuelve el dato asociado a la clave, o None si no existe."""
        idx  = self._hash(clave)
        nodo = self.slots[idx]
        while nodo:
            if nodo.clave == clave:
                return nodo.dato
            nodo = nodo.siguiente
        return None

    def eliminar(self, clave):
        """
        Elimina la clave de la lista enlazada del slot.
        No genera problemas de sondeo: encadenamiento no usa sondeo.
        Devuelve True si se elimino, False si no existia.
        """
        idx    = self._hash(clave)
        nodo   = self.slots[idx]
        previo = None

        while nodo:
            if nodo.clave == clave:
                if previo:
                    previo.siguiente = nodo.siguiente
                else:
                    self.slots[idx] = nodo.siguiente
                self._count -= 1
                return True
            previo = nodo
            nodo   = nodo.siguiente
        return False

    def __setitem__(self, clave, dato):
        self.agregar(clave, dato)

    def __getitem__(self, clave):
        return self.obtener(clave)

    def __len__(self):
        return self._count      # O(1)

    def __str__(self):
        lineas = []
        for i, nodo in enumerate(self.slots):
            if nodo:
                items = []
                while nodo:
                    items.append(f"({nodo.clave}:{nodo.dato})")
                    nodo = nodo.siguiente
                lineas.append(f"  [{i}] -> " + " -> ".join(items))
        return "\n".join(lineas) if lineas else "  (tabla vacia)"
