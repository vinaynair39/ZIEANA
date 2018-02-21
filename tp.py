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

    phone_log = {
        'mum': "919819585343",
        'dad': "917977155639",
        'Pranav': "917506105179",
        'Vinay': "917715001084",
    }

    def place_Call(self, to):
        calls = self.client.calls.create(
            to=f'{to}',
            from_="+17865202738",
            url="http://demo.twilio.com/docs/voice.xml"

        )
        print(calls.sid)




if __name__ == "__main__":
    obj = Twilio('AC54ae2752e1452a934167476156168571', '7264a522752fc9da26cee19bc7eb066d')
    obj.place_Call("917715001084")