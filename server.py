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
    Echo server class
    """
    dicc = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion" + '\n')
        fichero = open("fichero.txt", "w")
        IP = self.client_address[0]
        PUERTO = str(self.client_address[1])
        fichero.write(IP + " " + str(PUERTO))
        # register2file
        def register2file():
            fich = open("registered.txt", "w")
            fich.write("User\tIP\tExpires\n")
            expire = time.strftime('%Y-­%m-­%d %H:%M:%S',
                             time.gmtime(time.time()))
            fich.write(cliente + '\t' + IP + '\t' +  expire)
        # Leyendo línea a línea lo que nos envía el cliente
        line = self.rfile.read()
        print "El cliente nos manda " + line
        line = line.split(" ")
        line2 = line[1].split(":")
        cliente = line2[1]
        line3 = line[3].split("\r")
        EXPIRES = line3[0]
        self.dicc[cliente] = IP
        hora_actual = time.time() 
        tiempo = time.time() + int(EXPIRES)
        while 1:
            if EXPIRES == '0':
                if cliente in self.dicc:
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    # borramos al usuario
                    del self.dicc[cliente]
                    register2file()
                    break
                #else:
                    #self.wfile.write("SIP/2.0 410 Gone\r\n\r\n")
                    #print "11111111111"
                    #break
            else:
                self.dicc[cliente] = [IP, tiempo]
                print "hhhhhhhhh"
                if hora_actual < tiempo:
                    print hora_actual
                    print "aaaaaaaaaaaaaa"
                    print tiempo
                    del self.dicc[cliente]
                    register2file()
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    print "3333333333333333"
                    print self.dicc
                break
            if not line or not line2:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PUERTO = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PUERTO), SIPRegisterHandler)
    print "Lanzado servidor UDP de eco..."
    serv.serve_forever()
