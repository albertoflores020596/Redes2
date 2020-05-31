from xmlrpc.server import SimpleXMLRPCServer,list_public_methods
from xmlrpc.server import SimpleXMLRPCRequestHandler
import logging
import os
from os import remove
import shutil
import inspect

class directorio(object):
    def __init__(self,):
        self.home='home/'
        self.gtw=self.home
        #home='home/Novela Ligera'
    def getstw(self):
        return self.gtw


logging.basicConfig(level=logging.DEBUG)
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
# Create server
with SimpleXMLRPCServer(('localhost', 8000),requestHandler=RequestHandler) as server:
    server.register_introspection_functions()



    class MyFuncs:

        def __init__(self, ):
            self.home = 'home/'
            self.gtw = self.home
            # home='home/Novela Ligera'

        def getstw(self):
            return self.gtw

        def _listMethods(self):
            return list_public_methods(self)

        def create(self,name):
            file = open(name, "w")
            file.close()
            return self.gtw

        def read(self, name):
            file = open(name, "r")
            Archivo=file.read()
            file.close()
            return Archivo,self.gtw

        def write(self, name,Cadena):
            file = open(name, "a")
            file.write(Cadena)
            file.close()
            return self.gtw

        def rename(self, name, Nname):
            os.rename(name,Nname)
            return self.gtw

        def remove(self, name):
            remove(name)
            return self.gtw

        def mkdir(self, dir):
            os.makedirs(dir)
            return self.getstw()

        def rmdir(self,dir,name):
            shutil.rmtree(dir)
            self.gtw=self.gtw.replace(name,"")
            return self.getstw()

        def ls(self, name):
               return os.listdir(name)
        def dir(self,):
               return self.gtw
        def cd(self,dir):
            self.gtw=dir
            return self.getstw()

    server.register_instance(MyFuncs())
    try:
        print ('Use Control-C to exit')
        server.serve_forever()
    except KeyboardInterrupt:
        print ('Exiting')
