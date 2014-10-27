#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import sys
import socket

# Cliente UDP simple.

# Parametros pasados por el teclado.
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
REGISTER = sys.argv[3]
EMAIL = sys.argv[4]
EXPIRES = sys.argv[5]

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

"""
Comprobamos que pasamos por teclado el numero de argumentos correctos y
enviamos al servidor nuestro email y el expires
"""

if len(sys.argv) != 6:
    print "Usage: client.py ip puerto register sip_addres expires_value"
    sys.exit()

if REGISTER == "REGISTER":
    LINE = "REGISTER sip:" + EMAIL + " " + "SIP/2.0\r\n"
    LINE2 = "Expires: " + EXPIRES + "\r\n\r\n"
    print "Enviamos: " + LINE + LINE2
my_socket.send(LINE + LINE2 + "\r\n")
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminado socket..."

# Cerramos todo
my_socket.close()
print "Fin."
