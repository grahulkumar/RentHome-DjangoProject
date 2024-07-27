from django.db import models

class HomeDetails(models.Model):
    image=models.ImageField(upload_to="house_images/")
    add=models.CharField(max_length=200)
    add1=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.IntegerField()
    price=models.FloatField()
    about=models.CharField(max_length=200)
    condition = models.CharField(max_length=50)
    
    def __str__(self):
        return self.add
