from django.db import models

from django.contrib.auth.models import User

class School(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="new")
