# simple_demo.py
from fpdf import FPDF
import random
import json
import sql_test
from PIL import Image
import io
from datetime import date
#import treepoem
from barcode import Gs1_128
from barcode.writer import ImageWriter
from io import BytesIO

today = date.today()

#datos de xml
razon_social = ""#"MATADERO Y CARNES FRIAS CIA. LTDA."
nombre_empresa = ""#"MATADERO Y CARNES FRIAS CIA. LTDA."
ruc = ""#"567890237327327"
dire_matriz = ""#'francelana guayaques av 8987'
# linea = '_________'
clave_acceso = ""#'12349947287323327'
factura_no = ""#'123-122-123232323484'
fecha_de_emision= ""#'09/32/2323'
razon_social_apellidos=""#'CONSUMIDOR FINAL'
ruc_ci=""#'999999999999'

producto1 = '2','jabon','21','42'
producto2 = '1','jabon','12','12'
producto3 = '3','jabon','2','6'

def crear_ticket(json_data):
    data_total = json_data['total']
    data_total_sin = json_data['totalSin']
    data_empresa = json_data['empresa_id']
    data_raz_soc = json_data['razonSocial']
    data_raz_soc_com = json_data['razonSocialComprador']
    data_conceptos = json_data['conceptos']
    data_conceptos = json.loads(data_conceptos.replace("'",'"'))
    #print("[pdf creator] coneptos >>")
    #print (data_conceptos)
    #print("[pdf creator muestra] >> ")
    #print (data_conceptos[0])
    nombre = str(random.random()).replace(".","") + ".pdf"
    
    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.set_left_margin(18)
	# pdf.set_line_width(20)
	# pdf.cell(200, 10, txt="Claro pe mascota!", ln=1, align="C")
    pdf.multi_cell(80, 5, txt="",border=0,align='C')
    pdf.multi_cell(80, 5, txt="",border=0,align='C')
    pdf.multi_cell(80, 5, txt="",border=0,align='C')
    pdf.set_font("Arial", size=20)
    pdf.multi_cell(80, 10, txt=data_raz_soc,border=1,align='C')
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(80, 5, txt="RUC.:"+json_data['ruc'],border=1,align='C')
    pdf.set_font("Arial", size=12)
    #pdf.multi_cell(80, 5, txt="RUC: "+ruc)
    #pdf.cell(80, 5, txt='-----------------------------------------------', ln=1)
    pdf.multi_cell(80, 5, txt='DIR MATRIZ :\n' +json_data['dirMatriz'],border=1)
    #pdf.cell(80, 5, txt='-----------------------------------------------', ln=1)
    pdf.multi_cell(80, 5, txt='Aut./Clave Acceso:\n'+json_data['clave'],border=1)
    #pdf.multi_cell(80, 5, txt=calcula_clave(json_data))
    #pdf.cell(80, 5, txt='__________________________________', ln=1)
    #pdf.multi_cell(80, 5, txt='______________')
    pdf.multi_cell(80, 5,border=1, txt='FACTURA No:'+json_data['factura_no'])
    d4 = today.strftime("%b-%d-%Y")
    pdf.multi_cell(80, 5, border=1,txt='FECHA EMISION:'+ str(d4))
    pdf.multi_cell(80, 5,border=1 ,txt='RAZON SOCIAL: '+json_data['razonSocialComprador'])
    #pdf.multi_cell(80, 5, border=1,txt='CONSUMIDOR FINAL')
    pdf.multi_cell(80, 5, border=1,txt='RUC:'+json_data['rucComprador'] )
    #pdf.cell(80, 5, txt='__________________________________', ln=1)
    #pdf.cell(80, 5, txt='__________________________________', ln=1)
    #pdf.multi_cell(80, 5, t        xt='cant')
    #pdf.cell(80, 5, txt='__________________________________', ln=1)
    col_width = pdf.w / 8.5
    row_height = pdf.font_size
    
    data = [['Cant', 'Producto', 'P.unit.', 'Total'],
	            ['1', 'Driscoll', '12.45', '5555'],
	            ['23', 'Doe', '23.45', '1245'],
	            ['2', 'Ma', '12.3', '5321']
	            ]

    data2 = data_conceptos
	# con = 0
    """
    for row in data:
	        con = 0
	        for item in row:
	                if (con == 0):
	                        pdf.cell(pdf.w/15, row_height*1,
	                                txt=item, border=1)
	                else:
	                        pdf.cell(pdf.w/10, row_height*1,
	                                txt=item, border=1)
	                con+=1
	        pdf.ln(row_height*1)
"""
    xd = ['Producto','Cant.','Uni.','Tot.','impuesto']

    #pdf.cell(80, 5, txt='__________________________________', ln=1)

    for e in xd[1:]:
        pdf.cell(20, row_height*1,txt=e,border=1)
    
   # pdf.multi_cell(80, 5, txt="",border=0,align='C')
    #pdf.multi_cell(80, 5, txt='__________________________________')
    pdf.multi_cell(80, 5, txt="",border=0,align='C')
    for row in data2:
        con = 0
        #pdf.cell(80, 5, txt='__________________________________', ln=1)
        for item in row.values():
            if (con == 0):
                #pdf.cell(pdf.w/15, row_height*1,txt=item,border=1,ln=4)
                #pdf.multi_cell(80, row_height*1,txt=xd[con],border=1)
                pdf.multi_cell(80, row_height*1,txt="    "+item.lower(),border=1)
            else:
                #pdf.cell(pdf.w/10, row_height*1,txt=item,border=1,ln=4)

                pdf.cell(20, row_height*1,txt=item[:6],border=1)
                #pdf.cell(20, 9,txt=xd[con]+"\n"+item[:6],border=1)
            con +=1
        pdf.ln(row_height)

    try:

        sub_imp = float(data_total) - float(data_total_sin)

        total =  float(data_total) 
        pdf.cell(80, 5,border=1 ,txt='Subtotal 12%: '+ str( round(total,2))  )
        pdf.multi_cell(80, 5, txt="",border=0,align='C')
        pdf.cell(80, 5,border=1 ,txt='Subtotal 0%: '+ data_total_sin)
        pdf.multi_cell(80, 5, txt="",border=0,align='C')
        pdf.cell(80, 5,border=1 ,txt='Subtotal : '+ data_total_sin)
        pdf.multi_cell(80, 5, txt="",border=0,align='C')
        pdf.cell(80, 5,border=1 ,txt='Descuento: '+ "0" )
        pdf.multi_cell(80, 5, txt="",border=0,align='C')
        pdf.cell(80, 5,border=1 ,txt='Iva 12%: '+ str( round(sub_imp,2) )) 
        pdf.multi_cell(80, 5, txt="",border=0,align='C')
        pdf.cell(80, 5,border=1 ,txt='Valor Total: '+ str( round(total,2)) )
    except:
        pass
    #pdf.cell(10,row_height, border=1, ln=1,txt=producto1[0],align='C')
    pdf.output(nombre)
    return nombre

def calcula_clave(json_file):
    return "657897654678654678"
 
def crear_factura(json_data):
    nombre = str(random.random()).replace(".","") + ".pdf"
    raSoc = json_data['razonSocial']
    ambie = json_data['ambiente']
    empre = json_data['empresa_id']
    ruc   = json_data['ruc']
    secue = json_data['secuencial']
    matriz = json_data['dirMatriz']
    sucursal = json_data['dirSucursal']
    raSocComprador = json_data['razonSocialComprador']
    totalCon = json_data['totalCon']
    totalSin = json_data['totalSin']
    clave = json_data['clave']
    
    data_image_hex = sql_test.get_image(json_data['empresa_id'])
    #print ("contenido imagen >"+ str(data_image_hex) ) 
    #print ("contenido imagen asegurado >"+ str(data_image_hex[0][0]) )
    
    #print ( type(data_image_hex[0][0]) )

    data_image_hex = data_image_hex[0][0]
    #print 
    nombre_image = nombre[:-4]+ ".png"
    data_image = data_image_hex  #bytes.fromhex(data_image_hex[:])
    image = Image.open(io.BytesIO(data_image))
    image.save(nombre_image)
    

#    with open( nombre_image, 'wb' ) as file:
#        file.write(str(data_image))


    
    #raSoc = json_data['razonSocial'
    fecha = json_data['fecha']
    rucComprador = json_data['rucComprador']
    data_conceptos = json_data['conceptos']
    data_conceptos = json.loads(data_conceptos.replace("'",'"'))
    pdf = FPDF(format='A4')
    pdf.add_page()
    pdf.set_font("Times", size=12)
    pdf.set_top_margin(2)
    w = pdf.w
    h = pdf.h

    pdf.set_xy(w/2,10)
    #pdf.cell(100,20,'descridddocion')
    pdf.multi_cell(w/2-15, 5, 'Ruc: '+ruc+'\n\nFACTURA\n\nNo:'+secue+'\nNumero Autorizacion.:\n56785456787656783212\nAMBIENTE:'+ambie+'\nEmision: Normal\nClave de Acceso: '+clave,1 )

    pdf.set_font("Times", size=10)
    pdf.set_xy(10,10)
    #print (w,h)
    #imagen
    pdf.multi_cell(w/2-15, 35, ' ',1 )
    pdf.image(nombre_image,15,10,70,35)
    pdf.set_x(10)
    pdf.multi_cell(w/2-15, 5,json_data['razonSocial']+'\nDir Matriz:\nDir'+json_data['dirMatriz']+'\nDir Sucursal: '+json_data['dirSucursal']+'\nContribuyente especial No:\nObligado a llevar contabilidad: No',1 )



    #rv = BytesIO()
    #Gs1_128(str(1000009078328787422482382922), writer=ImageWriter()).write(rv)
    tempito = pdf.get_y()
    pdf.multi_cell(w-20, 25, ' ',0)
    tempi_post = pdf.get_y()
    # or sure, to an actual file:
    with open(nombre[:-4]+'cc.png', 'wb') as f:
        Gs1_128("2503202001179184241300120010010000030190000061611", writer=ImageWriter()).write(f)
    
    pdf.image(nombre[:-4]+'cc.png',40,tempito+1,140,25)
    #======== informacion del cliente =======
    pdf.set_x(30)
    pdf.set_xy(30,tempi_post)
    pdf.set_font("Arial", size=16)
    pdf.cell(60, 10, 'INFORMACION DEL CLIENTE', 0, 1, 'C')
    #pdf.cell
    pdf.set_x(10)
    pdf.set_font("Arial", size=12)
    d4 = today.strftime("%b-%d-%Y")

    pdf.multi_cell(w-25, 10, 'Razon Social:\t '+raSocComprador+'\nRUC/CI:\t\t'+rucComprador+'\nFecha de Emision: '+ str(d4),1 )

    #========= SECCION PRODUCTOS ===========
    #heades
    pdf.set_x(10)
    pdf.cell(60, 10, '', 0, 1, 'C')
    pdf.set_font("Arial", size=11)
    pdf.set_x(10)
    pdf.cell(30,10,'Codigo',1)
    #pdf.cell(25,10,'Cod Alterno',1)
    pdf.cell(20,10,'Cantidad',1)
    pdf.cell(75,10,'Descripcion',1)
    pdf.cell(20,10,'P.unitario',1)
    pdf.cell(10,10,'Desc.',1)
    pdf.cell(25,10,'Precio. Total',1)
    #escribe espacios blancos
    pdf.set_x(10)
    pdf.cell(60, 10, '', 0, 1, 'C')
    pdf.set_x(10)
    #pdf.cell(30,10,'',1)
    #pdf.cell(20,10,'.',1)
    #pdf.cell(30,10,'',1)
    col_width = pdf.w / 8.5
    row_height = pdf.font_size
    #df.cell(30,10,'',1)
    #pdf.multi_cell(80, 5, txt="",border=0,align='C')
    #pdf.multi_cell(80, 5, txt="",border=0,align='C')
    pdf.set_font("Arial", size=9)
    #print (data_conceptos)
    x = pdf.get_x()
    y = pdf.get_y()
    for row in data_conceptos:
        con = 0
        #print (row['nombre'])
        #print (row['unitario'])
        #print (row['cantidad'])
        #print (row['total'])
        #print (row['impuesto'])
        #print (row['codigo'])
        temporal = [row['codigo'] , row['cantidad'], row['nombre'], row['unitario'],
                    row['impuesto'],row['total']]
        #x = pdf.get_x()
        #y = pdf.get_y()
        #pdf.set_xy(pdf.get_x(),pdf.get_y())
        #for casilla in temporal:
        if (len(row['nombre'])>28 ):
            row_height = 5
        else:
            row_height = 5#pdf.font_size+2
        pdf.multi_cell(30, row_height*1,txt=row['codigo'].lower(),border=1)
        pdf.set_xy(x+30,y)
        pdf.multi_cell(20, row_height*1,txt=row['cantidad'],border=1)
        pdf.set_xy(x+50, y)
        pdf.multi_cell(75, row_height*1,txt=row['nombre'].replace(" ","-").lower(),border=1)
        pdf.set_xy(x+125, y)
        pdf.multi_cell(20, row_height*1,txt=row['unitario'],border=1)
        pdf.set_xy(x+145, y)
        pdf.multi_cell(10, row_height*1,txt="0",border=1)
        pdf.set_xy(x+155, y)
        pdf.multi_cell(25, row_height*1,txt=row['total'],border=1)
        pdf.set_xy(x+175, y)
        pdf.multi_cell(80, 5, txt="",border=0,align='C')
        y = pdf.get_y()
        """
        #pdf.cell(80, 5, txt='__________________________________', ln=1)
        for item in row.values():
            if (con == 0):
                #pdf.cell(pdf.w/15, row_height*1,txt=item,border=1,ln=4)
                #pdf.multi_cell(80, row_height*1,txt=xd[con],border=1)
                pdf.multi_cell(80, row_height*1,txt="    "+item.lower(),border=1)
            else:
                #pdf.cell(pdf.w/10, row_height*1,txt=item,border=1,ln=4)
                pdf.cell(20, row_height*1,txt=item[:6],border=1)
                #pdf.cell(20, 9,txt=xd[con]+"\n"+item[:6],border=1)
            con +=1
        pdf.ln(row_height)
"""

    #seccion informacion adicional
    pdf.set_x(10)
    pdf.set_x(10)
    pdf.cell(60, 10, '', 0, 1, 'C')
    pdf.cell(60, 10, '', 0, 1, 'C')
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", size=12)
    pdf.cell(60, 10, 'INFORMACION ADICIONAL', 0, 1, 'C')

    tem = pdf.get_y()
    pdf.multi_cell(w/2+5, 7, 'Direccion: '+sucursal+'\nEmail: \nTelefonos:\nVendedor:\nObservacion: ',1 )
    #seccion datos totales

    pdf.set_xy(w/2+20,tem)
    pdf.multi_cell(w/2-40, 7, 'Subtotal 12%: XXXXX\nSubtotal 0%: \nSubtotal : \nDescuento: \n ICE : \nPropina: 0.0\nIva 12%: \nValor total:'+totalSin,1 )

    #pdf.output("test.pdf","F")
    pdf.output(nombre)
    return nombre

"""
def crear_factura():
	nombre = str(random.random()).replace(".","") + ".pdf"
	pdf = FPDF(format='A4')
	pdf.add_page()
	pdf.set_font("Arial", size=14)
	pdf.set_left_margin(18)
	# pdf.set_line_width(20)
	# pdf.cell(200, 10, txt="Claro pe mascota!", ln=1, align="C")

	pdf.multi_cell(80, 5, txt=razon_social,border=1,align='C')
	pdf.set_font("Arial", size=12)
	pdf.multi_cell(80, 5, txt=nombre_empresa,border=1)
	pdf.multi_cell(80, 5, txt="RUC: "+ruc)
	pdf.multi_cell(80, 5, txt='DIR MATRIZ :' +dire_matriz)
	pdf.cell(80, 5, txt='__________________________________', ln=1)
	pdf.multi_cell(80, 5, txt='AUTORIZACION/clave_acceso')
	pdf.multi_cell(80, 5, txt=clave_acceso)
	pdf.multi_cell(80, 5, txt='______________')
	pdf.multi_cell(80, 5, txt='FACTURA No:'+factura_no)
	pdf.multi_cell(80, 5, txt='FECHA EMISION:'+fecha_de_emision)
	pdf.multi_cell(80, 5, txt='RAZON SOCIAL: '+razon_social_apellidos)
	pdf.multi_cell(80, 5, txt='CONSUMIDOR FINAL')
	pdf.multi_cell(80, 5, txt='RUC:' + ruc_ci,)
	pdf.cell(80, 5, txt='__________________________________', ln=1)

	pdf.multi_cell(80, 5, txt='cant')
	pdf.cell(80, 5, txt='__________________________________', ln=1)

    col_width = pdf.w / 8.5
	row_height = pdf.font_size
    xd = ['Producto','Cant.','Uni.','Tot.','']
    for row in data2:
        con = 0
        for item in row.values():
            if (con == 0):
                #pdf.cell(pdf.w/15, row_height*1,txt=item,border=1,ln=4)
                pdf.multi_cell(80, row_height*1,txt=xd[con],border=1)
                pdf.multi_cell(80, row_height*1,txt=item.lower(),border=1)
            else:
                #pdf.cell(pdf.w/10, row_height*1,txt=item,border=1,ln=4)

                pdf.cell(20, row_height*1,txt=item[:6],border=1)
                #pdf.cell(20, 9,txt=xd[con]+"\n"+item[:6],border=1)
            con +=1
        pdf.ln(row_height)

    pdf.cell(10,row_height, border=1, ln=1,txt=producto1[0],align='C')
    pdf.output(nombre)
    return nombre
"""
# crear_ticket()
