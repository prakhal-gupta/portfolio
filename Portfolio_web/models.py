from django.db import models
from .models import *

class Customer_Message(models.Model):
    name_c                = models.TextField(max_length=100,null=True)
    mobile_c              = models.CharField(max_length=50,null=True)
    email_c               = models.EmailField(max_length=100)
    subject_c             = models.CharField(max_length=100,null=True)
    message_c             = models.TextField(null=True)
    response_a            = models.TextField(null=True)      
    Timestamp             = models.DateTimeField(auto_now=True)

        
