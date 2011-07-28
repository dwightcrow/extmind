'''
created by dwight


like a boss
'''

from extmind.learn.models import *
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import datetime
import smtplib
from email.mime.text import MIMEText
from twilio.rest import TwilioRestClient

daysOfWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                         "Saturday", "Sunday" )
acct_sid='AC57dbdb451899116433c836624a4ea6d9'
acct_token='b7f9a35884ee939d8ee44683ff855bc2'


class Command(BaseCommand):
    # checks if you were supposed to do something today, and emails
    # you if you didn't do anything
    # Setup email
    
    def handle(self, *args, **options):
        # setup email
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login( 'superawesome8888', '8888superawesome')

        # setup twilio
        client = TwilioRestClient( acct_sid, acct_token )
        

        #determine day of week
        today = daysOfWeek[ datetime.date.today().weekday() ].upper()
        for u in User.objects.all():
            print 'looking at u=%s' % u.username
            u_profile = u.profile
            minutesToday = getattr( u_profile, today[:3].lower() + 'Min' )
            if minutesToday == 0:
                continue
            # they have a goal for the day. check if they did anyhting
            now = datetime.datetime.now()
            startOfDay = now - datetime.timedelta(hours=now.hour, minutes=now.minute)
            conceptsToday = Concept.objects.filter(user=u).filter( date__gt=startOfDay).count()
            print 'concepts today for %s is %d' % (u.username, conceptsToday )
            msgBody = 'Hi %s, you didnt do your planned work today (%s). You should!' %  \
                (u.username, today.lower() )
            if conceptsToday == 0:
                if u_profile.emailRemind:
                    print 'Emailing %s at %s' % (u.username, u.email)
                    msg = MIMEText( msgBody )
                    msg['Subject'] = 'Friendly Growth Reminder!'
                    msg['From'] = 'coach@deliberatePractice.com'
                    msg['To'] = u.email
                    mailServer.sendmail( 'Cognify.me', u.email, msg.as_string())
                    print msg
                if u_profile.textRemind:
                    print 'texting %s at # %s' % (u.username, u_profile.phoneNumber)
                    txt = client.sms.messages.create(to=u_profile.phoneNumber,
                                     from_="+16502651713",
                                     body=msgBody )
                if u_profile.phoneRemind:
                    print 'calling %s at # %s' % (u.username, u_profile.phoneNumber)
                    print dir( client )
                    print dir( client.calls )
                    call = client.calls.create(to=u_profile.phoneNumber, from_="+16502651713",
                                             url="http://cognify.me/static/phoneRemind")
                    #print call
                    #print dir( call )
        mailServer.close()



            
            