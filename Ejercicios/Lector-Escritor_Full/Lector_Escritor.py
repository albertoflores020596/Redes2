import logging
import threading
import time
n_Threading=2
class Libro(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.mensaje="Hola Lectores!!,firma: "
    def Escribir(self,msj):
        logging.debug('Esperando por el candado')
        self.lock.acquire()
        try:
            logging.debug('escribiendo libro')
            self.mensaje = self.mensaje+msj
        finally:
            self.lock.release()
    def Leer (self):
        print( self.mensaje)

def lector(lock,cond,libro):
    if barrier.n_waiting!=0:
        barrier.wait()
    t = threading.currentThread()
    with cond:
        cond.wait()
        logging.debug('El libro esta libre')
        libro.Leer()


def escritor(lock,barrier,cond,libro):
    print(threading.current_thread().name,'Esperando con por mas ESCRITORES')
    id_Escritor=barrier.wait()
    logging.debug('Intenta libro')
    lock.acquire()
    with cond:
          logging.debug('Toma libro')
          Mensaje = str(threading.current_thread().name)
          libro.Escribir(Mensaje)
          time.sleep(3)
          logging.debug('Terminadondo de escribir libro')
          logging.debug('Deja el libro')
          lock.release()
          cond.notifyAll()

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',

)

lock = threading.Lock()
NUM_THREADS = 2
libro=Libro()
condition = threading.Condition()
barrier = threading.Barrier(NUM_THREADS)
h1 = threading.Thread(target=escritor,args=(lock,barrier,condition,libro), name='Escritor 1',)
h1.start()

h3 = threading.Thread(target=lector,args=(lock,condition,libro), name='Lector 1', )
h3.start()

h4 = threading.Thread(target=lector,args=(lock,condition,libro), name='lector 2',)
h4.start()

h2 = threading.Thread(target=escritor,args=(lock,barrier,condition,libro), name='Escritor 2',)
h2.start()

h5 = threading.Thread(target=lector,args=(lock,condition,libro), name='Lector 3', )
h5.start()

h6 = threading.Thread(target=lector,args=(lock,condition,libro), name='lector 4',)
h6.start()

