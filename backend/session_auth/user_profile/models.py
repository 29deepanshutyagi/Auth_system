from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255,default='')
    last_name=models.CharField(max_length=255,default='')
    phone=models.CharField(max_length=255,default='')
    city=models.CharField(max_length=255,default='')
    def __str__(self) -> str:
        return self.first_name
    