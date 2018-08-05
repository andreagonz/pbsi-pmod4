from buscador import Resultado
from datetime import datetime

def formato(lst_res, tipo='txt', domains=False):
    if tipo == 'xml':
        res_xml(lst_res, domains)
    elif tipo == 'html':
        res_html(lst_res, domains)
    else:
        res_txt(lst_res, domains)

def res_xml(lst_res, domains=False):
    return 'xml'

def res_html(lst_res, domains=False):
    return 'html'
    
def res_txt(lst_res, domains=False):
    print("Fecha: %s\n" % datetime.now())
    for b, lst in lst_res.items():
        print("Resultados de %s" % b)
        for x in lst:
            print('Url: %s' % x.url)
            print('Titulo: %s' % x.titulo)
            print('%s\n' % x.texto)
        print()
    
