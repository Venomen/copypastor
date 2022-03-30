#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from datetime import date

__author__ = "Dawid Deregowski deregowski.net"
__copyright__ = "Copyright (c) %s - Dawid Deręgowski deregowski.net" % date.today().year
__version__ = "1.0.0"

import pwd
import getpass
import setuptools
import os
import sys
import shutil
import errno
import pathlib


# you need python3!

print(f"Checking Python version...")

if sys.version_info <= (3, 4):
    print(f"Sorry, copypastor requires at least Python 3.4!")
    sys.exit(1)

# check requirements

print(f"Checking copypastor requirements...")

if os.path.isfile("./copypastor/requirements.txt"):
    with open("./copypastor/requirements.txt") as f:
        required = f.read().splitlines()
else:
    print(f"NO requirements.txt file in install dir! Please check this before installation.")
    print(f"\ncopypastor v{__version__} - bye bye.")
    sys.exit(1)

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

# test if user and installation dirs exists

print(f"Checking copypastor Install Setup & Configurations...")

# checking main app dirs

if not os.path.exists(copypastor_cfg_dir):
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

print(f"Starting copy install config files...")

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

# installation parameters

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="copypastor",
    version=__version__,
    author="Dawid Deręgowski",
    author_email="dawid@deregowski.net",
    description="For clipboard copy/paste remote action ;-)",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/Venomen/copypastor",
    packages=setuptools.find_packages(),
    install_requires=required,
    entry_points={
        "console_scripts": [
            "copypastor = copypastor.copypastor:start"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
