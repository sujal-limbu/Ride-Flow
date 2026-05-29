from django.db import models
from django.conf import settings
from core.models import Vehicle

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicle          = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date       = models.DateField()
    end_date         = models.DateField()
    num_days         = models.IntegerField()
    total_price      = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_code = models.CharField(max_length=100, blank=True)
    transaction_uuid = models.CharField(max_length=100, unique=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.name} ({self.status})"