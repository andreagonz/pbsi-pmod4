import time
import requests
from requests import get
from requests.exceptions import ConnectionError
from aux import printError

def hacer_peticion(url, proxy, user_agent, intervalo=0):
    try:
        time.sleep(intervalo)
        headers = {'User-Agent': user_agent}
        return requests.get(url, headers=headers, proxies=proxy)
    except ConnectionError:
        printError('Error en la conexion a la url "%s", tal vez el servidor no esta arriba.' % url,
                   True)
    return None
