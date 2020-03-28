from flask import Flask
from flask_mail import Mail,Message

app = Flask(__name__)

#app.config['MAIL_SERVER']= 'mail.prettyprinted.com'
#app.config['MAIL_PORT']=465

mail = Mail(app)

@app.route('/')
def index():
    msg = Message('hello', sender='anthony@prettyprinted.com', recipients=['lubeck05@gmail.com'])
    mail.send(msg)
    return 'Messae SENT!'

if __name__ == '__main__':
    app.run(debug=True)
