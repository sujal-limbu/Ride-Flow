from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
    
class DashBoard(models.Model):
    # Standard ForeignKey linking each dashboard to a CustomUser
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Uploads will go to MEDIA_ROOT/dashboards/
    image = models.ImageField(upload_to='dashboards/')

    def __str__(self):
        return f"Dashboard of {self.user.username}"