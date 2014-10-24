#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion" + '\n')
        #self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
        print self.client_address
        fichero = open("fichero.txt", "w")
        IP = self.client_address[0]
        PUERTO = str(self.client_address[1])
        fichero.write(IP + " " + str(PUERTO))
        # Leyendo línea a línea lo que nos envía el cliente
        line = self.rfile.read()
        print "El cliente nos manda " + line
        line = line.split(" ")
        line2 = line[1].split(":")
        cliente = line2[1]
        EXPIRES = line[3]
        self.dicc[cliente] = IP
        print self.dicc
        while 1:
            if EXPIRES == '0\r\n\r\n\r\n':
                if cliente in self.dicc:
                    #print "22222222222222"
                    self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
                    # borramos al usuario
                    del self.dicc[cliente]
                    #break
                else:
                    self.wfile.write("SIP/1.0 410 Gone\r\n\r\n")
                    #print "11111111111"
            else:
                self.dicc[cliente] = [IP, EXPIRES]
                self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
                #print "3333333333333333"
                #break
            if not line or not line2:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PUERTO = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PUERTO), SIPRegisterHandler)
    print "Lanzado servidor UDP de eco..."
    serv.serve_forever()
