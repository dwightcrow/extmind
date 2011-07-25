from extmind import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


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
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    emailRemind = models.BooleanField( default=False )
    textRemind = models.BooleanField( default=False )
    phoneRemind = models.BooleanField( default=False )
    timeOfRemind = models.TimeField( null=True ) 
    monMin = models.IntegerField( default=0 )
    tueMin = models.IntegerField( default=0 )
    wedMin = models.IntegerField( default=0 )
    thuMin = models.IntegerField( default=0 )
    friMin = models.IntegerField( default=0 )
    satMin = models.IntegerField( default=0 )
    sunMin = models.IntegerField( default=0 )

def create_user_profile(sender, instance, **kwargs):
    if 'created' in kwargs and kwargs['created']:
        profile = UserProfile()
        profile.user = instance
        profile.save()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
post_save.connect(create_user_profile, User, dispatch_uid="app.models")