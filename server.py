#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):

    """
    Funcion register: registramos el usuario con el email, la ip y la hora
    """
    dicc = {}

    def register2file(self):
        fich = open("registered.txt", "w")
        fich.write("User\tIP\tExpires\n")
        for cliente, valor in self.dicc.items():
            ip = valor.split(",")[0]
            hora = time.strftime('%Y-­%m-­%d %H:%M:%S',
                            time.gmtime(time.time()))
            fich.write(cliente + '\t' + ip + '\t' + hora + '\n')

    """
    Funcion handle: leemos lo que nos envia el cliente y procesamos el expires
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion" + '\n')
        IP = self.client_address[0]
        PUERTO = str(self.client_address[1])
        # Leyendo línea a línea lo que nos envía el cliente
        line = self.rfile.read()
        print "El cliente nos manda " + line
        line = line.split(" ")
        line2 = line[1].split(":")
        cliente = line2[1]
        line3 = line[3].split("\r")
        EXPIRES = line3[0]
        self.dicc[cliente] = IP
        tiempo = time.time() + int(EXPIRES)
        hora_actual = time.time()
        while 1:
            if EXPIRES == '0':
                if cliente in self.dicc:
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    # borramos al usuario
                    del self.dicc[cliente]
                    self.register2file()
                    break
            else:
                self.dicc[cliente] = IP + ", " + str(tiempo)
                self.register2file()
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                break
            if not line or not line2:
                break
        for elemento, valor in self.dicc.items():
            hora = valor.split(",")[-1]
            if hora_actual > hora:
                del self.dicc[elemento]
                self.register2file()

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PUERTO = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PUERTO), SIPRegisterHandler)
    print "Lanzado servidor UDP de eco..."
    serv.serve_forever()
