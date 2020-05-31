import xmlrpc.client
import time
import os
#192.168.0.4
#s = xmlrpc.client.ServerProxy('http://192.168.0.4:8000')
s = xmlrpc.client.ServerProxy('http://localhost:8000')
class directorio(object):
    def __init__(self,):
        self.home='home/'
        self.gtw=self.home
        #home='home/Novela Ligera'
    def getstw(self):
        return self.gtw
    def cd(self,name):
        #self.gtw = os.path.join(self.gtw,name)
        self.gtw = name

d=directorio()
while True:
    print("Comandos: ")
    print(s.system.listMethods())
    C = input(str(d.getstw())+ ": ")
    print("\n")
    Comando = C.split(" ", 3)
  #  print(str(Comando))
    if str(Comando[0]) in str(s.system.listMethods()):

        if str(Comando[0])=="create":
            d.cd(s.create(str(os.path.join(d.getstw(),Comando[1]))))
        if str(Comando[0])=="read":
            file,gtw =s.read(str(os.path.join(d.getstw(),Comando[1])))
            d.cd(gtw)
            print(file)
        if str(Comando[0])=="write":
            d.cd(s.write(str(os.path.join(d.getstw(), Comando[1])),Comando[2]))
        if str(Comando[0])=="rename":
            d.cd(s.rename(str(os.path.join(d.getstw(), Comando[1])),os.path.join(d.getstw(), Comando[2])))
        if str(Comando[0])=="remove":
            d.cd(s.remove(str(os.path.join(d.getstw(), Comando[1]))))
        if str(Comando[0])=="mkdir":
            d.cd(s.mkdir(str(os.path.join(d.getstw(), Comando[1]))))
        if str(Comando[0])=="rmdir":
            d.cd(s.rmdir(str(os.path.join(d.getstw(), Comando[1])),Comando[1]))
        if str(Comando[0])=="ls":
            print(s.ls(str(d.getstw())))
        if str(Comando[0])=="cd":
            d.cd(s.cd(os.path.join(d.getstw(), Comando[1])))

    else:
        print("Comando no reconocido")

    print("\n")