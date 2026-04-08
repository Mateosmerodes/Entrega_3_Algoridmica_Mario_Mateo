"""
Class_Mapa.py
--------------
TAD Vector Asociativo (Mapa) en dos implementaciones:

  MapaAbierto     — Direccionamiento abierto con:
                    * __len__ O(1)
                    * eliminar con tombstone
                    * redimension al siguiente primo >= 2*tamano
                      cuando factor de carga >= 0.90

  MapaEncadenado  — Encadenamiento con ListaOrdenadaMapa:
                    * __len__ O(1)
                    * Todos los metodos del TAD Mapa
                    * Slots son listas enlazadas ordenadas

Importa:
  Class_ListaOrdenada_Mapa.ListaOrdenadaMapa
"""

from Class_ListaOrdenada_Mapa import ListaOrdenadaMapa


# ── Utilidades primos ────────────────────────────────────────

def _es_primo(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0: return False
    return True


def _siguiente_primo(n):
    while not _es_primo(n):
        n += 1
    return n


# ── Centinela tombstone ──────────────────────────────────────
_ELIM = object()


# ══════════════════════════════════════════════════════════════
# MapaAbierto
# ══════════════════════════════════════════════════════════════

class MapaAbierto:
    """
    TAD Mapa con direccionamiento abierto (sondeo lineal).

    - __len__  : O(1)
    - eliminar : tombstone _ELIM
    - agregar  : redimensiona al siguiente primo >= 2*tamano
                 cuando factor de carga >= 0.90
    """

    def __init__(self, tamano=11):
        self._tamano = tamano
        self._slots  = [None] * tamano
        self._datos  = [None] * tamano
        self._count  = 0

    def _hash(self, clave):
        return clave % self._tamano

    def _sondeo(self, pos):
        return (pos + 1) % self._tamano

    def _redimensionar(self):
        nuevo        = _siguiente_primo(2 * self._tamano)
        slots_ant    = self._slots
        datos_ant    = self._datos
        self._tamano = nuevo
        self._slots  = [None] * nuevo
        self._datos  = [None] * nuevo
        self._count  = 0
        for i, k in enumerate(slots_ant):
            if k is not None and k is not _ELIM:
                self[k] = datos_ant[i]

    def __setitem__(self, clave, dato):
        if self._count / self._tamano >= 0.90:
            self._redimensionar()
        idx        = self._hash(clave)
        pos        = idx
        first_tomb = None

        for _ in range(self._tamano):
            if self._slots[pos] is None:
                dest = first_tomb if first_tomb is not None else pos
                self._slots[dest] = clave
                self._datos[dest] = dato
                self._count += 1
                return
            elif self._slots[pos] is _ELIM:
                if first_tomb is None:
                    first_tomb = pos
            elif self._slots[pos] == clave:
                self._datos[pos] = dato
                return
            pos = self._sondeo(pos)

        if first_tomb is not None:
            self._slots[first_tomb] = clave
            self._datos[first_tomb] = dato
            self._count += 1

    def __getitem__(self, clave):
        idx = self._hash(clave)
        pos = idx
        for _ in range(self._tamano):
            if self._slots[pos] is None:
                return None
            if self._slots[pos] is not _ELIM and self._slots[pos] == clave:
                return self._datos[pos]
            pos = self._sondeo(pos)
        return None

    def __len__(self):
        return self._count      # O(1)

    def eliminar(self, clave):
        """Marca el slot con tombstone _ELIM. O(1/(1-lambda))."""
        idx = self._hash(clave)
        pos = idx
        for _ in range(self._tamano):
            if self._slots[pos] is None:
                return False
            if self._slots[pos] is not _ELIM and self._slots[pos] == clave:
                self._slots[pos] = _ELIM
                self._datos[pos] = None
                self._count -= 1
                return True
            pos = self._sondeo(pos)
        return False

    def contiene(self, clave):
        return self[clave] is not None

    def info(self):
        return (f"tamano={self._tamano}, elementos={self._count}, "
                f"lambda={self._count/self._tamano:.3f}")

    def __str__(self):
        lineas = []
        for i in range(self._tamano):
            s = self._slots[i]
            if s is None:
                lineas.append(f"  [{i:3}] None")
            elif s is _ELIM:
                lineas.append(f"  [{i:3}] <ELIM>")
            else:
                lineas.append(f"  [{i:3}] {s} -> {self._datos[i]}")
        return "\n".join(lineas)


# ══════════════════════════════════════════════════════════════
# MapaEncadenado
# ══════════════════════════════════════════════════════════════

class MapaEncadenado:
    """
    TAD Mapa con encadenamiento usando ListaOrdenadaMapa en cada slot.

    - __len__  : O(1) (contador global _count)
    - Los slots son ListaOrdenadaMapa: listas enlazadas ordenadas
      por clave con tamano O(1), borrar, indice, extraer(pos).
    """

    def __init__(self, tamano=11):
        self._tamano = tamano
        self._slots  = [ListaOrdenadaMapa() for _ in range(tamano)]
        self._count  = 0

    def _hash(self, clave):
        return clave % self._tamano

    def __setitem__(self, clave, dato):
        idx    = self._hash(clave)
        antes  = self._slots[idx].tamano()
        self._slots[idx].insertar(clave, dato)
        if self._slots[idx].tamano() > antes:
            self._count += 1    # nueva insercion (no actualizacion)

    def __getitem__(self, clave):
        return self._slots[self._hash(clave)].buscar(clave)

    def __len__(self):
        return self._count      # O(1)

    def eliminar(self, clave):
        idx = self._hash(clave)
        ok  = self._slots[idx].borrar(clave)
        if ok:
            self._count -= 1
        return ok

    def contiene(self, clave):
        return self[clave] is not None

    def indice(self, slot, pos):
        """Devuelve (clave, dato) en la posicion pos de la lista del slot. O(n)."""
        return self._slots[slot].indice(pos)

    def extraer_de_slot(self, slot, pos=0):
        """Extrae y devuelve (clave, dato) en posicion pos del slot dado. O(n)."""
        resultado = self._slots[slot].extraer(pos)
        if resultado is not None:
            self._count -= 1
        return resultado

    def info(self):
        return (f"tamano={self._tamano}, elementos={self._count}, "
                f"lambda={self._count/self._tamano:.3f}")

    def __str__(self):
        lineas = []
        for i, lst in enumerate(self._slots):
            if lst.tamano() > 0:
                lineas.append(f"  [{i:3}] {lst}")
        return "\n".join(lineas) if lineas else "  (tabla vacia)"
