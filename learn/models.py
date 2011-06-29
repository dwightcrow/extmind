from django.db import models

# Create your models here.

class Concept( models.Model ):
    name = models.CharField( max_lenght=256 )
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    user = models.ForeignKey(User, related_name='concepts')

