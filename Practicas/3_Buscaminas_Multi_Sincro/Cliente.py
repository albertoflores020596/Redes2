#!/usr/bin/env python3
from time import time
from Tablero import *
import socket
import threading

class Juego():
    def __init__(self,id):
        self.Nombre=id
        self.Turno=0
        self.fin =False
    def Cambiar(self):
        self.Turno=not(self.Turno)

    def getTurno(self):
         return self.Turno

    def getNombre(self):
        return self.Nombre

    def cambiarF(self):
        self.fin = not (self.fin)

def Manda(UDPClientSocket,Estado):

            XY = input("\nIngresa las cordenadas de la casilla que quieres destapar: (X Y):  ")
            X, Y = XY.split(' ')
            UDPClientSocket.send(X.encode('utf-8'))
            UDPClientSocket.send(Y.encode('utf-8'))
            Estado.Cambiar()

def escuchaTablero(UDPClientSocket,Estado):

        with UDPClientSocket:

            while not Estado.fin:
                 Estado.Turno = int(UDPClientSocket.recv(bufferSize).decode('utf-8'))
                 print()
                 if int(Estado.Turno) == int(Estado.Nombre):
                    print("BUSCAMINAS")
                    Buscaminas.imprimir()
                    Mandar = threading.Thread(target=Manda, args=[UDPClientSocket,Estado])
                    Mandar.start()
                 else:
                    print("Es turno del Jugador " + str(Estado.Turno) + ". Espere su Turno...")
                    print()
                 Respuesta = UDPClientSocket.recv(bufferSize).decode('utf-8')
                 mina, X, Y, Juego, Ganador ,Gjugador= Respuesta.split(' ')
                 if int(mina) == 1:
                     Buscaminas.destaparM(int(X), int(Y))
                     Buscaminas.imprimir()
                     print("\n ╚(•⌂•)╝\n")
                     print("GAME OVER")
                     print("El Jugador "+str(Gjugador) +":    Perdio （╯‵□′）╯︵┴─┴")
                     tiempo_final = time()
                     tiempo_ejecucion = tiempo_final - tiempo_inicial
                     print("El tiempo de juego: ", tiempo_ejecucion)
                     Estado.cambiarF()
                 else:
                     print("\n  ٩(๑╹ ꇴ╹)۶\n")
                     print("NO ES MINA!!! ,  ╭（′▽‵）╭（′▽‵）╭（′▽‵）╯　　")
                     print("\n\nTermino tu turno")
                     Buscaminas.destapar(int(X), int(Y))

            while str(Respuesta)!="fin":
                  Respuesta = UDPClientSocket.recv(bufferSize).decode('utf-8')





#HOST = "192.168.0.5"
HOST = 'localhost'
PORT = 54321
bufferSize = 1024
Inicio='0'
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPClientSocket.connect((HOST, PORT))
while True:
    Inicio = UDPClientSocket.recv(bufferSize).decode('utf-8')
    if str(Inicio) == "config":
        print("Bienvenido a BUSCAMINAS.. Configure la partida antes de iniciar \n\n")
        max = input("Ingresa el maximo de jugadores permitidos: ")
        d = input("\nLa dificultad:\n 1.) Facil (9X9).\n 2.) Dificil (16x16)\n\n Elegie la dificultad: ")
        Mensaje = str(max + ' ' + d)
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
id, Dificultad = respuesta.split(' ')
print("Jugadores Completos ,Iniciando Juego")
print('Se recibio Dificultad: ' + str(Dificultad) + ' ID jugador: ' + str(id))
Buscaminas=Tablero(int(Dificultad),0)
tiempo_inicial = time()
Estado=Juego(int(id))
print("Hola, Bienvenido Jugador " + str(Estado.Nombre))
thread_read = threading.Thread(target=escuchaTablero, args=[UDPClientSocket,Estado])
thread_read.start()


