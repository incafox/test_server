import smtplib, ssl
from email.mime.text import MIMEText
from email.header import Header

def send_email(portx,filenamex, passwordx,sx,rx, smtpserver):
    print("port "+portx)
    print("filename "+portx)
    print("password "+passwordx)
    print("sender "+sx)
    print("receiver "+rx)
    print("smtp server "+smtpserver)
    #port = 587  # For SSL
    port = portx  # For SSL
    #password = "*Macafri2019"
    password = passwordx
    message2 = """\
            Subject:
            Factura."""
    #sender_email = "facturacion@macafri.com"  # Enter your address
    sender_email = sx  # Enter your address
    #receiver_email = "lubeck05@gmail.com"  # Enter receiver address
    receiver_email = rx  # Enter receiver address
    # context = ssl.create_default_context()
    #message = MIMEText("factura electronica","plain","utf-8")
    message = MIMEMultipart()
    message['From'] =sender_email
    message['To'] = receiver_email
    message['Subject'] =Header("from google","utf-8").encode()
    message.attach(MIMEText(open(filename).read()))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    #with smtplib.SMTP("smtp.zoho.com", port) as server:
    with smtplib.SMTP(smtpserver, port) as server:
        server.starttls(context=context)
        #server.login("facturacion@macafri.com", password)
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message.as_string())


