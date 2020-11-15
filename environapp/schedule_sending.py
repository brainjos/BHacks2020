import schedule
import time
import os
from twilio.rest import Client
phonenumber = int(input('what is your phone number?(insert +area code)'))
shower = int(input('how long in minutes did you shower today?(please answer within 8:05. results will come then as well.)'))
account_sid = "ACde852f468e8a9bd6d64a68c3aa35ec16"
yourpercent = 20/(shower*1.5)
auth_token = "3c9ecac073e105c34fa397ac3b3e254b"
client = Client(account_sid, auth_token)
message1 = client.messages \
        .create(
            body=shower,
            from_='+13157562206',
            to_=phonenumber,
            )
message2 = client.messages \
             .create(
                 body=shower*1.5,
                 from_='+13157562206',
                 to_=phonenumber,)
message3 = client.messages \
              .create(
                  body=yourpercent,
                  from_='+13157562206',
                  to_=phonenumber      
                   )
schedule.every().day.at("20:00").do(print(message1.sid)),
schedule.every().day.at("20:05").do(print(message2.sid,"gallons were used"))
schedule.every().day.at("20:06").do(print(message3.sid,"is your percentage compared to the average person")
