#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            print("El cliente nos manda ", line.decode('utf-8'),
                 self.client_address)

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
