from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import Vehicle
from payments.models import Booking
from datetime import datetime
import hmac
import hashlib
import base64
import uuid
import json

@login_required
def payments(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str   = request.POST.get('end_date')
        total_price    = request.POST.get('total_price')
        num_days       = request.POST.get('num_days')
        vehicle_image  = request.POST.get('vehicle_image')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date   = datetime.strptime(end_date_str,   '%Y-%m-%d').date()

        transaction_uuid = str(uuid.uuid4())

        
        Booking.objects.create(
            user             = request.user,
            vehicle          = vehicle,
            start_date       = start_date,
            end_date         = end_date,
            num_days         = num_days,
            total_price      = total_price,
            transaction_uuid = transaction_uuid,
            status           = 'pending',
        )

        secret_key = "8gBm/:&EnhH.1/q"
        message    = f"total_amount={total_price},transaction_uuid={transaction_uuid},product_code=EPAYTEST"
        signature  = base64.b64encode(
            hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
        ).decode()

        context = {
            'vehicle':          vehicle,
            'start_date':       start_date,
            'end_date':         end_date,
            'total_price':      total_price,
            'num_days':         num_days,
            'vehicle_image':    vehicle_image,
            'transaction_uuid': transaction_uuid,
            'signature':        signature,
            'product_code':     'EPAYTEST',
            'success_url':      request.build_absolute_uri('/payments/success/'),
            'failure_url':      request.build_absolute_uri('/payments/failure/'),
        }

        return render(request, 'payments.html', context)

    return redirect('vehicle_list')


@login_required
def payment_success(request):
    data = request.GET.get('data', '')
    try:
        decoded    = base64.b64decode(data).decode('utf-8')
        esewa_data = json.loads(decoded)

        # Verify eSewa response signature
        secret_key    = "8gBm/:&EnhH.1/q"
        signed_fields = esewa_data.get('signed_field_names', '').split(',')
        message       = ','.join(
            f"{field}={esewa_data[field]}"
            for field in signed_fields
            if field != 'signature'
        )
        expected_sig = base64.b64encode(
            hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
        ).decode()

        if expected_sig != esewa_data.get('signature'):
            return render(request, 'payment_failure.html', {'error': 'Invalid signature'})

        # Mark booking confirmed
        transaction_uuid = esewa_data.get('transaction_uuid')
        transaction_code = esewa_data.get('transaction_code')

        booking                  = Booking.objects.get(transaction_uuid=transaction_uuid)
        booking.status           = 'confirmed'
        booking.transaction_code = transaction_code

        booking.save()

        vehicle = booking.vehicle
        vehicle.is_available = False
        vehicle.save()

        context = {
            'booking':          booking,
            'transaction_code': transaction_code,
            'total_amount':     esewa_data.get('total_amount'),
        }
        return render(request, 'payment_success.html', context)

    except Booking.DoesNotExist:
        return render(request, 'payment_failure.html', {'error': 'Booking not found'})
    except Exception as e:
        return render(request, 'payment_failure.html', {'error': str(e)})


@login_required
def payment_failure(request):
    return render(request, 'payment_failure.html')


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user   = request.user,
        status = 'confirmed'
    ).order_by('-created_at')
    return render(request, 'my_bookings.html', {'bookings': bookings})