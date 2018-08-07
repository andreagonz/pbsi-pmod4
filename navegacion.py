import time
import requests
from requests import get, post
from requests.exceptions import ConnectionError
from aux import printError

def hacer_peticion(url, proxy, user_agent, intervalo=0, post=False, data=None):
    try:
        time.sleep(intervalo)
        headers = {'User-Agent': user_agent}
        if post:
            # return requests.post(url, headers=headers, proxies=proxy, data=data, verify=False)
            return requests.post(url, headers=headers, proxies=proxy, data=data)
        # return requests.get(url, headers=headers, proxies=proxy, verify=False)
        return requests.get(url, headers=headers, proxies=proxy)
    except ConnectionError:
        printError('Error en la conexion a la url "%s", tal vez el servidor no esta arriba.' % url,
                   True)
    return None
