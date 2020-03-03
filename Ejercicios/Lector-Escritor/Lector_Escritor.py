import logging
import threading
import time


def lector(lock):
    logging.debug('Intenta libro')
    lock.acquire()
    try:
      logging.debug('toma libro')
      time.sleep(3)
    finally:
       logging.debug('Deja el libro')
       lock.release()


def escritor(lock):
    logging.debug('Intenta libro')
    lock.acquire()
    try:
      logging.debug('Toma libro')
      time.sleep(3)
    finally:
       logging.debug('Deja el libro')
       lock.release()

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',

)

lock = threading.Lock()

h1 = threading.Thread(target=lector,args=(lock,), name='Lector 1', daemon=True,)
h1.start()

h2 = threading.Thread(target=lector,args=(lock,), name='lector 2',)
h2.start()

h3 = threading.Thread(target=escritor,args=(lock,), name='Escritor 1',)
h3.start()

h4 = threading.Thread(target=escritor,args=(lock,), name='Escritor 2',)
h4.start()
