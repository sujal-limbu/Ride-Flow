from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import Vehicle
from datetime import datetime
import hmac
import hashlib
import base64
import uuid

@login_required
def payments(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)

    if request.method == 'POST':
        # Extract all form data
        start_date_str  = request.POST.get('start_date')
        end_date_str    = request.POST.get('end_date')
        total_price     = request.POST.get('total_price')
        num_days        = request.POST.get('num_days')
        vehicle_image   = request.POST.get('vehicle_image')

        # Parse dates
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date   = datetime.strptime(end_date_str,   '%Y-%m-%d').date()

        # Generate unique transaction ID
        transaction_uuid = str(uuid.uuid4())

        # Generate eSewa HMAC-SHA256 signature
        secret_key = "8gBm/:&EnhH.1/q"  # test key — replace with live key in production
        message = f"total_amount={total_price},transaction_uuid={transaction_uuid},product_code=EPAYTEST"
        signature = base64.b64encode(
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
        }

        return render(request, 'payments.html', context)

    return redirect('vehicle_list')