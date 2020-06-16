from Pokemon import *
import socket
import threading
import time
import logging
bufferSize = 1024
listaConexiones = []
lock =threading.Lock()
con= threading.Condition()
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-2s) %(message)s',)
def generar():
    pikachu =   Pokemon("pikachu", "electrico", 0, "amarillo", "impactrueno", 0, "raton")

    charmander = Pokemon("charmander", "fuego", 0, "naranja", "lanzallamas", 0, "lagartija")

    charizard = Pokemon("charizard", "fuego", 1, "naranja", "naranja", 1, "lagartija")

    chikorita = Pokemon("chikorita", "planta", 0, "verde", "hojas navaja",0, "hoja")

    articuno = Pokemon("articuno", "hielo", 1, "azul", "presion", 0, "congelar")

    gastly = Pokemon("gastly", "fantasma",1, "morado", "levitacion", 0, "gas")

    gengar = Pokemon("gengar", "fantasma", 0, "morado", "cuerpo", 1, "sombra")

    dragonite = Pokemon("dragonite", "dragon", 1, "naranja", "foco interno", 1, "dragon")

    raichu = Pokemon("raichu", "electrico", 1, "amarillo", "impactrueno", 1, "raton")

    alakazam = Pokemon("alakazam", "psiquico", 0, "cafe", "sincronia", 1, "psiquico")
    r = 1
    if r == 1: return pikachu
    if r == 2: return charmander
    if r == 3: return charizard
    if r == 4: return chikorita
    if r == 5: return articuno
    if r == 6: return gastly
    if r == 7: return gengar
    if r == 8: return dragonite
    if r == 9: return raichu
    if r == 10: return alakazam

class Juego (object,):
    def __init__(self):
        self.Turnos = 1
        self.star=0
        self.max=0
        self.fin=False;
        self.config=False
        self.Pj= generar()

    def cambiarT(self):
        if int(self.Turnos)==int(self.max):
            self.Turnos=1;
        else:
            self.Turnos+=1

    def cambiarF(self):
        self.fin=not(self.fin)

    def Operacion(self,Mensaje):
         RasgosA=["tipo","color","skill","categoria","vuela","evolucion","volar"]
         RasgosC=["nombre","se llama","el pokemon se llama"]
         for cadena in RasgosA:
             if Mensaje.find(cadena)>=0:
                 print("Es una Rasgo")
                 return 1
         for cadena in RasgosC:
             if Mensaje.find(cadena)>=0:
                 print("Esta Adivinando")
                 return 2

    def Separar(self, Mensaje):
        if Mensaje.find("nombre") >= 0 or Mensaje.find("se llama") >= 0 or Mensaje.find("el pokemon es") >= 0: return "nombre", Mensaje
        if Mensaje.find("tipo")>=0: return "tipo",Mensaje
        if Mensaje.find("color")>=0: return "color", Mensaje
        if Mensaje.find("skill")>=0: return "skill", Mensaje
        if Mensaje.find("categoria")>=0: return "categoria", Mensaje
        if Mensaje.find("vuela")>=0 or Mensaje.find("volar")>=0:
            if Mensaje.find("no")>=0:return "vuela", 0
            else: return "vuela", 1
        if Mensaje.find("evolucion")>=0 or Mensaje.find("evolucionar")>=0:
            if Mensaje.find("no")>=0:return "evolucion", 0
            else: return "evolucion", 1



def Esperar (barrier,conn,nombre,game):
    while True:
         if int(barrier.n_waiting) == 0:
             break
         print('Esperando,con {} jugadores más'.format(barrier.n_waiting)+'. Faltan:'+str(int(game.max) -barrier.n_waiting)+' para iniciar...')
         Mensaje = 'Judador '+ str(nombre) + ': Esperando Jugadores, Faltan:'+str(int(game.max) - int(barrier.n_waiting))+' para iniciar...'
         conn.send(str(Mensaje).encode('utf-8'))
         time.sleep(1)
    print()

def Iniciar(id, sc, game):
        r = 'null'
        while r != 'ok':
            sc.send(str('ok').encode('utf-8'))
            r = str(sc.recv(bufferSize).decode('utf-8'))
        print('Jugador ' + id + ":listo")
        mensaje = str(id)
        sc.send(str(mensaje).encode('utf-8'))
        game.star += 1

def ActualizarTurno(id):
    print("Actualizando Turno a Jugadores")
    for conn in listaConexiones:
        if conn.fileno() == -1:
            listaConexiones.remove(conn)
        conn.send(str(id).encode('utf-8'))

def ActualizarJugada(respuesta,id,rasgo,dato):
    for conn in listaConexiones:
        print("Actualizando Jugada a Jugadores")
        if conn.fileno() == -1:
            listaConexiones.remove(conn)
        Mensaje = str( str(id) + "." + str(rasgo) + "." + str(dato) + "." + str(respuesta))
        print(Mensaje)
        conn.send(Mensaje.encode('utf-8'))


def recibir_datos(barrier,sc, addr,game,lock,con,b):
    id = threading.current_thread().name
    barrier.wait()
    Iniciar(id, sc, game)
    b.wait()
    while not game.fin:
        with con:
            while not int(game.Turnos)==int(id):
                     logging.debug("Jugador" + id + " :Esperando su turno...")
                     con.wait()
            if  not game.fin:
                logging.debug("Es turno del jugador : " + id)
                ActualizarTurno(id)
                Respuesta = sc.recv(bufferSize).decode('utf-8')
                if int(game.Operacion(Respuesta))==1:
                        Caracteristica,Dato=game.Separar(Respuesta)
                        print("Se identifica " + str(Caracteristica)+"/"+str(Dato))
                        ActualizarJugada(game.Pj.Comparar(Caracteristica,Dato),id,Caracteristica,Dato)
                        logging.debug('Jugador ' + id + ':Termino su jugada')
                        game.cambiarT()
                        con.notifyAll()
                if (game.Operacion(Respuesta)) == 2:
                        Caracteristica, Dato = game.Separar(Respuesta)

                        if game.Pj.Comparar(Caracteristica, Dato)>=0:
                            ActualizarJugada(str(-10), id, Caracteristica, Dato)
                            logging.debug('Jugador ' + id + ':Termino su jugada')
                            logging.debug('Jugador ' + id + ':ADIVINO')
                            break
                        else:
                            ActualizarJugada(str(-1), id, Caracteristica, Dato)
                            logging.debug('Jugador ' + id + ':Termino su jugada')
                            logging.debug('Jugador ' + id + ':NO adivino')
                            game.cambiarT()
                            con.notifyAll()




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


#HOST = "192.168.0.4"
HOST = 'localhost'
PORT = 8000
r='0'
UDPServerSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPServerSocket.bind((HOST, PORT))
UDPServerSocket.listen(5)
print("El servidor TCP está disponible y en espera de Jugadores")

game = Juego()
print("POKEMON A ADIVINAR: "+ game.Pj.getNombre())
if not game.config:
        print("Esperando primer Jugador...")
        client_conn, client_addr = UDPServerSocket.accept()
        client_conn.send(str("config").encode('utf-8'))
        Respuesta =  client_conn.recv(bufferSize).decode('utf-8')
        game.max = Respuesta
        print(" Jugadores max: " + game.max)
        game.config=not(game.config)
        client_conn.close()
        UDPServerSocket.close()

UDPServerSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPServerSocket.bind((HOST, PORT))
UDPServerSocket.listen(5)
b = threading.Barrier(int(game.max))
barrier = threading.Barrier(int(game.max))
servirPorSiempre(UDPServerSocket, listaConexiones,game,lock,con,barrier,b)
UDPServerSocket.close()
