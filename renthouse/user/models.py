from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    name= models.CharField(max_length=200,null=False)
    role = models.CharField(max_length=20,default='User')
    email = models.EmailField(unique=True)
    
    username = models.CharField(max_length=150, unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email