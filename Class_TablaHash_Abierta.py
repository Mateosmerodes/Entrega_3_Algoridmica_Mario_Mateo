"""
Class_TablaHash_Abierta.py
---------------------------
Dos implementaciones de tabla hash con direccionamiento abierto:

  TablaHashAbierta   — tamano fijo, con tombstone para borrado.
  TablaHashDinamica  — redimension automatica al siguiente primo
                       >= 2*tamano cuando lambda >= umbral.

Ambas usan sondeo lineal y el centinela _ELIMINADO (tombstone)
para que el borrado no rompa las cadenas de sondeo.

Coste operaciones:
  Insertar/buscar/eliminar : O(1/(1-lambda)) promedio
  __len__                  : O(1)  (contador separado _count)
  Redimension (Dinamica)   : O(n) puntual, O(1) amortizado
"""


# ── Utilidades primos (usadas por TablaHashDinamica) ────────

def _es_primo(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0: return False
    return True


def _siguiente_primo(n):
    """Devuelve el primer primo >= n."""
    while not _es_primo(n):
        n += 1
    return n


# ── Centinela compartido ─────────────────────────────────────
_ELIMINADO = object()


# ══════════════════════════════════════════════════════════════
# TablaHashAbierta — tamano fijo con tombstone
# ══════════════════════════════════════════════════════════════

class TablaHashAbierta:
    """
    Tabla hash con direccionamiento abierto (sondeo lineal) y
    centinela ELIMINADO para no romper cadenas de sondeo al borrar.

    Al buscar  : se salta _ELIMINADO y se continua sondeando.
    Al insertar: se puede reutilizar un slot _ELIMINADO.
    """

    def __init__(self, tamano=11):
        self.tamano = tamano
        self.slots  = [None] * self.tamano
        self.datos  = [None] * self.tamano
        self._count = 0

    def _hash(self, clave):
        return clave % self.tamano

    def _rehash(self, pos):
        return (pos + 1) % self.tamano

    def agregar(self, clave, dato):
        idx           = self._hash(clave)
        pos           = idx
        primer_tomb   = None

        for _ in range(self.tamano):
            if self.slots[pos] is None:
                destino = primer_tomb if primer_tomb is not None else pos
                self.slots[destino] = clave
                self.datos[destino] = dato
                self._count += 1
                return
            elif self.slots[pos] is _ELIMINADO:
                if primer_tomb is None:
                    primer_tomb = pos
            elif self.slots[pos] == clave:
                self.datos[pos] = dato   # actualizar
                return
            pos = self._rehash(pos)

        if primer_tomb is not None:
            self.slots[primer_tomb] = clave
            self.datos[primer_tomb] = dato
            self._count += 1

    def obtener(self, clave):
        idx = self._hash(clave)
        pos = idx
        for _ in range(self.tamano):
            if self.slots[pos] is None:
                return None
            if self.slots[pos] is not _ELIMINADO and self.slots[pos] == clave:
                return self.datos[pos]
            pos = self._rehash(pos)
        return None

    def eliminar(self, clave):
        """
        Marca el slot con _ELIMINADO (tombstone).
        La busqueda salta tombstones pero continua; la insercion
        puede reutilizarlos.
        """
        idx = self._hash(clave)
        pos = idx
        for _ in range(self.tamano):
            if self.slots[pos] is None:
                return False
            if self.slots[pos] is not _ELIMINADO and self.slots[pos] == clave:
                self.slots[pos] = _ELIMINADO
                self.datos[pos] = None
                self._count    -= 1
                return True
            pos = self._rehash(pos)
        return False

    def __setitem__(self, clave, dato):
        self.agregar(clave, dato)

    def __getitem__(self, clave):
        return self.obtener(clave)

    def __len__(self):
        return self._count      # O(1)

    def __str__(self):
        lineas = []
        for i in range(self.tamano):
            s = self.slots[i]
            if s is None:
                lineas.append(f"  [{i:3}] None")
            elif s is _ELIMINADO:
                lineas.append(f"  [{i:3}] <ELIMINADO>")
            else:
                lineas.append(f"  [{i:3}] {s} -> {self.datos[i]}")
        return "\n".join(lineas)


# ══════════════════════════════════════════════════════════════
# TablaHashDinamica — redimension automatica
# ══════════════════════════════════════════════════════════════

class TablaHashDinamica:
    """
    Tabla hash con direccionamiento abierto y redimension automatica.

    Cuando factor_de_carga >= umbral se expande al siguiente primo
    >= 2 * tamano_actual y se re-insertan todos los elementos.

    Coste:
      Insertar (amortizado) : O(1)
      Buscar                : O(1/(1-lambda)) promedio
      Redimension           : O(n) puntual
      __len__               : O(1)
    """

    def __init__(self, tamano_inicial=11, umbral=0.75):
        self.tamano   = tamano_inicial
        self.umbral   = umbral
        self.slots    = [None] * self.tamano
        self.datos    = [None] * self.tamano
        self._count   = 0
        self._resizes = 0       # contador de redimensiones

    @property
    def factor_carga(self):
        return self._count / self.tamano

    def _hash(self, clave):
        return clave % self.tamano

    def _rehash(self, pos):
        return (pos + 1) % self.tamano

    def _redimensionar(self):
        nuevo_tamano = _siguiente_primo(2 * self.tamano)
        print(f"  [REDIMENSION] {self.tamano} -> {nuevo_tamano}  "
              f"(lambda={self.factor_carga:.2f} >= {self.umbral})")
        slots_ant, datos_ant = self.slots, self.datos
        self.tamano  = nuevo_tamano
        self.slots   = [None] * nuevo_tamano
        self.datos   = [None] * nuevo_tamano
        self._count  = 0
        self._resizes += 1
        for i, k in enumerate(slots_ant):
            if k is not None and k is not _ELIMINADO:
                self.agregar(k, datos_ant[i])

    def agregar(self, clave, dato):
        if self._count / self.tamano >= self.umbral:
            self._redimensionar()
        idx         = self._hash(clave)
        pos         = idx
        primer_tomb = None

        for _ in range(self.tamano):
            if self.slots[pos] is None:
                destino = primer_tomb if primer_tomb is not None else pos
                self.slots[destino] = clave
                self.datos[destino] = dato
                self._count += 1
                return
            elif self.slots[pos] is _ELIMINADO:
                if primer_tomb is None:
                    primer_tomb = pos
            elif self.slots[pos] == clave:
                self.datos[pos] = dato
                return
            pos = self._rehash(pos)

        if primer_tomb is not None:
            self.slots[primer_tomb] = clave
            self.datos[primer_tomb] = dato
            self._count += 1

    def obtener(self, clave):
        idx = self._hash(clave)
        pos = idx
        for _ in range(self.tamano):
            if self.slots[pos] is None:
                return None
            if self.slots[pos] is not _ELIMINADO and self.slots[pos] == clave:
                return self.datos[pos]
            pos = self._rehash(pos)
        return None

    def eliminar(self, clave):
        idx = self._hash(clave)
        pos = idx
        for _ in range(self.tamano):
            if self.slots[pos] is None:
                return False
            if self.slots[pos] is not _ELIMINADO and self.slots[pos] == clave:
                self.slots[pos] = _ELIMINADO
                self.datos[pos] = None
                self._count    -= 1
                return True
            pos = self._rehash(pos)
        return False

    def __setitem__(self, clave, dato):
        self.agregar(clave, dato)

    def __getitem__(self, clave):
        return self.obtener(clave)

    def __len__(self):
        return self._count      # O(1)

    def info(self):
        return (f"Tamano={self.tamano}, Elementos={self._count}, "
                f"Lambda={self.factor_carga:.3f}, Redimensiones={self._resizes}")

    def __str__(self):
        lineas = []
        for i in range(self.tamano):
            s = self.slots[i]
            if s is None:
                lineas.append(f"  [{i:3}] None")
            elif s is _ELIMINADO:
                lineas.append(f"  [{i:3}] <ELIM>")
            else:
                lineas.append(f"  [{i:3}] {s} -> {self.datos[i]}")
        return "\n".join(lineas)
