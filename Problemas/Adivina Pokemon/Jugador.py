
from time import time
from Pokemon import *
import socket
import threading

class Juego():
    def __init__(self,id):
        self.Nombre=id
        self.Turno=0
        self.fin =False
        self.pj= Pokemon("", "", "?", "", "", "?", "")
    def Cambiar(self):
        self.Turno=not(self.Turno)

    def getTurno(self):
         return self.Turno

    def getNombre(self):
        return self.Nombre

    def cambiarF(self):
        self.fin = not (self.fin)

    def Error(self,dato):
         if int(dato) ==0:print("No Existe esa Categoria")

    def ver(self):
        print("Pokemon: pikachu charmander charizard chikorita articuno gastly gengar dragonite raichu alakazam    \n\n")
        print("Nombre: "+(self.pj.nombre))
        print("Tipo: " + (self.pj.tipo))
        print("Vuela: " + (self.pj.vuela))
        print("Color: " + (self.pj.color))
        print("Skill: " + (self.pj.skill))
        print("Evolucion: " + (self.pj.evolucion))
        print("Categoria: " + (self.pj.categoria))

    def Lnombre(self,rasgo):self.pj.nombre=str(rasgo) +": correcto"
    def Ltipo (self,rasgo): self.pj.tipo=str(rasgo) +": correcto"
    def Lvuela(self,rasgo):self.pj.vuela="Si-correcto"
    def Lcolor(self,rasgo): self.pj.color=str(rasgo) +": correcto"
    def Lskill(self,rasgo): self.pj.skill=str(rasgo) +": correcto"
    def Levolucion(self,rasgo): self.pj.evolucion="Si: correcto"
    def Lcategoria(self,rasgo): self.pj.categoria=str(rasgo) + ": correcto"

    def Anombre(self,rasgo):self.pj.nombre=self.pj.nombre+", "+str(rasgo) +": Incorrecto"
    def Atipo (self,rasgo): self.pj.tipo=self.pj.tipo+", "+str(rasgo) +": Incorrecto"
    def Avuela(self,rasgo):self.pj.vuela="No: correcto"
    def Acolor(self,rasgo): self.pj.color=self.pj.color+", "+str(rasgo) +": Incorrecto"
    def Askill(self,rasgo): self.pj.skill= self.pj.skill+", "+str(rasgo) +": Incorrecto"
    def Aevolucion(self,rasgo):self.pj.evolucion="No: Incorrecto"
    def Acategoria(self,rasgo): self.pj.categoria=self.pj.categoria+", "+str(rasgo) + ": Incorrecto"

    def Listo(self,rasgo,dato):

            if str(rasgo) == "nombre": return self.Lnombre(dato)
            if str(rasgo) == "tipo":   return self.Ltipo(dato)
            if str(rasgo) == "vuela": return self.Lvuela(dato)
            if str(rasgo) == "color": return self.Lcolor(dato)
            if str(rasgo) == "skill": return self.Lskill(dato)
            if str(rasgo) == "evolucion":return  self.Levolucion(dato)
            if str(rasgo) == "categoria": return self.Lcategoria(dato)
    def Agregar(self,rasgo,dato):

            if str(rasgo) == "nombre": return self.Anombre(dato)
            if str(rasgo) == "tipo":   return self.Atipo(dato)
            if str(rasgo) == "vuela": return self.Avuela(dato)
            if str(rasgo) == "color": return self.Acolor(dato)
            if str(rasgo) == "skill": return self.Askill(dato)
            if str(rasgo) == "evolucion":return  self.Aevolucion(dato)
            if str(rasgo) == "categoria": return self.Acategoria(dato)





def Manda(UDPClientSocket, Estado):
            r = input("\nAdivina el Pokemon: ")
            UDPClientSocket.send(str(r).encode('utf-8'))
            Estado.Cambiar()

def Escucha(UDPClientSocket, Estado):

        with UDPClientSocket:

            while not Estado.fin:
                Estado.Turno = int(UDPClientSocket.recv(bufferSize).decode('utf-8'))
                print()
                Estado.ver()
                if int(Estado.Turno) == int(Estado.Nombre):
                    Mandar = threading.Thread(target=Manda, args=[UDPClientSocket, Estado])
                    Mandar.start()
                else:
                    print("Es turno del Jugador " + str(Estado.Turno) + ". Espere su Turno...")
                    print()
                Respuesta = UDPClientSocket.recv(bufferSize).decode('utf-8')
                id,rasgo,dato,r=Respuesta.split(".")
                if int(r)>=0:
                    Estado.Listo(rasgo,dato);
                    print("El jugador " + str(id) + " : " + rasgo + " - " + dato + "  Fue CORRECTO")
                if int(r)==-1:
                    Estado.Agregar(rasgo,dato)
                    print("El jugador " + str(id) + " : "+ rasgo + " - " + dato + "  Fue INCORRECTO")
                if int(r)==-10:
                    print("El jugador " + str(id) + " : Adivino:  el pokemon es "+ dato )
                    print("fIN  DE juego  GANADOR : Jugador "+ str(id))
                    break

            while str(Respuesta) != "fin":
                Respuesta = UDPClientSocket.recv(bufferSize).decode('utf-8')

#HOST = "192.168.0.4"
HOST = 'localhost'
PORT = 8000
bufferSize = 1024
Inicio='0'
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPClientSocket.connect((HOST, PORT))
while True:
    Inicio = UDPClientSocket.recv(bufferSize).decode('utf-8')
    if str(Inicio) == "config":
        print("Bienvenido a ADIVINA POKEMON!! .. Configure la partida antes de iniciar \n\n")
        max = input("Ingresa el maximo de jugadores permitidos: ")
        Mensaje = str(max)
        UDPClientSocket.send(Mensaje.encode('utf-8'))
        UDPClientSocket.close()
        print("Configuracion con exito, presione enter, para continuar..")
        k = input()
        UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        UDPClientSocket.connect((HOST, PORT))
        if str(Inicio) == str('ok'):
            break
    elif str(Inicio) ==str('ok'):
        break
    else:
        print(Inicio)


UDPClientSocket.send(Inicio.encode('utf-8'))
respuesta = UDPClientSocket.recv(bufferSize).decode('utf-8')
id = respuesta
print("Jugadores Completos ,Iniciando Juego")
print(' ID jugador: ' + str(id))
tiempo_inicial = time()
Estado=Juego(int(id))
print("Hola, Bienvenido Jugador " + str(Estado.Nombre))
thread_read = threading.Thread(target=Escucha, args=[UDPClientSocket,Estado])
thread_read.start()

