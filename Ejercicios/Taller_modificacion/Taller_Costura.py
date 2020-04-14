import logging
import threading
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',)


class Taller (object):
    def __init__(self):
        self.mMIN = threading.Condition()
        self.mMAX = threading.Condition()
        self.mangas=0
        self.cuerpos=0
        self.chalecos = 0

    def incrementarManga(self):
            with self.mMAX:
                if self.mangas >= 10:
                    logging.debug("Alcanzo la el limite de manga")
                    self.mMAX.wait()
                else:
                    self.mangas += 1
                    logging.debug("Creo una manga, Total mangas=%s", self.mangas)
            with self.mMIN:
                if self.mangas >= 2:
                    logging.debug("Tiene suficientes mangas")
                    self.mMIN.notify()

    def incrementarChaleco(self):
        with self.mMAX:
            if self.chalecos >= 100:
                logging.debug("Alcanzo la el limite de chalecos")
                self.mMAX.wait()
            else:
                self.chalecos += 1
                logging.debug("Creo una chaleco, Total chalecos=%s", self.chalecos)
        with self.mMIN:
            if self.mangas >= 2 & self.cuerpos >=1:
                logging.debug("Tiene suficientes mangas y cuerpos")
                self.mMIN.notify()


    def decrementarManga(self):
        with self.mMIN:
            while not self.mangas >= 2:
                logging.debug("Espera a tener suficientes mangas")
                self.mMIN.wait()
            self.mangas -= 2
            logging.debug("Toma 2 mangas, total  mangas=%s", self.mangas)
        with self.mMAX:
            logging.debug("Hay espacio para mas Mangas")
            self.mMAX.notify()

    def incrementarCuerpo(self):
        with self.mMAX:
            if self.cuerpos >= 5:
                logging.debug("Alcanzo el limite de cuerpos")
                self.mMAX.wait()
            else:
                self.cuerpos += 1
                logging.debug("Creo un cuerpo , Total cuerpos=%s", self.cuerpos)
        with self.mMIN:
            if self.cuerpos >= 1:
                logging.debug("Tiene suficientes cuerpos")
                self.mMIN.notify()

    def decrementarCuerpo(self):
        with self.mMIN:
            while not self.cuerpos >= 1:
                logging.debug("Espera que tener suficientes cuerpos")
                self.mMIN.wait()
            self.mangas -= 1
            logging.debug("Toma 1 cuerpo, total  cuerpos=%s", self.cuerpos)
        with self.mMAX:
            logging.debug("Hay espacio para mas cuerpos")
            self.mMAX.notify()

    def getMangas(self):
        return (self.mangas)

    def getCuerpo(self):
        return (self.cuerpos)
    def getChaleco(self):
        return (self.chalecos)



def crearMangas(Taller):
     while (Taller.getMangas() <= 10):
            Taller.incrementarManga()
            time.sleep(1)

def crearCuerpo(Taller):
     while (Taller.getCuerpo() <=5 ):
            Taller.incrementarCuerpo()
            time.sleep(10)

def crearChaleco(Taller):
    while (Taller.getChaleco() <=100 ):
        Taller.decrementarManga()
        Taller.decrementarCuerpo()
        Taller.incrementarChaleco()
        time.sleep(5)



t=Taller()

h2 = threading.Thread(name='Persona 1(Mangas)',target=crearMangas,args=(t,))
h2.start()

h3 = threading.Thread(target=crearCuerpo,args=(t,), name='Persona 2(Cuerpo)', )
h3.start()

h1 = threading.Thread(target=crearChaleco,args=(t,), name='Persona 3(Chaleco)',)
h1.start()





