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
    
#renting home model
class RentingHome(models.Model):
    start_date=models.DateTimeField( auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(auto_now=False, auto_now_add=False)
    u=models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f"Renting starts on {self.start_date} and ends on {self.end_date}"