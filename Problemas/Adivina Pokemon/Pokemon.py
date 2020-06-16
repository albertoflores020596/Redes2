import random

class Pokemon:

    def __init__(self, n, t, v, c, s, e, ca):
        self.nombre = n
        self.tipo = t
        self.vuela = str(v)
        self.color = c
        self.skill = s
        self.evolucion = str(e)
        self.categoria = ca

    def getNombre(self):
        return self.nombre

    def Cnombre(self,rasgo):return rasgo.find(self.nombre)
    def Ctipo (self,rasgo): return rasgo.find(self.tipo)
    def Cvuela(self,rasgo): return str(rasgo).find(self.vuela)
    def Ccolor(self,rasgo): return rasgo.find(self.color)
    def Cskill(self,rasgo): return rasgo.find(self.skill)
    def Cevolucion(self,rasgo): return str(rasgo).find(self.evolucion)
    def Ccategoria(self,rasgo): return rasgo.find(self.categoria)

    def Comparar(self,rasgo,dato):

            if str(rasgo) == "nombre": return self.Cnombre(dato)
            if str(rasgo) == "tipo":   return self.Ctipo(dato)
            if str(rasgo) == "vuela": return self.Cvuela(dato)
            if str(rasgo) == "color": return self.Ccolor(dato)
            if str(rasgo) == "skill": return self.Cskill(dato)
            if str(rasgo) == "evolucion":return  self.Cevolucion(dato)
            if str(rasgo) == "categoria": return self.Ccategoria(dato)



















