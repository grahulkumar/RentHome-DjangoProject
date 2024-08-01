from django.db import models
from user.models import CustomUser

class HomeDetails(models.Model):
    image=models.ImageField(upload_to="house_images/")
    add=models.CharField(max_length=200)
    add1=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.IntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    about=models.CharField(max_length=200)
    condition = models.CharField(max_length=50)
    status = models.CharField(max_length=50,default="not rented")
    people=models.IntegerField(default=1)
    rid= models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.add
