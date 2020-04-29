import pyodbc

server = '186.46.45.30'
database = 'desarrollo'
username = 'sa'
password = 'Fedenaligas2017'
driver='{ODBC Driver 17 for SQL Server}'

test = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+password)
#print(test)
cursor = test.cursor()
tsql = "SELECT * FROM sys.databases;"
tsql2 = "go"

#with cursor.execute(tsql):
#	print(67)
with cursor.execute(tsql):
	row = cursor.fetchone()
	while row : 
		#print(row[0])
		row = cursor.fetchone()

def get_productos():
    command = "SELECT empresa_id,codigo_art,nombre_art FROM articu"
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print (row)
    return row

#recpge solo porcentaje
def get_descuentos(codigo):
    command = """
    SELECT valor_arb,codtbo_arb, condic_arb
    FROM artbon
	inner join bonifi ON codigo_bon=codtbo_arb 
	WHERE artbon.empresa_id = '10001'
	  and artbon.codart_arb = '"""+codigo+"""'
	  and artbon.condic_arb = '01'
    """
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print (row)
    return row



def get_secuencial(codDoc, empresa, agencia): #01 para solo factura
    command = "select numero_doc from docume where(codigo_doc = "+codDoc+" and empresa_id = "+empresa+" and agenci_id="+agencia+")" 
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print("[get secuencial] >> " + str(row))
    return row

#suma una unidad al secuencial actual
def update_secuencial(codDoc, empresa, agencia): #01 para solo factura
    actual = get_secuencial(codDoc, empresa, agencia)
    sec_actual= ""
    for e in actual:
        sec_actual = str(e[0])

    sec_actual = int(sec_actual)
    #print (sec_actual)
    sec_actual += 1
    sec_actual = str(sec_actual)
    zeros_len = 9-len(sec_actual)
    zeros = []
    zeros_cadena = ""
    for e in range(zeros_len):
        zeros_cadena+="0"
    #pone todo junto
    sec_final = zeros_cadena + sec_actual
    #print ("secfinal >>>" + sec_final)
    #command = "select numero_doc from docume where(codigo_doc = "+codDoc+" and empresa_id = "+empresa+" and agenci_id="+agencia+")" 
    command = "update docume set numero_doc = '"+sec_final+"' where(codigo_doc = "+codDoc+" and empresa_id = "+empresa+" and agenci_id="+agencia+")"
    row = ''
    with cursor.execute(command):
        pass
        #row = cursor.fetchall()
    #print("[update secuencial] >> " + str(row))
    pass



#no usado
def updatexxx_secuencial(empresa,agencia,coddoc):
    num = get_secuencial(empresa,agencia,coddoc)
    #print ("[set_]")
    nuevo = int(num)
    #print("[set_secuencial] >> "+str(nuevo))
    nuevo = nuevo+1
    command = "update docume set numero_doc = "+str(nuevo)+" where(codigo_doc = 001 and empresa_id ="
    command+=empresa+"and agenci_id="+agencia+")"
    #print ("[set_secuencial] >> "+command)
    with cursor.execute(command):
        row = cursor.fetchall()
    #print ("[set_secuencial] >> "+str(row))
    pass


def add_user(data_json):
    na = data_json['nombre']
    em = data_json['email']
    ru = data_json['ruc']
    numero = data_json['numero']
    pass


def save_invoice(json_data):
    #extarct the data
    command = ""
    row=''
    with cursor.execute(command):
        row = cursor.fetchall()
    return row


def get_image(empresa_id):
    #extarct the data
    #print("empresa imagen >> "+empresa_id)
    command = "select logo_emp from empres where(empresa_id = "+empresa_id+")"
    row=''
    with cursor.execute(command):
        row = cursor.fetchall()
    return row



def get_link_p12(empresa_id):
    command = "select urlfir_emo,clavfg_emp from empres where(empresa_id="+empresa_id+")"
    #command="select codpre_arp,precio_arp from artpre where(codart_arp like '%"
    #command+=codigo+"%' and precio_arp!=0)"
    row=''
    with cursor.execute(command):
        row = cursor.fetchall()
    return row




def get_price(codigo):
    command="select codpre_arp,precio_arp from artpre where(codart_arp like '%"
    command+=codigo+"%' and precio_arp!=0)"
    row=''
    with cursor.execute(command):
        row = cursor.fetchall()
    return row

def get_impuesto(codigo):
    #obtiene codigo de impuesto
    command1 = "select codtar_ari from artimp where(codart_ari like '%"
    #print(command1)
    command1 += str(codigo)+"%')"
    row=''
    #print("query 1 ")
    #print(command1)
    with cursor.execute(command1):
        row=cursor.fetchall()
    codigo_precio = 0
    for e in row:
        codigo_precio = str(e[0])
    command2 = "select descrip_tim,porcen_tim from tarimp where(codtar_tim='"
    command2+= str(codigo_precio) + "')"
    row2 = ''
    #print("query 2")
    #print(command2)
    with cursor.execute(command2):
        row2 = cursor.fetchall()
    return row2

def get_docume():
    #command = "SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.productos')"
    command = "SELECT * FROM docume"
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print (row)
    return row
def get_usuari():
    #command = "SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.productos')"
    command = "SELECT codigo_usu,clave_usu FROM usuari"
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print (row)
    return row

def get_client():
    #command = "SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.productos')"
    command = "SELECT * FROM client"
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print (row)
    return row



def get_empres():
    #command = "SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.productos')"
    command = "SELECT * FROM empres"
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print (row)
    return row

def get_empresas():
    #command = "SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.productos')"
    #command = "SELECT empresa_id,razsoc_emp, FROM empres"
    command = "select empresa_id, razsoc_emp, ambien_emp,ruc_emp, direcc_emp from empres"
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print (row)
    return row
def get_agencia(empresa):
    #command = "SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.productos')"
    command = "SELECT agenci_id,direcc_age,nombre_age FROM agenci WHERE(empresa_id="+empresa+")"
    #print(command)
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print (row)
    return row

def get_client(cliente, empresaid):
    #command = "SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.productos')"
    command = "select * from client where (rucci_cli like '%"
    command+= cliente+"%' or codigo_cli LIKE'%"+cliente+"%' or nombre_cli like '%"+cliente+"%' and empresa_id="+empresaid+" )"
    #print(command)
    row = ''
    with cursor.execute(command):
        row = cursor.fetchall()
    #print (row)
    return row





