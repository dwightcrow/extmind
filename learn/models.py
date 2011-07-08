from extmind import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Concept( models.Model ):
    name = models.CharField( max_length=256 )
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    user = models.ForeignKey(User, related_name='concepts')
    
    def __unicode__(self):
        return self.name + " : " + self.user.username

class Goal( models.Model ):
    # Data constraints
    DAYS_OF_WEEK = (("MONDAY", "Monday"),("TUESDAY", "Tuesday"), ("WEDNESDAY", "Wednesday"),
                 ("THURSDAY", "Thursday"), ("FRIDAY", "Friday"), ("SATURDAY", "Saturday"),
                 ("SUNDAY", "Sunday"))
    LENGTH = ((0, "---"), (15, "15 Minutes"), (30, "30 Minutes"), (60, "1 Hour") )
    # Actual fields
    day = models.CharField(max_length=64, choices=DAYS_OF_WEEK )
    length = models.CharField( max_length=32,choices=LENGTH )
    user = models.ForeignKey(User, related_name='goals')

    def __unicode__(self):
        return self.user.username+":"+self.day.capitalize()+":"+self.length
    
class Session( models.Model ):
    user = models.ForeignKey(User, related_name='sessions')
    date = models.DateTimeField(auto_now_add=True)
    length = models.IntegerField()
    
    def __unicode__(self):
        return self.user.username+":"+self.date+":"+self.length