import Operaciones as op

class Tablero():
    def __init__(self, di,opcion):
        self.Estado=1
        self.Ganador=0
        self.dificultad = di
        if self.dificultad == 1:
            self.m = 9
            self.n = 9
            self.minas = 10
            self.libres=(self.m*self.n)-self.minas
            self.abiertas = 0
            if opcion==1:
              self.tablero = op.creaMatriz(self.n, self.m, self.minas)
            elif opcion==0:
              self.tablero = op.Vacia(self.n, self.m,)
        elif self.dificultad == 2:
            self.m = 16
            self.n = 16
            self.minas = 40
            self.libres = (self.m * self.n) - self.minas
            self.abiertas=0
            if opcion==1:
              self.tablero = op.creaMatriz(self.n, self.m, self.minas)
            elif opcion == 0:
              self.tablero = op.Vacia(self.n, self.m,)

    def imprimir(self):
        print("  ",end='')
        for i in range(len(self.tablero[0])):
            print("\t",i+1, end="")
        print()
        print()
        for i in range(len(self.tablero)):
            print(i+1, end="")
            for j in range(len(self.tablero[i])):
                print("\t",str(self.tablero[i][j],'utf-8'), end=' ')
            print()

    def isMina(self, x, y):

        if str(self.tablero[x-1][y-1],'utf-8')== 'X':
         return 1
        else:
         return 0

    def destaparM(self,x,y):
        self.tablero[x-1][y-1] = 'X'
    def destapar(self,x,y):
        self.tablero[x-1][y-1] = 'O'

    def Juego(self):
        return self.Estado and 1
    def cEstado(self,e):
        self.Estado=e

    def getGanador(self):
        self.Ganador

    def  isAbierta (self,x,y):

        if str(self.tablero[x-1][y-1]) == str("*"):
            return 0
        else:
            return 1

2











