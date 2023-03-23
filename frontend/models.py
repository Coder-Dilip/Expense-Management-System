from django.db import models

from django.contrib.auth.models import User

class School(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="new")
    # security_question="first word of the school if you want to rename your school",security_answer=answer)
    security_question=models.CharField(max_length=200,default="first word of the school if you want to rename your school")
    security_answer=models.CharField(max_length=100,default="not available")

