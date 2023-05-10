from django.db import models

from django.contrib.auth.models import User

class Notification(models.Model):
    school_username = models.CharField(max_length=100)
    message=models.CharField(max_length=200)
    redirect_url=models.CharField(max_length=100)



