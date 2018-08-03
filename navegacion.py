import requests
from random import randint
from requests import get
from requests.exceptions import ConnectionError

user_agents = ['firefox', 'chrome']
proxies = [{'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}]

def hacer_peticion(url):
    try:
        headers = {'User-Agent': user_agents[randint(0, len(user_agents) - 1)]}
        return requests.get(url, headers=headers, proxies=proxies[randint(0, len(proxies) - 1)])
    except ConnectionError:
        error('Error en la conexion, tal vez el servidor no esta arriba.', True)
    return None
