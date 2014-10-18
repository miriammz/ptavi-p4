#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import sys
import socket

# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
register = sys.argv[3]
email = sys.argv[4]

# Contenido que vamos a enviar
#LINE = sys.argv[3] 
LINE = ""

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

if register == "REGISTER":
	LINE = "REGISTER sip:" + email + " " + "SIP/1.0\r\n\r\n"
	print "Enviamos: " + LINE
my_socket.send(LINE)
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminado socket..."

# Cerramos todo
my_socket.close()
print "Fin."

# python client.py ip puerto linea (ej 127.0.0.1 5060 register email@email.com)
