from django.db import models

class Vehicle(models.Model):

    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('scooter', 'Scooter'),
        ('bike', 'Bike'),
    ]

    name = models.CharField(max_length=100)

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES,
        default='car'
    )

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price_per_day = models.IntegerField(null=True)
    location_name = models.CharField(max_length=500, blank=True, null=True)

    year = models.IntegerField()

    description = models.TextField()

    def __str__(self):
        return self.name


class VehicleImage(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='vehicle_images/')

    def __str__(self):
        return f"Image for {self.vehicle.name}"