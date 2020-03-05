#!/usr/bin/env python3
from time import time
from Tablero import *
import socket
import threading



def Manda(UDPClientSocket):
    try:

            XY = input("\nIngresa las cordenadas de la casilla que quieres destapar: (X Y):  ")
            X, Y = XY.split(' ')
            UDPClientSocket.send(X.encode('utf-8'))
            UDPClientSocket.send(Y.encode('utf-8'))
    except Exception as e:
        print(e)

def escuchaTablero(UDPClientSocket):

    try:
        while True:
             print("BUSCAMINAS")
             print()
             Buscaminas.imprimir()
             print()
             print()
             Mandar = threading.Thread(target=Manda, args=[UDPClientSocket])
             Mandar.start()
             print()
             Respuesta = UDPClientSocket.recv(bufferSize)
             Respuesta = Respuesta.decode('utf-8')
             mina, X, Y, Juego, Gnador = Respuesta.split(' ')
             ##print("Se recibio :",repr(Respuesta),X,Y)

             if int(mina) == 1:

                 Buscaminas.destaparM(int(X), int(Y))
                 Buscaminas.imprimir()
                 print("Perdio (°°)-p!!!")
                 tiempo_final = time()
                 tiempo_ejecucion = tiempo_final - tiempo_inicial
                 print("El tiempo de juego: ", tiempo_ejecucion)
                 UDPClientSocket.close()
                 break
             else:
                 Buscaminas.destapar(int(X), int(Y))
    except Exception as e:
        print(e)


#HOST=input("Bienvenido a BUSCAMINAS\nIngresa el ip del Servidor: ")
#PORT=input("\nIngresa el puerto del servidor: ")
#HOST = "192.168.0.5"
HOST = 'localhost'
PORT = 54321
bufferSize = 1024

UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPClientSocket.connect((HOST, PORT))
print("Conectado al Servidor")

Dificultad = UDPClientSocket.recv(bufferSize)
Buscaminas=Tablero(int(Dificultad),0)
tiempo_inicial = time()
thread_read = threading.Thread(target=escuchaTablero, args=[UDPClientSocket])
thread_read.start()

