# !/usr/bin/env python3

import socket
from random import *
import threading
import time
from Tablero import *
import logging
bufferSize = 1024
listaConexiones = []
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-2s) %(message)s',)



class Juego (object,):
    def __init__(self):
        self.Turnos = 1
        self.star=0
        self.max=0
        self.Dificultad=0
        self.fin=False;
        self.config=False

    def cambiarT(self):
        if int(self.Turnos)==int(self.max):
            self.Turnos=1;
        else:
            self.Turnos+=1

    def cambiarF(self):
        self.fin=not(self.fin)

def Iniciar(id, sc,game):
        r='null'
        while r!='ok':
            sc.send(str('ok').encode('utf-8'))
            r = str(sc.recv(bufferSize).decode('utf-8'))
        print('Jugador '+id +":listo ,Mandando Dificultad")
        mensaje=str(id)+' '+str(game.Dificultad)
        sc.send(str(mensaje).encode('utf-8'))
        game.star+=1


def Esperar (barrier,conn,nombre,game):
    while True:
         if int(barrier.n_waiting) == 0:
             break
         print('Esperando,con {} jugadores más'.format(barrier.n_waiting)+'. Faltan:'+str(int(game.max) -barrier.n_waiting)+' para iniciar...')
         Mensaje = 'Judador '+ str(nombre) + ': Esperando Jugadores, Faltan:'+str(int(game.max) - int(barrier.n_waiting))+' para iniciar...'
         conn.send(str(Mensaje).encode('utf-8'))
         time.sleep(1)
    print()
    Buscaminas.imprimir()

def servirPorSiempre(socketTcp, listaconexiones,game,lock,con,barrier,b):
    print("servirdor configurado.listo para experar jugadores")
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(name=barrier.n_waiting+1,target=recibir_datos, args=[barrier,client_conn, client_addr,game,lock,con,b])
            tEspera = threading.Thread(target=Esperar, args=[barrier, client_conn,barrier.n_waiting+1,game])
            thread_read.start()
            tEspera.start()
    except Exception as e:
        print(e)

def ActualizarJugada(X,Y,id,game):
      for conn in listaConexiones:
          print("Actualizando Jugada a Jugadores")
          if conn.fileno() == -1:
              listaConexiones.remove(conn)
          if Buscaminas.isMina(X,Y)==1:
               Respuesta='1'+' '+str(X)+' '+str(Y)+' '+'1'+' '+'0 '+str(id)
               conn.send(Respuesta.encode('utf-8'))
               game.cambiarF()
               print("MINA EXPLOTO!!, Perdedor jugador "+ id)
          elif Buscaminas.isMina(X,Y)==0:
               Respuesta='0'+' '+str(X)+' '+str(Y)+' '+'1'+' '+'0 '+str(id)
               conn.send(Respuesta.encode('utf-8'))



def ActualizarTurno(id):
    print("Actualizando Turno a Jugadores")
    for conn in listaConexiones:
        if conn.fileno() == -1:
            listaConexiones.remove(conn)
        conn.send(str(id).encode('utf-8'))

def recibir_datos(barrier,sc, addr,game,lock,con,b):
    id = threading.current_thread().name
    barrier.wait()
    Iniciar(id, sc, game)
    b.wait()
    while not game.fin:
        with con:
            while not int(game.Turnos)==int(id):
                     logging.debug("Jugador " + id + " :Esperando su turno...")
                     con.wait()
            if  not game.fin:
                logging.debug("Es turno del jugador : " + id)
                ActualizarTurno(id)
                X = sc.recv(bufferSize)
                Y = sc.recv(bufferSize)
                ActualizarJugada(int(X), int(Y),id,game)
                logging.debug('Jugador ' + id + ':Termino su jugada')
                game.cambiarT()
                con.notifyAll()

#HOST = "192.168.0.5"
HOST = 'localhost'
PORT = 54321  # The port used by the server
r='0'
UDPServerSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPServerSocket.bind((HOST, PORT))
UDPServerSocket.listen(5)
lock =threading.Lock()
con= threading.Condition()
print("El servidor TCP está disponible y en espera de solicitudes")
game = Juego()
if not game.config:
        print("Configurando partida")
        client_conn, client_addr = UDPServerSocket.accept()
        client_conn.send(str("config").encode('utf-8'))
        Respuesta =  client_conn.recv(bufferSize).decode('utf-8')
        game.max,game.Dificultad = Respuesta.split(' ')
        print("dificultad: " + game.Dificultad + " Jugadores max: " + game.max)
        game.config=not(game.config)
        client_conn.close()
        UDPServerSocket.close()

UDPServerSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPServerSocket.bind((HOST, PORT))
UDPServerSocket.listen(5)
b = threading.Barrier(int(game.max))
barrier = threading.Barrier(int(game.max))
Buscaminas = Tablero(int(game.Dificultad), 1)
servirPorSiempre(UDPServerSocket, listaConexiones,game,lock,con,barrier,b)
UDPServerSocket.close()
