# Tema4_17
import time
import random

#escojemos un pivote( el primer elemento) y se coloca en su posicion definitiva
def particion(unaLista, primero, ultimo):
    valorPivote = unaLista[primero]

    marcaIzq = primero+1
    marcaDer = ultimo

    hecho = False
    while not hecho:

        while marcaIzq <= marcaDer and unaLista[marcaIzq] <= valorPivote:
            marcaIzq = marcaIzq + 1

        while unaLista[marcaDer] >= valorPivote and marcaDer >= marcaIzq:
            marcaDer = marcaDer - 1

        if marcaDer < marcaIzq:
            hecho = True
        else:
            unaLista[marcaIzq],unaLista[marcaDer] = unaLista[marcaDer],unaLista[marcaIzq]

    unaLista[primero],unaLista[marcaDer] = unaLista[marcaDer],unaLista[primero]

    return marcaDer

#le pasamos una copia para no modificar el vectro original
def seleccionarK(V, k):
    copia = V[:]  # no modificar el original
    return seleccionarKAux(copia, 0, len(copia)-1, k)


def seleccionarKAux(lista, primero, ultimo, k):
    if primero <= ultimo:

        puntoDivision = particion(lista, primero, ultimo)

        if puntoDivision == k:
            return lista[puntoDivision]

        elif k < puntoDivision:
            return seleccionarKAux(lista, primero, puntoDivision-1, k)

        else:
            return seleccionarKAux(lista, puntoDivision+1, ultimo, k)

#vreamos una lista de numeros aleatorios
unaLista = []
for i in range (2000):
    unaLista.append(random.randint(0, 100))
print(f'{unaLista}')
# mediana
k = 3

inicio=time.time()   #cronometramos
print("Buscando la posición 4: ")
print(seleccionarK(unaLista, k))
fin=time.time()
print(f'Complejidad temporal: {fin-inicio}')
