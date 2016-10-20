#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple."""
import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """SIP server class."""

    clients_dicc = {}

    def handle(self):
        """Cada vez que un cliente envia un mensaje se ejecuta."""
        data = self.rfile.read().decode('utf-8')
        print(data)
        client_data = data.split()
        user = client_data[1][4:]
        exval = int(client_data[4])
        self.clients_dicc[user] = (self.client_address[0], exval)
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

        if int(exval) == 0:
            del self.clients_dicc[user]

        print(self.clients_dicc)

if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
    except IndexError:
        sys.exit("Usage: server.py port_number")
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de SIP...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
