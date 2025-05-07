#!/usr/bin/python3
import sys
import logging
import os

# Inserisci il path del tuo progetto
sys.path.insert(0, '/var/www/Zork_Wiki_Site')
os.environ['PYTHON_EGG_CACHE'] = '/var/www/Zork_Wiki_Site/.python-eggs'

from myapp import app as application
