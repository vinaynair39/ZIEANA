from twilio.rest import Client


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

