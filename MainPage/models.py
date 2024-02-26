from django.db import models


class ChatMessage(models.Model):
    input = models.TextField()
    reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_uid = models.CharField(max_length=100)  
    objects = models.Manager() 

