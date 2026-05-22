from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Vehicle,VehicleImage

def index(request):
    return render(request, 'core/home.html')

def profile(request):
    return render(request, 'core/profile.html')

def vehicle_list(request):
    vehicles = Vehicle.objects.prefetch_related('images').all()
    return render(request, 'core/vehicle_list.html', {'vehicles': vehicles})

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        name        = request.POST.get('name')
        vehicle_type = request.POST.get('vehicle_type')
        year        = request.POST.get('year')
        price_per_day = request.POST.get('price_per_day')
        description = request.POST.get('description')
        latitude    = request.POST.get('latitude')
        longitude   = request.POST.get('longitude')

        vehicle = Vehicle.objects.create(
            name=name,
            vehicle_type=vehicle_type,
            year=year,
            price_per_day = price_per_day,
            description=description,
            latitude=latitude,
            longitude=longitude,
        )

        for image in request.FILES.getlist('images'):
            VehicleImage.objects.create(vehicle=vehicle, image=image)


        return redirect('vehicle_list')  
    return render(request, 'core/add_vehicle.html')

def my_bookings(request):
    return render(request , 'core/my_bookings.html')

def vehicle_detail(request , vehicle_id ):
    return render(request , 'core/vehicle_detail.html')