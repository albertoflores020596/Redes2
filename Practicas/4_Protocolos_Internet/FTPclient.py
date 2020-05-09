import socket
import threading
import logging
from pathlib import Path
import time
from FTP import *
from os import listdir
from os.path import isfile, join
bufferSize = 512
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-2s) %(message)s',)

def ls(ruta = 'imgS/.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

threading.current_thread().setName("Cliente")
HOST = 'localhost'
PORT = 21
bufferSize = 1024
passs='admin'
user='user'
FTP=protocoloTFP()
TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
FTP.cConect(TCPClientSocket,HOST,PORT)
time.sleep(1)
FTP.cLogin(TCPClientSocket,user,passs)
time.sleep(1)
FTP.cDIR(TCPClientSocket)
time.sleep(1)
FTP.cSET(TCPClientSocket)
time.sleep(1)
FTP.cCLOSE(TCPClientSocket)
