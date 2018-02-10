from twilio.rest import Client
from flask import Flask, request
from twilio import twiml




class Twilio:

    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def send_sms(self, to, message):
        self.client.api.account.messages.create(
            to=f'+{to}',
            from_="+17865202738",
            body=message)

    app = Flask(__name__)

    @app.route("/sms", methods=['GET', 'POST'])

    def receive_sms():
        number=request.form['From']
        body=request.form['Body']
        resp = twiml.Response()
        resp.message(f'{number} said {body}')
        return str(resp)



    if __name__ == "__main__":
        app.run(host='192.168.0.102', port=8080, debug=True)


