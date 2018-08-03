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
        
class Resultado():

    def __init__(self, u, t):
        self.url = u
        self.texto = t

class Buscador():

    def busqueda(self, s):
        return None
    
    def formato(lst_res, tipo='txt'):
        if tipo == 'xml':
            return res_xml(lst_res)
        if tipo == 'html':
            return res_html(lst_res)
        return res_txt(lst_res)

    def res_xml(lst_res):
        return xml

    def res_html(lst_res):
        return html

    def res_txt(lst_res):
        return txt
        
class BuscadorGoogle(Buscador):

    def busqueda(self, s):
        return []
    
class BuscadorBing(Buscador):

    def busqueda(self, s):
        return []
    
class BuscadorDuckduckgo(Buscador):

    def busqueda(self, s):
        
        return []

class BuscadorPastebin(Buscador):

    def busqueda(self, s):
        return []
    
class BuscadorBoardreader(Buscador):

    def busqueda(self, s):
        return []
    
class BuscadorZoneH(Buscador):

    def busqueda(self, s):
        return []
    

"""
fabrica = FabricaBuscador()
google = fabrica.get_buscador('google')
ddg = fabrica.get_buscador('duckduckgo')
google.busqueda(s)
ddg.busqueda(s)
"""