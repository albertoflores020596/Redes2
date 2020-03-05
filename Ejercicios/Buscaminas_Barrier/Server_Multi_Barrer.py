# !/usr/bin/env python3

import socket
from random import *
import threading
import time
from Tablero import *
bufferSize = 1024
listaConexiones = []
d = randint(1, 2)
Buscaminas = Tablero(d, 1)
NUM_THREADS = 5
threads =[]

def servirPorSiempre(socketTcp, listaconexiones,barrier):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            listaconexiones.append(client_conn)
            print("Conectado a", client_addr)
            client_conn.send(str(d).encode('utf-8'))
            threads =threading.Thread(name='Jugador', target=recibir_datos,args=[barrier, client_conn, client_addr],)
            threads.start()
            print()
            #Buscaminas.imprimir()
    except Exception as e:
        print(e)


def ActualizarJugada(X,Y):
      for conn in listaConexiones:
          print("Actualizando Jugada a clientes")
          if conn.fileno() == -1:
              listaConexiones.remove(conn)
          if Buscaminas.isMina(X,Y)==1:
               Respuesta='1'+' '+str(X)+' '+str(Y)+' '+'1'+' '+'0'
               conn.send(Respuesta.encode('utf-8'))
          elif Buscaminas.isMina(X,Y)==0:
               Respuesta='0'+' '+str(X)+' '+str(Y)+' '+'1'+' '+'0'
               conn.send(Respuesta.encode('utf-8'))



def recibir_datos(barrier,sc, addr):
    print(threading.current_thread().name,'Esperando,con {} jugadores más'.format(barrier.n_waiting))
    Jugador_id = barrier.wait()
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo Jugada del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
           X = sc.recv(bufferSize)
           Y = sc.recv(bufferSize)
           ActualizarJugada(int(X),int(Y))
    except Exception as e:
         print(e)


#HOST = "192.168.0.5"
HOST = 'localhost'
PORT = 54321  # The port used by the server
r='0'
UDPServerSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPServerSocket.bind((HOST, PORT))
UDPServerSocket.listen(10)
barrier = threading.Barrier(NUM_THREADS)
print("El servidor está disponible y en espera de solicitudes")
servirPorSiempre(UDPServerSocket, listaConexiones,barrier)
UDPServerSocket.close()
