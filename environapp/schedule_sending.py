import schedule
import time
import os
from twilio.rest import Client
phonenumber = int(input('what is your phone number?(insert +area code)'))
shower = int(input('how long in minutes did you shower today?(please answer within 8:05. results will come then as well.)'))
sink = int(input('how long in minutes did you use the tap? (please answer before 8:10)'))
account_sid = "ACde852f468e8a9bd6d64a68c3aa35ec16"
yourpercentshow = 20/(shower*2.5)
yourpercentsink = 11/(sink*2)
auth_token = "3c9ecac073e105c34fa397ac3b3e254b"
body7 = (shower*2.5+sink*2), "was the amount of water you used total",(yourpercentshow+yourpercentsink)/2,'was the percent of water you used today compared to the average person'
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
           .create(
               body=sink*2,
               from_='+131575622016',
               to_=phonenumber,)
message6 = client.messages \
           .create(
               body=yourpercentsink,
               from_='+131575622016',
               to_=phonenumber,)
message7 = client.messages \
           .create(
body= body7,
from_='+131575622016',
to_=phonenumber
)
def m1():
    print(message1.sid)
def m2():
    print(message2.sid,'gallons were used')
def m3():
    print(message3.sid,"is your percentage compared to the average person for shower water.")
def m4():
    print(message4.sid)
def m5():
    print(message5.sid,"was the gallons of water you used")
def m6():
    print(message6.sid,"was your percentage of water used compared to the average person")
def m7():
    print(message7.sid)

schedule.every().day.at("20:00").do(m1),
schedule.every().day.at("20:05").do(m2),
schedule.every().day.at("20:06").do(m3),
schedule.every().day.at("20:06").do(m4),
schedule.every().day.at("20:10").do(m5),
schedule.every().day.at("20:11").do(m6),
schedule.every().day.at("20:12").do(m7),

