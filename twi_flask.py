from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


GOOD_BOY_URL = "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"


@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    response = MessagingResponse()
    print(response)
    num_media = int(request.values.get("NumMedia"))
    if not num_media:
        msg = response.message("habla pe, enviame una imagen cualquiera")
    else:
        msg = response.message("msjknvjkvmksf")
        msg.media(GOOD_BOY_URL)
    return str(response)


if __name__ == "__main__":
    app.run()
