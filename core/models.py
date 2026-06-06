from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Vehicle(models.Model):

    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('scooter', 'Scooter'),
        ('bike', 'Bike'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='car')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price_per_day = models.IntegerField(null=True)
    location_name = models.CharField(max_length=500, blank=True, null=True)
    year = models.IntegerField()
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    # ── Helper: average rating ───────────────────────────────────────
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return 0

    def review_count(self):
        return self.reviews.count()


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_images/')

    def __str__(self):
        return f"Image for {self.vehicle.name}"


# ── NEW: Review Model ────────────────────────────────────────────────
class Review(models.Model):
    vehicle  = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reviews')
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating   = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment  = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('vehicle', 'user')   
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} → {self.vehicle.name} ({self.rating}★)"