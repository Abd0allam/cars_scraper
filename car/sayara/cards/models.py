from django.db import models

class UsedCars(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField()  
    odo = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    

class NewdCars(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField()

    def __str__(self):
        return self.name