import random

class QuikSort:
    def __init__(self, unaLista):
        self.unaLista = unaLista

    def ordenamientoRapido(self):
        self.ordenamientoRapidoAuxiliar(self.unaLista, 0, len(self.unaLista) - 1)

    def ordenamientoRapidoAuxiliar(self, unaLista, primero, ultimo):
        if primero < ultimo:
            puntoDivision = self.particion(unaLista, primero, ultimo)
            self.ordenamientoRapidoAuxiliar(unaLista, primero, puntoDivision - 1)
            self.ordenamientoRapidoAuxiliar(unaLista, puntoDivision + 1, ultimo)

    # --- NUEVO MÉTODO: Dedicado solo a elegir el pivote ---
    def seleccionar_indice_pivote(self, unaLista, primero, ultimo):
        """Por defecto, elige el primer elemento (comportamiento original)"""
        return primero

    def particion(self, unaLista, primero, ultimo):
        # 1. Las clases hijas decidirán qué índice usar llamando a este método
        indice_pivote = self.seleccionar_indice_pivote(unaLista, primero, ultimo)
        
        # 2. Intercambiamos el pivote elegido con el primer elemento.
        # Esto nos permite usar tu lógica original sin romper nada.
        unaLista[primero], unaLista[indice_pivote] = unaLista[indice_pivote], unaLista[primero]
        
        valorPivote = unaLista[primero]
        marcaIzq = primero + 1
        marcaDer = ultimo
        hecho = False
    
        while not hecho:
            while marcaIzq <= marcaDer and unaLista[marcaIzq] <= valorPivote:
                marcaIzq += 1
            while unaLista[marcaDer] >= valorPivote and marcaDer >= marcaIzq:
                marcaDer -= 1
            
            if marcaDer < marcaIzq:
                hecho = True
            else:
                unaLista[marcaIzq], unaLista[marcaDer] = unaLista[marcaDer], unaLista[marcaIzq]
        
        unaLista[primero], unaLista[marcaDer] = unaLista[marcaDer], unaLista[primero]
        return marcaDer
    
class QuikSortUltimo(QuikSort):
    """Elige siempre el último elemento como pivote"""
    def seleccionar_indice_pivote(self, unaLista, primero, ultimo):
        return ultimo

class QuikSortMedio(QuikSort):
    """Elige siempre el elemento del medio como pivote"""
    def seleccionar_indice_pivote(self, unaLista, primero, ultimo):
        return (primero + ultimo) // 2

class QuikSortAleatorio(QuikSort):
    """Elige un elemento aleatorio como pivote (Evita el peor caso de O(n^2))"""
    def seleccionar_indice_pivote(self, unaLista, primero, ultimo):
        return random.randint(primero, ultimo)