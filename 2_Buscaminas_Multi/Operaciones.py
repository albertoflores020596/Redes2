from random import *
import numpy as np

def creaMatriz(n , m , mi):
    matriz = np.chararray((n,m))
    matriz [:]='O'
    minas=mi
    while minas != 0:
     x = randint(0, n-1)
     y = randint(0, m-1)
     if matriz[x][y] != 'X':
         matriz[x][y] = 'X'
         minas -= 1
    return matriz


def Vacia(n,m):
        matriz = np.chararray((n, m))
        matriz[:] = '*'
        return matriz






