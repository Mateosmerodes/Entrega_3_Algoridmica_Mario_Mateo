"""
Class_ListaOrdenada_Mapa.py
-----------------------------
Lista enlazada ordenada de pares (clave, dato) para usarse como
estructura interna del TAD Mapa con encadenamiento.

Metodos:
  tamano()       O(1)   - contador separado _tam
  insertar()     O(n)   - mantiene orden ascendente por clave
  buscar()       O(n)
  borrar()       O(n)
  indice(pos)    O(n)   - devuelve (clave, dato) en posicion pos
  extraer(pos=0) O(n)   - extrae el elemento en posicion pos
"""


class NodoPar:
    """Nodo que almacena un par (clave, dato) con enlace al siguiente."""

    def __init__(self, clave, dato):
        self.clave = clave
        self.dato  = dato
        self.sig   = None


class ListaOrdenadaMapa:
    """
    Lista enlazada ordenada ascendentemente por clave.
    Usada como cubeta en TablaHashEncadenada para el TAD Mapa.
    """

    def __init__(self):
        self._cabeza = None
        self._tam    = 0

    def tamano(self):
        """Devuelve el numero de elementos. O(1)."""
        return self._tam

    def insertar(self, clave, dato):
        """Inserta o actualiza (clave, dato) manteniendo orden. O(n)."""
        actual, previo = self._cabeza, None
        while actual and actual.clave < clave:
            previo  = actual
            actual  = actual.sig
        if actual and actual.clave == clave:
            actual.dato = dato   # actualizar
            return
        nuevo     = NodoPar(clave, dato)
        nuevo.sig = actual
        if previo:
            previo.sig = nuevo
        else:
            self._cabeza = nuevo
        self._tam += 1

    def buscar(self, clave):
        """Devuelve el dato asociado a clave, o None si no existe. O(n)."""
        actual = self._cabeza
        while actual:
            if actual.clave == clave:
                return actual.dato
            if actual.clave > clave:
                break
            actual = actual.sig
        return None

    def borrar(self, clave):
        """Elimina el nodo con esa clave. Devuelve True si existia. O(n)."""
        actual, previo = self._cabeza, None
        while actual:
            if actual.clave == clave:
                if previo:
                    previo.sig = actual.sig
                else:
                    self._cabeza = actual.sig
                self._tam -= 1
                return True
            if actual.clave > clave:
                break
            previo  = actual
            actual  = actual.sig
        return False

    def indice(self, pos):
        """Devuelve (clave, dato) en la posicion pos (0-indexado). O(n)."""
        actual = self._cabeza
        for _ in range(pos):
            if actual is None:
                raise IndexError(f"pos={pos} fuera de rango [0, {self._tam-1}]")
            actual = actual.sig
        if actual is None:
            raise IndexError(f"pos={pos} fuera de rango [0, {self._tam-1}]")
        return (actual.clave, actual.dato)

    def extraer(self, pos=0):
        """
        Extrae y devuelve (clave, dato) en la posicion pos. O(n).
        Por defecto extrae el primer elemento (pos=0).
        """
        if self._cabeza is None:
            return None
        actual, previo = self._cabeza, None
        for _ in range(pos):
            if actual.sig is None:
                raise IndexError(f"pos={pos} fuera de rango")
            previo  = actual
            actual  = actual.sig
        if previo:
            previo.sig = actual.sig
        else:
            self._cabeza = actual.sig
        self._tam -= 1
        return (actual.clave, actual.dato)

    def __str__(self):
        items, actual = [], self._cabeza
        while actual:
            items.append(f"({actual.clave}:{actual.dato})")
            actual = actual.sig
        return " -> ".join(items) if items else "(vacia)"
