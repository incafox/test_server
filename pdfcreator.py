# simple_demo.py
from fpdf import FPDF
import random
import json

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
    pdf.multi_cell(80, 5,border=1, txt='FACTURA No:'+"1234543434343434")
    pdf.multi_cell(80, 5, border=1,txt='FECHA EMISION:'+json_data['fecha'])
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
        pdf.cell(80, 5, txt='__________________________________', ln=1)
        for item in row.values():
            if (con == 0):
                #pdf.cell(pdf.w/15, row_height*1,txt=item,border=1,ln=4)
                #pdf.multi_cell(80, row_height*1,txt=xd[con],border=1)
                pdf.multi_cell(80, row_height*1,txt="    "+item.lower(),border=0)
            else:
                #pdf.cell(pdf.w/10, row_height*1,txt=item,border=1,ln=4)

                pdf.cell(20, row_height*1,txt=item[:6],border=0)
                #pdf.cell(20, 9,txt=xd[con]+"\n"+item[:6],border=1)
            con +=1
        pdf.ln(row_height)



    #pdf.cell(10,row_height, border=1, ln=1,txt=producto1[0],align='C')
    pdf.output(nombre)
    return nombre

def calcula_clave(json_file):
    return "657897654678654678"

def crear_factura():
    #poner aca logica para crear factura
    pass


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
