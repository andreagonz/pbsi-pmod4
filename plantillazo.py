
#!/usr/bin/python
# -*- coding: utf-8 -*-
#UNAM-CERT

###TOR

"""
***EJEMPLO***
python req.py -p 9889 -s  87.118.110.170 -U romina.martinez -P P4ssw0rd123 -T
"""

"""
Se debe instalar TOR
Debian: apt-get install TOR
Iniciarlo: service tor start o simplemente colocar el comado tor (Depende de como es que se haya instalado)
De igual forma se debe instalar socks
Debian: apt-get install python-socks
"""

###USER-AGENT

"""
En este caso se quiso modificar el User-Agent personalizado, pero de igual forma se pueden usar los mas comunes 
o incluso hacerlo de forma aleatoria en:
https://pypi.python.org/pypi/fake-useragent
"""

import sys
import optparse
from requests import get
from requests.exceptions import ConnectionError
from urllib import urlopen
import socks
import socket


def printError(msg, exit = False):
        """
        Imprime mensaje de Error y sale del programa
        """
        sys.stderr.write('Error:\t%s\n' % msg)
        if exit:
            sys.exit(1)

def addOptions():

    """
    Aquí se configuraron las banderas posibles para la ejecución del programa
    """

    parser = optparse.OptionParser()
    parser.add_option('-v','--verbose', dest='verbose', default=None, action='store_true', help='If specified, prints detailed information during execution.')
    parser.add_option('-p','--port', dest='port', default='80', help='Port that the HTTP server is listening to.')
    parser.add_option('-T', '--tor', dest='tor', default=None, action="store_true", help='Make request with TOR')
    opts,args = parser.parse_args()
    return opts
    
def checkOptions(options):
        """
        Verifica que se haya ingresado una dirección de servidor
        """
    if options.server is None:
        printError('Debes especificar un servidor a atacar.', True)

def torito(options):
        """
        Al ingresar la bandera -T, utiliza servidores TOR para realizar el request
        """ 
    if options.tor != None:
        print '\n \t Se usará TOR \n'
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
    else:
        pass

def myip():
        """
        Devuelve la IP pública con la que se está realizando el request
        """
    my_ip = urlopen('http://ip.42.pl/raw').read()
    print 'La IP que se eśtá usando es: ', my_ip



if __name__ == '__main__':
    try:
        opts = addOptions()
        checkOptions(opts)
        torito(opts) 
        myip()
    except Exception as e:
        printError('Ocurrio un error inesperado')
printError(e, True)