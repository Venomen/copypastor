#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
import os
from datetime import date

__author__ = "Dawid Deregowski deregowski.net"
__copyright__ = "Copyright (c) %s - Dawid Deręgowski deregowski.net" % date.today().year
__version__ = "1.0.4"

"""
For clipboard copy/paste remote action ;-)
"""

import pwd
import getpass
import socket
import codecs
import pyperclip
import clipboard


# Local user config file/dir
copypastor_conf = "config.py"
current_user = getpass.getuser()
copypastor_cfg_dir = pwd.getpwnam(current_user).pw_dir + "/.config/copypastor/"
copypastor_cfg = copypastor_cfg_dir + copypastor_conf

# Importing config outside app, from user home dir
sys.path.insert(1, copypastor_cfg_dir)
from config import *


def start_client():
    server_address = (REMOTE_HOST, REMOTE_PORT)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    print("\n Connecting to {} port {}...".format(*server_address))
    try:
        sock.connect(server_address)

        # Send data
        message = bytes(AUTH_KEY, encoding='utf8')
        print("-- Sending auth:", codecs.decode(message))
        sock.sendall(message)
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        print("-- Received clipboard:", codecs.decode(data))
        if data:
            try:
                pyperclip.copy(codecs.decode(data))
            except pyperclip.PyperclipException:
                print("-- ERROR: Couldn't copy clipboard data.")
        else:
            print("-- ERROR: Ups, bad auth or no clip data!")
    except ConnectionRefusedError:
        print("ERROR: connection failed!")
    except socket.gaierror:
        print("ERROR: bad hostname or can't connect.")
    finally:
        print("...closing socket.")
        sock.close()


def start_silent_client():
    server_address = (REMOTE_HOST, REMOTE_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("\n Client Mode Activated")
    try:
        sock.connect(server_address)
        message = bytes(AUTH_KEY, encoding='utf8')
        sock.sendall(message)
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        if data:
            try:

                tmp_file = copypastor_cfg_dir + 'tmp.png'
                with open(tmp_file, 'wb') as file:
                    file.write(data)
                with open(tmp_file, 'rb') as file:
                    binary_content = file.read()
                clipboard.copy(binary_content)
                os.remove(tmp_file)

            except pyperclip.PyperclipException:
                print("-- ERROR: Couldn't copy clipboard data.")
        else:
            print("-- ERROR: Ups, bad auth or no clip data!")
    except ConnectionRefusedError:
        print("ERROR: connection failed!")
    except socket.gaierror:
        print("ERROR: bad hostname or can't connect.")
    finally:
        sock.close()
