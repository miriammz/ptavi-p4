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
        self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
        print self.client_address
        fichero = open("fichero.txt", "w")
        ip = self.client_address[0]
        puerto = self.client_address[1]
        fichero.write(ip + " " + str(puerto))
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente nos manda " + line
            line2 = line.split(":")
            self.dicc["cliente"] = line[1]
            self.dicc["ip"] = ip
            cliente = self.dicc["cliente"]
            ip = self.dicc["ip"]
            if not line or not line2:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    puerto = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", puerto), SIPRegisterHandler)
    print "Lanzado servidor UDP de eco..."
    serv.serve_forever()
