import requests
from requests import get
from requests.exceptions import ConnectionError

def printError(msg, exit = False):
    """
    Imprime mensaje de Error y sale del programa
    """
    sys.stderr.write('Error:\t%s\n' % msg)
    if exit:
        sys.exit(1)

def hacer_peticion(url, proxy, user_agent):
    try:
        headers = {'User-Agent': user_agent}
        return requests.get(url, headers=headers, proxies=proxy)
    except ConnectionError:
        printError('Error en la conexion a la url "%s", tal vez el servidor no esta arriba.' % url,
                   True)
    return None
