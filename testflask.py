from flask import Flask, request, jsonify
import json
import email_server
import helpersigner
import sql_test
from flask import send_file
import pdfcreator
import random
import urllib.request
#import firmador_enviador

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

"""
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    if ('Cache-Control' not in response.headers):
        response.headers['Cache-Control'] = 'public, max-age=600'
    return response
"""

@app.route("/services/mssql/getproductos", methods=["GET", "POST"])
def get_productos():
    #empresa = request.json['empresa_id']
    r = sql_test.get_productos()
    res = []
    for e in r:
        empresa_id,codigo_art, nombre_art = e# e[1],e[2]
        #empresa,cod_principal,cod_corregir,nombre_principal,rgb,color,accion,observaciones,codificacion,des_codificacion,aux = e
        #print(e)
        #print(nombre_art)
        temp = {
                "codigo_art": str(codigo_art).upper(),
                "nombre_art": str(nombre_art).upper(),
               # "cod_corregir": str(cod_corregir),
                #"nombre_principal": str(nombre_principal),
                #"rgb":str(rgb),
                #"color":str(color),
                #"accion":str(accion),
                #"observaciones":str(observaciones),
                #"codificacion":str(codificacion),
                #"des_codificacion":str(des_codificacion),
                #"aux":str(aux)
                }
        res.append(temp)

    return json.dumps(res)  #str(res)


@app.route("/services/mssql/getprice", methods=["GET","POST"])
def get_price():
    cod = request.json['codigo']
    r = sql_test.get_price(cod)
    res=[]
    for e in r:
        codpre_arp,precio_arp=e
        temp = {
	    "codpre_arp":str(codpre_arp),
            "precio_arp":str(precio_arp)
	}
        res.append(temp)
    return json.dumps(res)

@app.route("/services/mssql/getdescuento", methods=["GET","POST"])
def get_descuento():
    cod = request.json['codigo']
    r = sql_test.get_descuento(cod)
    res=[]
    for e in r:
        #tipo no se usa es solo pa llenar
        #por defecto ya bota en porcentaje noma
        porcentaje,tipo=e[0],e[1]
        temp = {
	    "porcentaje":str(porcentaje),
            "tipo":str(tipo)
	}
        res.append(temp)
    return json.dumps(res)





@app.route("/services/mssql/getimpuesto", methods=["GET","POST"])
def get_impuesto():
    cod = request.json['codigo']
    cod = str(cod)
    print("codigo es >  " + cod)
    r = sql_test.get_impuesto(cod)
    res=[]
    for e in r:
        descrip_tim,porcen_tim=e
        temp = {
	    "descrip_tim":str(descrip_tim),
            "porcen_tim":str(porcen_tim)
	}
        res.append(temp)
    return json.dumps(res)

#firma y envia 
@app.route("/services/mssql/send", methods=["GET","POST"])
def send_xml():
    respuesta = ""
    cod = request.form.get('empresa_id')
    xml = request.form.get('xml')
    ambiente = request.form.get('ambiente')
    archivo = open("ultimo.xml", "w+")
    archivo.write(xml)
    cod = str(cod)
    xml = str(xml)
    #print(cod)
    #print(xml)
    # print("codigo es >  " + cod)
    y = str(random.random())
    y = y[2:]
    e = sql_test.get_link_p12(cod)
    #print(e)
    #print(e[0])
    (url_p12, url_pwd) = e[0] #sql_test.get_link_p12(cod)
    print(url_p12)
    url = ""
    res = []
    #for e in r:
    #    url = e
    url = str(url)
    #print (url)
    urllib.request.urlretrieve(url_p12,y+".p12")
    #primero instala la clave
    #xml = helpersigner.genera_clave(xml)
    #procede a firmar
    xml_firmado = helpersigner.firmador(xml,"/root/"+y+".p12", url_pwd)
    archivo2 = open("ultimo-firmado.xml", "w+")
    archivo2.write(xml_firmado.decode())
    #sql_test.update_secuencial()#en db sql server
    #respuesta=helpersigner.enviador(xml_firmado, ambiente) #envia a sri
    #res.append(temp)
    #procede a enviar
    respuesta = helpersigner.enviador(xml_firmado.decode(), ambiente)
    print (respuesta)
    return str(respuesta)


#usar solo en caso de que la factura sea exitosa
@app.route("/services/mssql/save_invoice")
def save_invoice():
    json_data = request.json
    sql_test.save_invoice(json_data)
    return "listo"
 

#
@app.route("/services/mssql/getdocume")
def get_docume():
    r = sql_test.get_docume()
    res = []
    for e in r:
        empresa_id,codigo_doc,descrip_doc,numero_doc = e[0],e[2],e[3],e[9]
        #print(e)
        temp = {
                "empresa_id": str(empresa_id),
                "codigo_doc": str(codigo_doc),
                "descrip_doc": str(descrip_doc),
                "numero_doc": str(numero_doc),
                }
        res.append(temp)
    return json.dumps(res) 

@app.route("/services/mssql/getusuari")
def get_usuari():
    r = sql_test.get_usuari()
    res = []
    for e in r:
        codigo_usu,clave_usu = e
        #print(e)
        temp = {
                "codigo_usu": str(codigo_usu),
                "clave_usu": str(clave_usu),
                }
        res.append(temp)

    return json.dumps(res) 

@app.route("/services/mssql/getempresas")
def get_empresas():
    r = sql_test.get_empresas()
    res = []
    for e in r:
        empresa_id,razsoc_emp,ambien_emp,ruc_emp,direcc_emp = e
        #print(e)
        temp = {
                "empresa_id": str(empresa_id),
                "razsoc_emp": str(razsoc_emp),
                "ambien_emp": str(ambien_emp),
                "ruc_emp": str(ruc_emp),
                "direcc_emp": str(direcc_emp),
                }
        res.append(temp)

    return json.dumps(res) 

@app.route("/services/mssql/getagenci",methods=["GET","POST"])
def get_agencia():
    empresa = request.json['empresa']
    print(empresa)
    r = sql_test.get_agencia(empresa)
    res = []
    for e in r:
        agenci_id,direcc_age,nombre_age = e
        #print(e)
        temp = {
                "agenci_id": str(agenci_id),
                "direcc_age": str(direcc_age),
                "nombre_age": str(nombre_age),
                }
        res.append(temp)

    return json.dumps(res) 

@app.route("/services/mssql/sign",methods=["GET","POST"])
def sign():

    xml = request.json['xml']
    
    print(xml)
    #se pone a firma el xml
    r = firmador_enviador.executor(empresa)
    return json.dumps(res) 

#solo ejemplo
@app.route('/download', methods=["GET","POST"])
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = request.json['filename'] #"/Examples.pdf"
    return send_file(path, as_attachment=True)

@app.route('/getpdfticketname', methods=["GET","POST"])
def getpdfticketname():
    #print(filename+" || >> creado")
    #filename = pdfcreator.crear_ticket()
    tipo = request.json['tipo_pdf']
    cod = request.json['empresa_id']
    razSoc = request.json['razonSocialComprador']
    totalCon = request.json['totalCon']
    totalSin = request.json['totalSin']
    conceptos = request.json['conceptos']
    total = request.json['total']

    #xml = request.json['xml']
    #print("datos para pdf >>> ")
    #print ("[conceptos] "+conceptos)
    #print ("[empresa] "+cod)
    #print ("[razon social] "+razSoc)
    #print ("[total con] "+totalCon)
    #print ("[total sin] "+totalSin)
    #print ("[]"+conceptos)
    #print ("[total] "+total)
    #print ("[json] "+ str(request.json))
    #print (conceptos)

    #entrega el json completo
    if (tipo=='1'):
        filename = pdfcreator.crear_ticket(request.json)
    else: #para pdf factura grande
        #fecha = request.json['fecha']
        filename = pdfcreator.crear_factura(request.json)
    #xml = helpersigner.xmlconclave(xml)
    # clave = request.json['clave']
    #filename = pdfcreator.crear_ticket()
    #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    #response.headers['Pragma'] = 'no-cache'
    #response.headers['Pragma'] = 'no-cache'
    #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return filename



@app.route('/getpdfticket/<string:filename>', methods=["GET","POST"])
#@no_cache
def getpdfticket(filename):
    #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return send_file(filename)

@app.route("/services/mssql/getempres")
def get_empres():
    r = sql_test.get_empres()
    res = []
    for e in r:
        empresa_id,nombre_emp,razsoc_emp,razcom_emp,ruc_emp,direcc_emp,telef1_emp,repres_emp = e[0],e[1],e[2],e[3],e[4],e[5],[6],e[7]
        #print(e)
        temp = {
                "empresa_id": str(empresa_id),
                "nombre_emp": str(nombre_emp),
                "razsoc_emp": str(razsoc_emp),
                "razcom_emp": str(razcom_emp),
                "ruc_emp": str(ruc_emp),
                "direcc_emp": str(direcc_emp),
                "telef1_emp": str(telef1_emp),
                "repres_emp": str(repres_emp),
                }
        res.append(temp)

    return json.dumps(res) 



@app.route("/services/mssql/getclient", methods=["GET","POST"])
def get_client(): 
    cliente = request.json['client']
    empresaid = request.json['empresa_id']
    #print(str(cliente),str(empresaid))
    r = sql_test.get_client(cliente, empresaid)
    res = []
    for e in r:
        codigo_cli,nombre_cli,razsoc_cli,rucci_cli,direcc_cli,telefo_cli,email_cli=e[1],e[2],e[3],e[5],e[13],e[14],e[17]
        #print(e)
        temp = {
                "codigo_cli": str(codigo_cli),
                "nombre_cli": str(nombre_cli),
                "razsoc_cli": str(razsoc_cli),
                "rucci_cli": str(rucci_cli),
                "direcc_cli": str(direcc_cli),
                "telefo_cli": str(telefo_cli),
                "email_cli": str(email_cli),
                }
        res.append(temp)
    print (json.dumps(res))
    return json.dumps(res)

@app.route("/services/mssql/get_secuencial", methods=["GET","POST"])
def get_secuencial(): 
    secuencial = ""
    codDoc = request.json['codDoc']
    empresa = request.json['empresa_id']
    agencia = request.json['agenci_id']
    secuencial = sql_test.get_secuencial(codDoc, empresa, agencia)
    #secuencial = secuencial[0]
    final =""
    for e in secuencial:
        final = str(e [0])
    print (final)
    return final
    #if (request.method == 'POST'):
        ##prcesa
    #    pass
    """
    r = sql_test.get_client(cliente, empresaid)
    res = []
    for e in r:
        codigo_cli,nombre_cli,razsoc_cli,rucci_cli,direcc_cli,telefo_cli=e[1],e[2],e[3],e[5],e[13],e[14]
        #print(e)
        temp = {
                "codigo_cli": str(codigo_cli),
                "nombre_cli": str(nombre_cli),
                "razsoc_cli": str(razsoc_cli),
                "rucci_cli": str(rucci_cli),
                "direcc_cli": str(direcc_cli),
                "telefo_cli": str(telefo_cli),
                }
        res.append(temp)
    return json.dumps(res)
    """

@app.route("/services/mssql/update_secuencial", methods=["GET","POST"])
def update_secuencial(): 
    #secuencial = ""
    codDoc = request.json['codDoc']
    empresa = request.json['empresa_id']
    agencia = request.json['agenci_id']
    #if (request.method == 'POST'):
    res = sql_test.update_secuencial(codDoc, empresa, agencia)
    return str(res)
 
@app.route("/services/mssql/add_user", methods=["GET","POST"])
def add_user(): 
    #if (request.method == 'POST'):
    data = request.json
    res = sql_test.add_user(data)
    return str(res)
 
@app.route("/services/mssql/send_email", methods=["GET","POST"])
def send_email(): 
    data = request.json
    res = sql_test.add_user(data)
    return str(res)
 

#if __name__ == "__main__":
#    app.run(host='0.0.0.0')
