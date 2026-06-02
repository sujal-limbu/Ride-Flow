from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vehicle,VehicleImage

def index(request):
    return render(request, 'core/home.html')

def profile(request):
    return render(request, 'core/profile.html')

def vehicle_list(request):
    vehicles = Vehicle.objects.prefetch_related('images').all()
    if request.GET.get('name'):
        vehicles = vehicles.filter(name__icontains=request.GET['name'])

    if request.GET.get('location'):
        vehicles = vehicles.filter(location_name__icontains=request.GET['location'])

    if request.GET.get('min_price'):
        vehicles = vehicles.filter(price_per_day__gte=request.GET['min_price'])

    if request.GET.get('max_price'):
        vehicles = vehicles.filter(price_per_day__lte=request.GET['max_price'])

    return render(request, 'core/vehicle_list.html', {'vehicles': vehicles})

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        name          = request.POST.get('name')
        vehicle_type  = request.POST.get('vehicle_type')
        year          = request.POST.get('year')
        price_per_day = request.POST.get('price_per_day')
        description   = request.POST.get('description')
        latitude      = request.POST.get('latitude')
        longitude     = request.POST.get('longitude')
        location_name = request.POST.get('location_name')

        vehicle = Vehicle.objects.create(
            name=name,
            vehicle_type=vehicle_type,
            year=year,
            price_per_day=price_per_day,
            description=description,
            latitude=latitude,
            longitude=longitude,
            location_name=location_name,
        
        )

        for image in request.FILES.getlist('images'):
            VehicleImage.objects.create(vehicle=vehicle, image=image)

        return redirect('vehicle_list')

    return render(request, 'core/add_vehicle.html')

def my_bookings(request):
    return render(request, 'core/my_bookings.html')


def vehicle_detail(request, id):
    vehicle = get_object_or_404(Vehicle, id = id)
    images  = vehicle.images.all()
    return render(request, 'core/vehicle_detail.html', {
        'vehicle': vehicle,
        'images':  images,
    })