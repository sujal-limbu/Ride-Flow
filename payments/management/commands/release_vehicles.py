from django.core.management.base import BaseCommand
from django.utils import timezone
from payments.models import Booking

class Command(BaseCommand):
    help = 'Release vehicles whose booking end date has passed'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        expired_bookings = Booking.objects.filter(
            end_date__lte=today,
            status='confirmed',
            vehicle__is_available=False
        )

        for booking in expired_bookings:
            booking.vehicle.is_available = True
            booking.vehicle.save()
            self.stdout.write(f"Released: {booking.vehicle.name}")