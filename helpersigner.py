import os
from sri import xades
from sri import mod11
#from sri import mainFinal
import base64



d_fecha = ""
d_tipocomprobante = ""
d_ruc = ""
d_tipoambiente = ""
d_serie = ""
d_numerosecuencial = ""
d_codigonumerico = ""
d_tipoemision=""

def leeCampo(cadena):
    campo = "<ambiente>"
    indx = cadena.index(campo) + len(campo)
    d_tipoambiente = cadena[indx:indx+1]
    print ("ambiente > "+d_tipoambiente)
#elif (campo == "<tipoEmision>"):
#if ("<tipoEmision>" in cadena):
    campo = "<tipoEmision>"
    indx = cadena.index(campo) + len(campo)
    d_tipoemision  = cadena[indx:indx+1]
    print ("tipo emision >" +d_tipoemision)
#elif (campo == "<ruc>"):
#if ("<ruc>" in cadena):
    campo = "<ruc>"
    indx = cadena.index(campo) + len(campo)
    d_ruc = cadena[indx:indx+13]
    print ("ruc >"+d_ruc)
#elif (campo == "<codDoc>"):  #COD DOG ES TIPO DE EMISION
#if ("<codDoc>" in cadena):
    campo = "<codDoc>"
    indx = cadena.index(campo) + len(campo)
    d_tipocomprobante = cadena[indx:indx+2]
    print ("tipo comprobante > "+d_tipocomprobante)
#elif (campo == "<secuencial>"):
#if ("<secuencial>" in cadena):
    campo = "<secuencial>"
    indx = cadena.index(campo) + len(campo)
    d_numerosecuencial = cadena[indx:indx+9]
    print ("<secuencial> "+ d_numerosecuencial)
#"""para serie"""
#elif (campo == "<ptoEmi>"):
#if ("<ptoEmi>" in cadena):
    campo = "<ptoEmi>"
    indx = cadena.index(campo) + len(campo)
    d_serie = cadena[indx:indx+3]
    #print (d_serie)
#elif (campo == "<estab>"):
#if ("<estab>" in cadena):
    campo = "<estab>"
    indx = cadena.index(campo) + len(campo)
    d_serie += cadena[indx:indx+3]
    print ("<estab> "+d_serie)
#---fecha---
#elif (campo == "<fechaEmision>"):
#if ("<fechaEmision>" in cadena):
    campo = "<fechaEmision>"
    indx = cadena.index(campo) + len(campo)
    d_fecha = cadena[indx:indx+10]
    print ("<fechaEmision>"+d_fecha)
    d_fecha=d_fecha.replace("/","")
    #print (d_fecha)
    return d_fecha+d_tipocomprobante+d_ruc+d_tipoambiente+d_serie+d_numerosecuencial+d_codigonumerico+"12345678"+d_tipoemision, d_tipoambiente



def creaclaveAcceso(c48digs):
    clave = c48digs
    print("[creaclaveAcceso clave] > "+ c48digs)
    temp = mod11.numero_verificador(clave)
    print ("[creaclaveAcceso]> "+ temp)
    clave+=str(temp)
    #print ("creaclaveAcceso> "+clave)
    return clave


"""el campo <claveAcceso><> debe estar vacio"""
def getXMLconCA(cadena):
    xmlConClaveFinal=""
    c48xxx,ambiente = leeCampo(cadena)
    print("[c48xxx] > "+c48xxx)

    clave = creaclaveAcceso(c48xxx)
    print ("[get xml con ca ] >>" + clave)
    #print ("getxml..> "+clave)
    if ("<claveAcceso>" in cadena):
        indx = cadena.index("<claveAcceso>") + len("<claveAcceso>")
        """borra anterior clave de acceso"""
        parteAtras = cadena[indx:]
        parteAtras = parteAtras[parteAtras.index("<"):]
        """termina borrado"""
        #xmlConClaveFinal = cadena[0:indx] + clave + cadena[indx:]
        xmlConClaveFinal = cadena[0:indx] + clave + parteAtras
    return xmlConClaveFinal, ambiente, clave


def genera_clave(xml):
    xml_clave = ""
    temp = xml
    res = ""
    #todo:res

     
    return res


#crea la clave de acceso de xml
def setClave(xml):
    finxml,ambiente,clave = getXMLconCA(xml)
    #procesa
    return finxml, ambiente, clave


def firmador(xml, pathP12, pwd):
    pwd_t = pwd
    pathP12_t =  pathP12
    print ("[path de centiifcado] > " + pathP12_t)

    pwd_enc = pwd_t.encode('ascii')
    pathP12_enc = pathP12_t.encode('ascii')

    respuesta=""
    print ("[se procesara : xml ] > " + xml)
    print ("[se procesara : path12 ] > " + pathP12)
    print ("[se procesara : pwd ] > " + pwd)
    xml_completo, ambiente, claveAcceso = getXMLconCA(xml)
    pwd_biteado = base64.b64encode(pwd_enc)
    pathP12_biteado = base64.b64encode(pathP12_enc)
    #pwd_biteado = bytes(pwd, "utf-8")
    #pathP12_biteado = bytes(pathP12, "utf-8")
    test = xades.Xades()
    respuesta = test.sign(xml_completo,pathP12_enc,pwd_enc)
    return respuesta
