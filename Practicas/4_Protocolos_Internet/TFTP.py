
import logging
bufferSize = 512
class protocoloTFTP (object,):


    def Identificar(self,Paquete):
        op = int(Paquete[0])
        if int(op) == 1:
            logging.debug('Se recibio codigo de operacion 01: Solicitud de Lectura')
            return 1
        elif int(op) == 2:
            logging.debug('Se recibio codigo de operacion 02: Solicitud de Escritura')
            return 2
        elif int(op) == 3:
            logging.debug('Se recibio codigo de operacion 03: Rececibio Archivo')
            return 3
        elif int(op) == 4:
            logging.debug('Se recibio codigo de operacion 04: Rececibio AKC')
            return 4
        elif int(op) == 0:
            error = Paquete[1]
            #m=Paquete[2:len(Paquete)]
            logging.debug('Se recibio codigo de operacion 05: Error,Codigo de error: ' + str(error) )
            return 0
        elif int(op) == 5:
            logging.debug('Se recibio codigo de operacion 05: Error,Codigo de error 0: Sin definir')
            return 5



        else:

            logging.debug('Se recibio codigo de operacion desconocido')
            return 0

    def Cambiar(self):
        self.con=not(self.con)

    def C1(self,fil):
        #print("Cliente: Se crea Paquete de lectura  codigo: 1 ")
        m= str('1'+ str(fil))
        return m

    def C2(self,fil):
      #  print("Se crea Paquete de Escritura codigo : 2 ")
        m=str('2'+ str(fil))
        return  m

    def C3(self,fil):
       # print("Se crea Paquete Datos Codigo : 4 ")
        m=str('3'+ str(fil))
        return  m

    def C4(self,):
        #print("Se crea Paquete AKC codigo : 5 ")
        m=str('4'+ str('AKC'))
        return  m

    def C5(self,img,c,m):
        #print("Se crea Paquete Error codigo : 5 ,tipo de error "+str(c)+" Descripcion:"+str(m))
        m=str('5'+str(c)+ str(m))
        return  m