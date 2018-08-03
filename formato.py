from buscador import Resultado

def formato(lst_res, tipo='txt', domains=False):
    if tipo == 'xml':
        return res_xml(lst_res, domains)
    if tipo == 'html':
        return res_html(lst_res, domains)
    return res_txt(lst_res, domains)

def res_xml(lst_res, domains=False):
    return xml

def res_html(lst_res, domains=False):
    return html
    
def res_txt(lst_res, domains=False):
    return txt
