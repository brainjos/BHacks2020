# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "ACa2265e40cf5d0e64787899eff0170023"
auth_token = "b217f03dc0715d6dab5ef35b7200db99"
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+12543263257',
         to='+14259997243'
     )

print(message.sid)