
import smtplib
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
connection = smtplib.SMTP('smtp.zoho.com', 587)
connection.ehlo()
connection.starttls(context=context)
connection.ehlo()
connection.login('facturacion@macafri.com', "*Macafri2019")
connection.sendmail('facturacion@macafri.com', 'lubeck05@gmail.com', "tmr")
