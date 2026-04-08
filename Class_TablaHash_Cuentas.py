"""
Class_TablaHash_Cuentas.py
---------------------------
Tabla hash especializada para almacenar y buscar cuentas bancarias
en formato string de 20 digitos.

Funcion hash: suma ponderada de caracteres con base 31.
Colisiones:   sondeo lineal con tombstone para borrado.
Redimension:  automatica al siguiente primo >= 2*tamano cuando lambda >= 0.75.

Coste:
  insertar / buscar / eliminar : O(1) promedio
  __len__                      : O(1)
"""


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


_ELIM = object()   # centinela tombstone


class TablaHashCuentas:
    """
    Tabla hash con direccionamiento abierto para cuentas bancarias.

    La clave es el numero de cuenta completo (string de 20 digitos).
    El dato es cualquier informacion del cliente asociada.

    Funcion hash: h = (h * 31 + ord(c)) % tamano  para cada caracter c.
    """

    def __init__(self, tamano=211):
        self._tam   = tamano
        self._slots = [None] * tamano
        self._datos = [None] * tamano
        self._count = 0

    def _hash(self, cuenta):
        """Hash polinomico en base 31 para cadenas."""
        h = 0
        for c in cuenta:
            h = (h * 31 + ord(c)) % self._tam
        return h

    def _rehash(self, pos):
        return (pos + 1) % self._tam

    def _redimensionar(self):
        nuevo       = _siguiente_primo(2 * self._tam)
        slots_ant   = self._slots
        datos_ant   = self._datos
        self._tam   = nuevo
        self._slots = [None] * nuevo
        self._datos = [None] * nuevo
        self._count = 0
        for i, k in enumerate(slots_ant):
            if k is not None and k is not _ELIM:
                self.insertar(k, datos_ant[i])

    def insertar(self, cuenta, cliente):
        """Inserta o actualiza la cuenta. Redimensiona si lambda >= 0.75."""
        if self._count / self._tam >= 0.75:
            self._redimensionar()
        idx  = self._hash(cuenta)
        pos  = idx
        tomb = None

        for _ in range(self._tam):
            if self._slots[pos] is None:
                dest = tomb if tomb is not None else pos
                self._slots[dest] = cuenta
                self._datos[dest] = cliente
                self._count += 1
                return True
            elif self._slots[pos] is _ELIM:
                if tomb is None:
                    tomb = pos
            elif self._slots[pos] == cuenta:
                self._datos[pos] = cliente
                return False    # actualizacion
            pos = self._rehash(pos)

        if tomb is not None:
            self._slots[tomb] = cuenta
            self._datos[tomb] = cliente
            self._count += 1
            return True
        return False

    def buscar(self, cuenta):
        """Devuelve el cliente asociado a la cuenta, o None si no existe."""
        idx = self._hash(cuenta)
        pos = idx
        for _ in range(self._tam):
            if self._slots[pos] is None:
                return None
            if self._slots[pos] is not _ELIM and self._slots[pos] == cuenta:
                return self._datos[pos]
            pos = self._rehash(pos)
        return None

    def eliminar(self, cuenta):
        """Marca el slot con tombstone. Devuelve True si existia."""
        idx = self._hash(cuenta)
        pos = idx
        for _ in range(self._tam):
            if self._slots[pos] is None:
                return False
            if self._slots[pos] is not _ELIM and self._slots[pos] == cuenta:
                self._slots[pos] = _ELIM
                self._datos[pos] = None
                self._count -= 1
                return True
            pos = self._rehash(pos)
        return False

    def __len__(self):
        return self._count      # O(1)

    def info(self):
        return (f"tamano={self._tam}, cuentas={self._count}, "
                f"lambda={self._count/self._tam:.3f}")
