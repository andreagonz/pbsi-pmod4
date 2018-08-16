#!/usr/bin/python3
# -*- coding: utf-8 -*-

from buscador import Resultado
from datetime import datetime
from urllib.parse import urlparse


from lxml import etree


def formato(lst_res, tipo='txt', domains=False, nombre='resultados', verboso=False):
    if verboso:
        print("Escribiendo reporte con formato %s." % tipo)
    if tipo == 'xml':
        res_xml(lst_res, domains, nombre)
    elif tipo == 'html':
        res_html(lst_res, domains, nombre)
    else:
        res_txt(lst_res, domains, nombre)

def res_xml(lst_res, domains=False, nombre='resultados'):



    f = open ('%s.xml' % nombre, 'w')
       
    #f.write("###########################\n")
    #f.write("Fecha: %s\n" % datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
    for b, lst in lst_res.items():
        #root = etree.Element('root')
        f.write("<root>")

        fecha = etree.Element('Fecha')
        fecha.text = str("Fecha: %s\n" % datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
        s = etree.tostring(fecha) 
        f.write(str(s))
        Resultados = etree.Element('Resultados')
        Resultados.text = str("RESULTADOS DE %s \n" % b.upper())
        s = etree.tostring(Resultados) 

        f.write(str(s))
        #f.write("Número de resultados: %d\n" % len(lst))
        if domains:
            l = list(set([urlparse(x.url).netloc for x in lst]))
            root = etree.Element('root')
            domi = etree.Element('Dominio')
            otro = etree.Element('Busqueda')
            
            for x in l:             
                domi.text = str(x)
                otro.append(domi)
                s = etree.tostring(otro) 
                f.write(str(s))
            f.write("</root>")


        else:
            root = etree.Element('root')
            titulo = etree.Element('Titulo')
            url = etree.Element('Url')
            desc = etree.Element('Descripcion')
            otro = etree.Element('Busqueda')
           
            for x in lst:
                titulo.text = str(x.titulo)
                url.text = str(x.url)
                desc.text = str(x.texto)
                otro.append(titulo)
                otro.append(url)
                otro.append(desc)
                s = etree.tostring(otro) 
                f.write(str(s))
            f.write("</root>")
        #f.write("\n###########################\n")
    f.close()

    

    return 'xml'

def res_html(lst_res, domains=False, nombre='resultados'):
    f = open ('%s.html' % nombre,'w')
    salto = "<br>"   
    f.write("###########################%s"%salto)
    f.write("%sFecha: %s%s" % (salto,datetime.now().strftime('%d-%b-%Y %H:%M:%S'),salto))
    

    tabla = """
    <br>
    <br>
<html>
<body>
<table>
    <td WIDTH="550" 
        HEIGHT="10">%s</td>
    <td WIDTH="325" 
        HEIGHT="10">%s</td>
    <td WIDTH="1000" 
        HEIGHT="10">%s</td>
  
</table>
</body>
</html>
"""

    tabla_domi = """
    <br>
    <br>
<html>
<body>
<table>
    <td WIDTH="550" 
        HEIGHT="10">%s</td>
</table>
</body>
</html>
"""

    titulo_domi = """
    <br>
    <br>
<html>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
    text-align: left;    
}
</style>
<body>
<table style="width:29%">
  <tr>
    <th>Url</th>
  </tr> 
</table>
</body>
</html>
  """

    titulo = """
    <br>
    <br>
<html>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
    text-align: left;    
}
</style>
<body>
<table style="width:100%">
  <tr>
    <th>Titulo</th>
    <th>Url</th> 
    <th>Descripcion</th>
  </tr> 
</table>
</body>
</html>
  """

    for b, lst in lst_res.items():
        
        f.write("%s %s RESULTADOS DE %s %s %s" % (salto,salto,b.upper(),salto,salto))
        f.write("Numero de resultados: %d %s" % (len(lst),salto))
        
        if domains:
            f.write(titulo_domi)
            l = list(set([urlparse(x.url).netloc for x in lst]))
            for x in l:
                f.write(tabla_domi%x)
        else:
            f.write(titulo)
            for x in lst:
                f.write((tabla%(x.titulo,x.url,x.texto)))
                #f.write(tabla)
        f.write("\n###########################\n")
    f.close()

    return 'html'
    
    
def res_txt(lst_res, domains=False, nombre='resultados'):

    f = open ('%s.txt' % nombre,'w')
       
    f.write("###########################\n\n")
    f.write("Fecha: %s" % datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
    for b, lst in lst_res.items():
        f.write("\n\n###########################\n\n")
        f.write("RESULTADOS DE %s \n" % b.upper())
        f.write("Número de resultados: %d\n" % len(lst))
        if domains:
            l = list(set([urlparse(x.url).netloc for x in lst]))
            for x in l:
                f.write(x)
                f.write("\n")
        else:
            for x in lst:
                f.write('\n\nUrl: %s' % x.url)
                f.write('\nTitulo: %s' % x.titulo)
                f.write('\n%s' % x.texto)
    f.close()
    
