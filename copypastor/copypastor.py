#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from datetime import date
import sys
import shutil
import os
import errno


__author__ = "Dawid Deregowski deregowski.net"
__copyright__ = "Copyright (c) %s - Dawid Deręgowski deregowski.net" % date.today().year
__version__ = "1.0.2"

"""
For clipboard copy/paste remote action ;-)
"""

from sys import argv
import argparse
from argparse import RawTextHelpFormatter

try:
    from pynput import keyboard
except ImportError or TypeError:
    print("-- ERROR: Ups, clipboard is broken. Maybe 'export DISPLAY'? \n "
          "* Please make sure that you have an X server running, and that the "
          "DISPLAY environment variable is set correctly.")
    sys.exit(1)

import emoji
import pwd
import getpass

# check cfg

copypastor_install_conf = "default_config.py"
copypastor_install_dir = os.getcwd() + "/copypastor/" + "config/"
copypastor_install_config = copypastor_install_dir + copypastor_install_conf
copypastor_install_init = copypastor_install_dir + "__init__.py"

current_user = getpass.getuser()
copypastor_conf = "config.py"
copypastor_cfg_dir = pwd.getpwnam(current_user).pw_dir + "/.config/copypastor/"
copypastor_cfg = copypastor_cfg_dir + copypastor_conf
copypastor_cfg_init = copypastor_cfg_dir + "__init__.py"

# checking main app dirs

if not os.path.exists(copypastor_cfg_dir):
    print(f"Ups.. no config files! I'll restore from default in {copypastor_cfg_dir} \n")
    try:
        os.makedirs(copypastor_cfg_dir, exist_ok=True)

    except Exception as details:
        print(f"Couldnt make dirs! {details}")
        print(f"Please check this before installing again.")
        print(f"\ncopypastor v{__version__} - bye bye.")
        sys.exit(1)

# copy config files

try:
    files = os.listdir(copypastor_install_dir)
    files.sort()

except FileNotFoundError:
    print(f"Copy config: source configs not found! Please check installation dir!")
    print(f"\ncopypastor v{__version__} - bye bye.")
    sys.exit(1)

if not os.path.exists(copypastor_cfg):
    try:
        shutil.copytree(copypastor_install_dir, copypastor_cfg_dir)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            try:
                shutil.copy(copypastor_install_config, copypastor_cfg)
                shutil.copy(copypastor_install_init, copypastor_cfg_init)
            except shutil.SameFileError:
                print(f"Ok, {copypastor_cfg} exists, moving on.")
            except Exception as details:
                print(f"Copy config: copy dir/file error! {details}")
                print(f"' '")
        if exc.errno == errno.EEXIST:
            try:
                shutil.copy(copypastor_install_config, copypastor_cfg)
                shutil.copy(copypastor_install_init, copypastor_cfg_init)
            except shutil.SameFileError:
                print(f"Ok, {copypastor_cfg} exists, moving on.")
            except Exception as details:
                print(f"Copy config: copy dir/file error! {details}")
                print(f"' '")
        else:
            print(f"Couldn't copy configs! {exc}")
            print(f"Please check this before installing again.")
            print(f"\ncopypastor v{__version__} - bye bye.")
            sys.exit(1)

from .src.server import start_server
from .src.server import start_silent_server
from .src.client import start_client
from .src.client import start_silent_client

# Local user config file/dir

copypastor_conf = "config.py"
current_user = getpass.getuser()
copypastor_cfg_dir = pwd.getpwnam(current_user).pw_dir + "/.config/copypastor/"
copypastor_cfg = copypastor_cfg_dir + copypastor_conf

# IMPORTANT!
# Loading config outside app, from user home dir

sys.path.insert(1, copypastor_cfg_dir)
from config import *

# The currently active modifiers

current_client = set()
current_server = set()

# Main action


def on_press(key):
    if any([key in COMBO for COMBO in ACTIVATE_CLIENT]):
        current_client.add(key)
        if any(all(k in current_client for k in COMBO) for COMBO in ACTIVATE_CLIENT):
            start_client()
    if any([key in COMBO for COMBO in ACTIVATE_SERVER]):
        current_server.add(key)
        if any(all(k in current_server for k in COMBO) for COMBO in ACTIVATE_SERVER):
            start_server()


def on_press_silent(key):
    if any([key in COMBO for COMBO in ACTIVATE_CLIENT]):
        current_client.add(key)
        if any(all(k in current_client for k in COMBO) for COMBO in ACTIVATE_CLIENT):
            start_silent_client()
    if any([key in COMBO for COMBO in ACTIVATE_SERVER]):
        current_server.add(key)
        if any(all(k in current_server for k in COMBO) for COMBO in ACTIVATE_SERVER):
            start_silent_server()


def on_release(key):
    if any([key in COMBO for COMBO in ACTIVATE_CLIENT]):
        current_client.remove(key)
    if any([key in COMBO for COMBO in ACTIVATE_SERVER]):
        current_server.remove(key)


def start_key_listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def start_silent_key_listen():
    with keyboard.Listener(on_press=on_press_silent, on_release=on_release) as listener:
        listener.join()


# Start menu

def start():
    try:
        if argv[1]:
            if argv[1] == "--help":  # little help menu
                parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                                 description="copypastor is created for clipboard copy/paste "
                                                             "remote action. "
                                                             "You can define your shortcuts & connection info in "
                                                             "default_config.py. "
                                                             "\n\nDefaults: "
                                                             "\n- silent mode, waiting for your shortcut "
                                                             "(client or server)"
                                                             "\n- main config in '%s'"
                                                             "\n- read README.md!" % copypastor_cfg)
                parser.add_argument("--version", nargs="?", help="current version & authors")
                parser.add_argument("--debug", nargs="?", help="get more details")
                parser.add_argument("--server", nargs="?", help="run server mode only")
                parser.add_argument("--client", nargs="?", help="run client mode only")
                parser.parse_args()
                sys.exit(0)

            if argv[1] == "--version" or argv[1] == "-v" or argv[1] == "--v":
                print(f'{__version__} {__copyright__}')
                sys.exit(0)

            if argv[1] == "--client":
                try:
                    print(emoji.emojize(":spaghetti: Starting copypastor [Client Mode Only] \n"
                                        "Press CTRL+C to Exit. Use without '--client' for default mode, "
                                        "'--help' for help."))
                    start_silent_client()
                    sys.exit(0)

                except KeyboardInterrupt:
                    print(" EXIT: Ctrl+C pressed, bye bye.")
                    sys.exit(1)

            if argv[1] == "--server":
                try:
                    print(emoji.emojize(":spaghetti: Starting copypastor [Server Mode Only] \n"
                                        "Press CTRL+C to Exit. Use without '--server' for default mode, "
                                        "'--help' for help."))
                    while True:
                        start_silent_server()

                except KeyboardInterrupt:
                    print(" EXIT: Ctrl+C pressed, bye bye.")
                    sys.exit(1)

            if argv[1] == "--debug":
                try:
                    print(emoji.emojize(":spaghetti: Starting copypastor [Debug] \n"
                                        "Press key 'C' to run a client-mode, key 'S' to run a server-mode, "
                                        "or 'CTRL+C' to Exit. \n"
                                        "Use without '--debug' for silent mode, '--help' for help."))
                    while True:
                        start_key_listen()

                except KeyboardInterrupt:
                    print(" EXIT: Ctrl+C pressed, bye bye.")
                    sys.exit(1)

            print(emoji.emojize(":spaghetti: ERROR: Bad params! \n"
                                "Please provide (or leave empty): --server --client --help --debug --version "))
            sys.exit(1)
    except IndexError:
        pass

    if "" in argv[0]:
        try:
            print(emoji.emojize(":spaghetti: Starting copypastor \n"
                                "Press key 'C' to run client-mode, key 'S' to run a server-mode, "
                                "or 'CTRL+C' to Exit. \n "
                                "Use '--debug' for detailed mode, '--help' for help.  "))
            while True:
                start_silent_key_listen()

        except KeyboardInterrupt:
            print(" EXIT: Ctrl+C pressed, bye bye.")
            sys.exit(1)
