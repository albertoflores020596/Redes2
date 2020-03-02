# !/usr/bin/env python3

import socket
import sys
import threading
from Tablero import *

def servirPorSiempre(socketTcp, listaconexiones):
    BuscaminasF = Tablero(1, 1)
    BuscaminasD = Tablero(2, 1)
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            listaconexiones.append(client_conn)
            Dificultad = client_conn.recv(bufferSize)
            print("Conectado a", client_addr)
            print("Iniciando Juego nuevo")
            if int(Dificultad)==1:
                thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr, BuscaminasF])
            else:
                thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr, BuscaminasD])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)


def recibir_datos(sc, addr,Buscaminas):
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:

            while Buscaminas.Estado == 1:
                Buscaminas.imprimir()
                X = sc.recv(bufferSize)
                Y = sc.recv(bufferSize)

                if Buscaminas.isMina(int(X), int(Y)):
                    Buscaminas.Estado = 0
                    Buscaminas.Ganador = 0
                    r = '1'
                    sc.send(r.encode('utf-8'))
                else:
                    r = '0'
                    sc.send(r.encode('utf-8'))
                Buscaminas.abiertas += 1
                if Buscaminas.libres == Buscaminas.abiertas:
                    Buscaminas.Estado = 0
                    Buscaminas.Ganador == 1;

            print("JUego Terminado")

            if Buscaminas.Ganador == 1:
                print("!!Jugador Gano!!  (°u°)b")
            else:
                print("!!Jugador Perdio!!  (°n°)p")
            break
        sc.close()


    except Exception as e:
        print(e)
    finally:
        sc.close()






listaConexiones = []
HOST = "8.40.1.120"  # The server's hostname or IP address
PORT = 54321  # The port used by the server
bufferSize = 1024
r='0'
UDPServerSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPServerSocket.bind((HOST, PORT))
UDPServerSocket.listen(3)
print("El servidor TCP está disponible y en espera de solicitudes")

servirPorSiempre(UDPServerSocket, listaConexiones)
