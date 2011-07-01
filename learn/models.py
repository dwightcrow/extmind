from extmind import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Concept( models.Model ):
    name = models.CharField( max_length=256 )
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    user = models.ForeignKey(User, related_name='concepts')



