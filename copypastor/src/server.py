#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
from datetime import date

__author__ = "Dawid Deregowski deregowski.net"
__copyright__ = "Copyright (c) %s - Dawid Deręgowski deregowski.net" % date.today().year
__version__ = "1.0.0"

"""
For clipboard copy/paste remote action ;-)
"""

import socket
import getpass
import pwd
import pyperclip

# Local user config file/dir

copypastor_conf = "config.py"
current_user = getpass.getuser()
copypastor_cfg_dir = pwd.getpwnam(current_user).pw_dir + "/.config/copypastor/"

# Importing config outside app, from user home dir

sys.path.insert(1, copypastor_cfg_dir)
from config import *


def start_server():
    server_address = (SERVER_HOST, SERVER_PORT)
    auth_key = bytes(AUTH_KEY, encoding='utf8')
    print("\n Server Mode Activated - Host: %s Port: %s" % (SERVER_HOST, SERVER_PORT))

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    print("Starting up Server on {} port {}".format(*server_address))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # Wait for a connection
    print("- Waiting for a connection...")
    connection, client_address = sock.accept()
    try:
        data = connection.recv(16)
        print("-- Connection from", client_address)
        try:
            data2 = bytes(get_clipboard(), encoding='utf8')
            if data == auth_key and data2:
                print("-- Access Granted.")
                print("-- Sending data back to the client...")
                connection.sendall(data2)
            else:
                print("-- ERROR: No clip data or bad auth key!", client_address)
        except TypeError:
            print("-- ERROR: Ups, clipboard is broken. Maybe 'export DISPLAY'?")
    finally:
        # Clean up the connection
        connection.shutdown(1)
        connection.close()
        print("-- Bye Bye.")


def start_silent_server():
    server_address = (SERVER_HOST, SERVER_PORT)
    auth_key = bytes(AUTH_KEY, encoding='utf8')
    print("\n Server Mode Activated - Host: %s Port: %s" % (SERVER_HOST, SERVER_PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
    sock.listen(1)
    connection, client_address = sock.accept()
    try:
        data = connection.recv(16)
        try:
            data2 = bytes(get_clipboard(), encoding='utf8')
            if data == auth_key and data2:
                connection.sendall(data2)
            else:
                print("-- ERROR: No clip data or bad auth key!", client_address)
        except TypeError:
            print("-- ERROR: Ups, clipboard is broken. Maybe 'export DISPLAY'?")
    finally:
        connection.shutdown(1)
        connection.close()


def get_clipboard():
    try:
        clipboard = pyperclip.paste()
        return clipboard
    except pyperclip.PyperclipException:
        print("-- ERROR: Clipboard is empty.")
