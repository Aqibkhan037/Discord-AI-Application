from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__ (self): 
        return self.name
    
class Rooms(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic =  models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    # participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name  
    

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) # so if user get's deleted the messages should also be deleted.  
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE )# when the parent is deleted, delete the childre,
    # So if the room get's deleted also delete the messages.
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body[0:50]

