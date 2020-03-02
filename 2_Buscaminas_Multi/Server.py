import socket
from Tablero import *

HOST = "192.168.56.1"  # The server's hostname or IP address
PORT = 54321  # The port used by the server
bufferSize = 1024
r='0'
UDPServerSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPServerSocket.bind((HOST, PORT))
UDPServerSocket.listen(1)

print("Servidor Iniciado,Esperando Cliente")

while (True):
        #address = UDPServerSocket.recvfrom(bufferSize)
        sc, addr = UDPServerSocket.accept()
        print("Jugador Conectado")

        Dificultad = sc.recv(bufferSize)
        print("Iniciando Juego nuevo")
        Buscaminas = Tablero(int(Dificultad),1)

        while   Buscaminas.Estado == 1:
                        Buscaminas.imprimir()
                        X= sc.recv(bufferSize)
                        Y = sc.recv(bufferSize)

                        if Buscaminas.isMina(int(X),int(Y)):
                                Buscaminas.Estado=0
                                Buscaminas.Ganador=0
                                r= '1'
                                sc.send(r.encode('utf-8'))
                        else:
                                r = '0'
                                sc.send(r.encode('utf-8'))
                        Buscaminas.abiertas+=1
                        if Buscaminas.libres == Buscaminas.abiertas:
                                Buscaminas.Estado = 0
                                Buscaminas.Ganador == 1;





        print("JUego Terminado")

        if Buscaminas.Ganador==1:
                print("!!Jugador Gano!!  (°u°)b")
        else:
                print("!!Jugador Perdio!!  (°n°)p")
        sc.close()







