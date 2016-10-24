#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente UDP que abre un socket a un servidor."""
import socket
import sys


try:
    SERVER, PORT, MET, USER, EXVAL = sys.argv[1:]
except ValueError:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")
REQ = ("REGISTER sip:" + USER + " SIP/2.0\r\nExpires: " + EXVAL + "\r\n\r\n")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    if MET == "register":
	    my_socket.connect((SERVER, int(PORT)))
	    my_socket.send(bytes(REQ, 'utf-8'))
	    try:
	        data = my_socket.recv(1024).decode('utf-8')
	    except ConnectionRefusedError:
	        sys.exit("No se puede conectar al servidor")
	    print(data)
