import schedule
import time
import os
from twilio.rest import Client
phonenumber = int(input('what is your phone number?(insert +area code)'))
shower = int(input('how long in minutes did you shower today?(please answer within 8:05. results will come then as well.)'))
sink = int(input('how long in minutes did you use the tap? (please answer before 8:10)')
account_sid = "ACde852f468e8a9bd6d64a68c3aa35ec16"
yourpercentshow = 20/(shower*1.5)
yourpercentsink = 11/(sink*2)
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
                  body=yourpercentshow,
                  from_='+13157562206',
                  to_=phonenumber,      
                   )
message4 = client.messages \
           .create(
                body=sink,
                from_='+13157562206',
                to_=phonenumber,
)
message5 = client.messages \
           body=sink*2,
           from_='+131575622016',
           to_=phonenumber,)
message6 = client.messages \
           body=yourpercentsink,
           from_='+131575622016',
           to_=phonenumber,)
schedule.every().day.at("20:00").do(print(message1.sid)),
schedule.every().day.at("20:05").do(print(message2.sid,"gallons were used"))
schedule.every().day.at("20:06").do(print(message3.sid,"is your percentage compared to the average person")
schedule.every().day.at("20:06").do(print(message4.sid)
schedule.every().day.at("20:10").do(print(message5.sid,"was the gallons of water you used")
schedule.every().day.at("20:11").do(print(message6.sid,"was your percentage of water used compared to the average person")
