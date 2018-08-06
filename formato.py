#!/usr/bin/python3
# -*- coding: utf-8 -*-

from buscador import Resultado
from datetime import datetime
from urllib.parse import urlparse

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
    print("Fecha: %s\n" % datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
    for b, lst in lst_res.items():
        print("RESULTADOS DE %s" % b.upper())
        print("Número de resultados: %d\n" % len(lst))
        if domains:
            l = list(set([urlparse(x.url).netloc for x in lst]))
            for x in l:
                print(x)
        else:
            for x in lst:
                print('Url: %s' % x.url)
                print('Titulo: %s' % x.titulo)
                print('%s\n' % x.texto)
    
