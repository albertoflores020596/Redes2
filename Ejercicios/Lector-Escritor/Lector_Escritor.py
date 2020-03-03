import logging
import threading
import time


def lector1(lock):
    logging.debug('Lector 1 intenta libro')
    lock.acquire()
    try:
      logging.debug('Lector1 toma libro')
      time.sleep(3)
    finally:
       logging.debug('Lector1 deja el libro')
       lock.release()

def lector2(lock):
    logging.debug('Lector 2 intenta libro')
    lock.acquire()
    try:
      logging.debug('Lector 2 toma libro')
      time.sleep(3)
    finally:
       logging.debug('Lector 2  deja el libro')
       lock.release()


def escritor1(lock):
    logging.debug('escritor 1 intenta libro')
    lock.acquire()
    try:
      logging.debug('escritor 1 toma libro')
      time.sleep(3)
    finally:
       logging.debug('escritor 1  deja el libro')
       lock.release()

def escritor2(lock):
    logging.debug('escritor 2 intenta libro')
    lock.acquire()
    try:
      logging.debug('escritor 2 toma libro')
      time.sleep(3)
    finally:
       logging.debug('escritor 2  deja el libro')
       lock.release()


logging.basicConfig(
    level=logging.DEBUG,
    format='( %(message)s',
)

lock = threading.Lock()

h1 = threading.Thread(target=lector1,args=(lock,), name='LockHolder', daemon=True,)
h1.start()

h2 = threading.Thread(target=lector2,args=(lock,), name='Worker',)
h2.start()

h3 = threading.Thread(target=escritor1,args=(lock,), name='Worker',)
h3.start()

h4 = threading.Thread(target=escritor2,args=(lock,), name='Worker',)
h4.start()
