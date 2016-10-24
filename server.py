#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor SIP en UDP simple."""
import socketserver
import sys
import json
from time import time, gmtime, strftime


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Clase para un servidor SIP."""

    data_dicc = {}

    def json2registered(self):
        """Busca fichero JSON con clientes; si no hay devuelve dicc vacio."""
        try:
            with open('registered.json') as f_json:
                self.data_dicc = json.load(f_json)
        except FileNotFoundError:
            self.data_dicc = {}

    def register2json(self):
        """Introduce en un fichero JSON los usuarios."""
        with open('registered.json', 'w') as f_json:
            json.dump(self.data_dicc, f_json, sort_keys=True, indent=4)

    def handle(self):
        """Cada vez que un cliente envia una peticion se ejecuta."""
        data = self.rfile.read().decode('utf-8')
        print(data)
        c_data = data.split()
        user, exval, c_ip = c_data[1][4:], c_data[4], self.client_address[0]
        now = int(time())
        str_now = strftime('%Y-%m-%d %H:%M:%S', gmtime(now))
        time_exval = int(exval) + now
        str_exval = strftime('%Y-%m-%d %H:%M:%S', gmtime(time_exval))
        self.data_dicc[user] = {'address': c_ip, 'expires': str_exval}
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        lista_expirados = []
        for user in self.data_dicc:
            if self.data_dicc[user]['expires'] <= str_now:
                lista_expirados.append(user)
        for name in lista_expirados:
            del self.data_dicc[name]
        self.register2json()

if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
    except (IndexError, ValueError):
        sys.exit("Usage: server.py port_number")
    SERV = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    try:
        SERV.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
