import socket

import logging
import time
import threading
from os import listdir
from os.path import isfile, join
from TFTP import *
def ls(ruta = 'imgC/.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]
def ls2(ruta = 'imgS/.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]
bufferSize = 1024
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-2s) %(message)s',)

threading.current_thread().setName("Cliente")
HOST = 'localhost'
PORT = 54321
serverAddressPort = (HOST , 54321 )
TFTP=protocoloTFTP()
while True:
    op = input("\n\n1-Lectura Archivo\n2-Escritura Archivo\n\nSeleccione una operacion : ")
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
       if op == '':
            Mensaje = str('0').encode('utf-8')
            logging.debug('Mandando  Solicitud  codigo : ?')
            UDPClientSocket.sendto(Mensaje, serverAddressPort)
            r = UDPClientSocket.recvfrom(bufferSize)
            Mensaje = str(r[0].decode('utf-8'))
            TFTP.Identificar(Mensaje)
            logging.debug("Terminacion de transferencia Prematura ")
            break
       if int(op)==1:
           print("Los archivos disponibles son:\n")
           print(ls2())
           fil= input("\nEscriba el nombre del archivo que desea Descargar:  ")
           logging.debug('Mandando  Solicitud de Lectura codigo : 1 ')
           UDPClientSocket.sendto(str(TFTP.C1(fil)).encode('utf-8'), serverAddressPort)
           r =  UDPClientSocket.recvfrom(bufferSize)
           Mensaje =str(r[0].decode('utf-8'))
           if  int(TFTP.Identificar(Mensaje) )!=5:
               time.sleep(1)
               r =  UDPClientSocket.recvfrom(bufferSize)
               Mensaje =str(r[0].decode('utf-8'))
               TFTP.Identificar(Mensaje)
               logging.debug("Terminacion de transferencia Normal ")
               break
           else:
                logging.debug("Terminacion de transferencia Prematura ")
                break

       elif int(op)==2:

           print(str('\n'))
           print(ls())
           fil= input("\n\nEscriba el nombre del archivo que desea subir:  ")
           Mensaje=  str(TFTP.C2(fil)).encode('utf-8')
           logging.debug('Mandando  Solicitud de Escritura  codigo : 2')
           UDPClientSocket.sendto(Mensaje,serverAddressPort)
           r = UDPClientSocket.recvfrom(bufferSize)
           Mensaje = str(r[0].decode('utf-8'))
           if int(TFTP.Identificar(Mensaje)) == 4:
               Mensaje = str(TFTP.C3(fil)).encode('utf-8')
               logging.debug('Mandando  Paquete Datos Codigo : 3')
               UDPClientSocket.sendto(Mensaje, serverAddressPort)
               Mensaje = str(TFTP.C4()).encode('utf-8')
               logging.debug('Mandando  Paquete AKC codigo : 4')
               UDPClientSocket.sendto(Mensaje, serverAddressPort)
               logging.debug("Terminacion de transferencia Normal ")
               break
           else:
               logging.debug("Terminacion de transferencia Prematura ")
               break

       elif int(op) == 0:
           Mensaje = str('04').encode('utf-8')
           logging.debug('Mandando  Solicitud  codigo : 0')
           UDPClientSocket.sendto(Mensaje, serverAddressPort)
           r = UDPClientSocket.recvfrom(bufferSize)
           Mensaje = str(r[0].decode('utf-8'))
           #TFTP.Identificar(Mensaje)}
           logging.debug(Mensaje)
           logging.debug("Terminacion de transferencia Prematura ")
           break






