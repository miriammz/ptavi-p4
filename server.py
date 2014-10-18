#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        print self.client_address
        fichero = open("fichero.txt", "w")
        IP = self.client_address[0]
        PUERTO = self.client_address[1]
        fichero.write(IP + " " + str(PUERTO))
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente nos manda " + line
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    puerto = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", puerto), EchoHandler)
    print "Lanzado servidor UDP de eco..."
    serv.serve_forever()
