#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys
from datetime import date

__author__ = "Dawid Deregowski deregowski.net"
__copyright__ = "Copyright (c) %s - Dawid Deręgowski deregowski.net" % date.today().year
__version__ = "1.0.0"

try:
    from pynput import keyboard
except ImportError or TypeError:
    print("-- ERROR: Ups, clipboard is broken. Maybe 'export DISPLAY'? \n "
          "* Please make sure that you have an X server running, and that the "
          "DISPLAY environment variable is set correctly.")
    sys.exit(1)

import getpass
import pwd

# Connection info

SERVER_PORT = 3113
SERVER_HOST = "0.0.0.0"
REMOTE_PORT = 3113
REMOTE_HOST = "dd-840-G5"
AUTH_KEY = "xkjHt7m2BJhTEN4T"

# Shortcuts

ACTIVATE_CLIENT = [
    {keyboard.KeyCode(char='c')},
    {keyboard.KeyCode(char='C')}
]

ACTIVATE_SERVER = [
    {keyboard.KeyCode(char='s')},
    {keyboard.KeyCode(char='S')}
]

# Config file/dir

copypastor_install_conf = "default_config.py"
copypastor_install_dir = os.getcwd() + "/copypastor/" + "config/"
copypastor_install_config = copypastor_install_dir + copypastor_install_conf
copypastor_install_init = copypastor_install_dir + "__init__.py"

current_user = getpass.getuser()
copypastor_conf = "config.py"
copypastor_cfg_dir = pwd.getpwnam(current_user).pw_dir + "/.config/copypastor/"
copypastor_cfg = copypastor_cfg_dir + copypastor_conf
copypastor_cfg_init = copypastor_cfg_dir + "__init__.py"
