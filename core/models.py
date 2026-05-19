from django.db import models

# Create your models here.
class Vehicle(models.Model):

    VEHICLE_TYPE_CHOICES = [
        ('car','Car'),
        ('scooter','Scooter'),
        ('bike','Bike'),
    ]

    name = models.CharField( max_length=100 )
    vehicle_type = models.CharField(max_length=100 , choices=VEHICLE_TYPE_CHOICES , default='car')
    year = models.IntegerField()
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Vehicle_Image(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete= models.CASCADE , related_name = 'images')
    image = models.ImageField(upload_to="media/")
