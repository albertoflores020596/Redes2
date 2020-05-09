import socket
import threading
import logging
from pathlib import Path
import time
from TFTP import *
from os import listdir
from os.path import isfile, join
bufferSize = 512
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-2s) %(message)s',)

def ls(ruta = 'imgS/.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]


def servirPorSiempre(TFTP,UDPServerSocket,):
    print("servirdor listo para atender clientes")
    try:
        while True:
            Paquete, addr = UDPServerSocket.recvfrom(bufferSize)  # buffer size is 1024 bytes
            thread_read = threading.Thread(name='Server', target=Atender, args=[UDPServerSocket,TFTP, addr,Paquete])
            thread_read.start()
    except Exception as e:
        print(e)

def Atender(UDP,TFTP,conn,Paquete):
    Paquete=str(Paquete.decode('utf-8'))
    #logging.debug('Atendiendo peticion de cliente')
    op=TFTP.Identificar(Paquete)
    if int(op)==1:
        img = Paquete[1:len(Paquete)]
        fileName = "imgS/"+ str(img)
        fileObj = Path(fileName)
        if fileObj.is_file():
            Mensaje = TFTP.C3(img)
            logging.debug('Mandando  Paquete Datos Codigo 3:')
            UDP.sendto(str(Mensaje).encode('utf-8'), conn)
            time.sleep(1)
            Mensaje = TFTP.C4()
            logging.debug('Mandando  Paquete AKC codigo 4:')
            UDP.sendto(str(Mensaje).encode('utf-8'), conn)
        else:
            Mensaje = TFTP.C5(img,1,"No exite fichero")
            logging.debug('Mandando  Paquete Error codigo 5: ,tipo de error 1:No exite fichero')
            UDP.sendto(str(Mensaje).encode('utf-8'), conn)
            Paquete, addr = UDPServerSocket.recvfrom(bufferSize)
            Paquete = str(Paquete.decode('utf-8'))
            TFTP.Identificar(Paquete)
    elif int(op)==2:
        img = Paquete[1:len(Paquete)]
        fileName = "imgS/" + str(img)
        fileObj = Path(fileName)
        if fileObj.is_file():
            Mensaje = TFTP.C5(img, 6, "Archivo ya existe")
            logging.debug('Mandando  Paquete Error codigo 5: ,tipo de error 6:Fichero ya existe')
            UDP.sendto(str(Mensaje).encode('utf-8'), conn)
        else:
            Mensaje = TFTP.C4()
            logging.debug('Mandando  Paquete AKC codigo 4: ')
            UDP.sendto(str(Mensaje).encode('utf-8'), conn)
            Paquete, addr = UDPServerSocket.recvfrom(bufferSize)
            Paquete = str(Paquete.decode('utf-8'))
            TFTP.Identificar(Paquete)


    elif int(op) == 9:
        Mensaje = TFTP.C5("error", 0, "No definido")
        logging.debug('Mandando  Paquete Error codigo : 5 ,tipo de error 4:Operacion TFTP Ilegal')
        UDP.sendto(str(Mensaje).encode('utf-8'), conn)
    else:
        Mensaje = TFTP.C5("error", 4, "Operacion TFTP Ilegal")
        logging.debug('Mandando  Paquete Error codigo : 5 ,tipo de error 4:Operacion TFTP Ilegal')
        UDP.sendto(str(Mensaje).encode('utf-8'), conn)



HOST = 'localhost'
PORT = 54321  # The port used by the server

with  socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    TFTP = protocoloTFTP()
    servirPorSiempre(TFTP,UDPServerSocket,)



