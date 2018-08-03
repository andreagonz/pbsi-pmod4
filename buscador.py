from navegacion import hacer_peticion

class FabricaBuscador():

    def get_buscador(self, nombre):
        if nombre == 'google':
            return BuscadorGoogle()
        if nombre == 'bing':
            return BuscadorBing()
        if nombre == 'duckduckgo':
            return BuscadorDuckduckgo()
        if nombre == 'pastebin':
            return BuscadorPastebin()
        if nombre == 'boardreader':
            return BuscadorBoardreader()
        if nombre == 'zone-h':
            return BuscadorZoneH()
        return None
        
class Resultado():

    def __init__(self, url, titulo, texto):
        self.url = url
        self.titulo = titulo
        self.texto = texto

class Buscador():

    def busqueda(self, s, max_res=50, no_params=False, regex=False):
        return []
            
class BuscadorGoogle(Buscador):

    def busqueda(self, s, max_res=50, no_params=False, regex=False):
        req = hacer_peticion("https://google.com/")
        return []
    
class BuscadorBing(Buscador):

    def busqueda(self, s, max_res=50, no_params=False, regex=False):
        return []
    
class BuscadorDuckduckgo(Buscador):

    def busqueda(self, s, max_res=50, no_params=False, regex=False):        
        return []

class BuscadorPastebin(Buscador):

    def busqueda(self, s, max_res=50, no_params=False, regex=False):
        return []
    
class BuscadorBoardreader(Buscador):

    def busqueda(self, s, max_res=50, no_params=False, regex=False):
        return []
    
class BuscadorZoneH(Buscador):

    def busqueda(self, s, max_res=50, no_params=False, regex=False):
        return []
