import logging
import threading
import time
n_Threading=2
logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',)
class Materiales(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.Mangas=0;
        self.Cuerpo=0;
        self.Capacidad = 10;
    def crearManga(self):
        self.Mangas+=1
        time.sleep(.1)

    def crearCuerpo(self):
            self.Cuerpo += 1
            time.sleep(.2)

    def crearChaleco(self):
        self.Mangas-=2
        self.Cuerpo-=1
        time.sleep(.5)

    def Imprimir(self):
     print('Mangas: ',self.Mangas,'Cuerpo: ',self.Cuerpo)

def tMangas(lock,cond,m):
    logging.debug('Empezo a crear Mangas')

    with cond:
          while m.Mangas < m.Capacidad:
                m.crearManga()
                m.crearManga()
                logging.debug('Creo 2 Mangas')
                m.Imprimir()
          logging.debug('Se lleno la Canasta de Mangas')
          cond.wait()


def tCuerpo(lock,cond,m):
    logging.debug('Empezo a crear Cuerpo')

    with cond:
        while m.Cuerpo < m.Capacidad:
                m.crearCuerpo()
                logging.debug('Creo 1 Cuerpo')
                m.Imprimir()
        logging.debug('Se lleno la Canasta de Cuerpos')
        cond.wait()



def tChaleco(lock,cond,m):
    logging.debug('Empezanco a ensamblar')
    with cond:
            while m.Mangas > 1 and m.Cuerpo > 0:
                m.crearChaleco()
                logging.debug('Creo 1 Chaleco')
                m.Imprimir()

            logging.debug('Se acbabo los materiales')
            cond.notifyAll()

lock = threading.Lock()
NUM_THREADS = 2
materiales=Materiales()
condition = threading.Condition()
barrier = threading.Barrier(NUM_THREADS)

h2 = threading.Thread(target=tMangas,args=(lock,condition,materiales), name='Persona 1',)
h2.start()


h3 = threading.Thread(target=tCuerpo,args=(lock,condition,materiales), name='Persona 2', )
h3.start()

h1 = threading.Thread(target=tChaleco,args=(lock,condition,materiales), name='Persona 3',)
h1.start()





