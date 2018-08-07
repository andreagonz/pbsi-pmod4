import sys

email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
user_agents = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0']
# proxies = [None]
# proxies = [{'http':  'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}]
proxies = [None, {'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}]
# user_agents = ['firefox', 'chrome']

def printError(e, exit = False):
    """
    Imprime mensaje de Error y sale del programa
    """
    sys.stderr.write('Error:\t%s\n' % str(e))
    # raise e
    if exit:
        sys.exit(1)
