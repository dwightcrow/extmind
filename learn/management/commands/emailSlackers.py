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

daysOfWeek = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                         "Saturday", "Sunday" )

class Command(BaseCommand):
    # checks if you were supposed to do something today, and emails
    # you if you didn't do anything
    # Setup email
    
    def handle(self, *args, **options):
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login( 'superawesome8888', '8888superawesome')

        #determine day of week
        weekday = daysOfWeek[ datetime.date.today().weekday() ].upper()
        for u in User.objects.all():
            print 'looking at u=%s' % u.username
            numGoalPerDay = Goal.objects.filter( user=u).filter( day=weekday ).count()
            print 'numgoals today for %s is %d' %(u.username, numGoalPerDay)
            if numGoalPerDay == 0:
                continue
            if numGoalPerDay > 1:
                print 'too many goals!!!!!!'
            goal = Goal.objects.filter( user=u).filter( day=weekday ).all()[0]
            if goal.length == 0:
                continue
            # they have a goal for the day. check if they did anyhting
            now = datetime.datetime.now()
            startOfDay = now - datetime.timedelta(hours=now.hour, minutes=now.minute)
            conceptsToday = Concept.objects.filter(user=u).filter( date__gt=startOfDay).count()
            print 'concepts today for %s is %d' % (u.username, conceptsToday )
            if conceptsToday == 0:
                print 'Gonna email %s' % u.username
                msg = MIMEText( '%s, you didnt do your planned work today (%s)' %  (u.username, weekday) )
                msg['Subject'] = 'Do You Want to Be Great or What?!'
                msg['From'] = 'coach@deliberatePractice.com'
                msg['To'] = u.email
                mailServer.sendmail( 'superawesome8888', u.email, msg.as_string())
                print msg
        mailServer.close()



            
            