from django.shortcuts import render

def index(request):
    return render(request, 'core/home.html')

def profile(request):
    return render(request, 'core/profile.html')

def vehicle_list(request):
    return render(request , 'core/vehicle_list.html')

def add_vehicle(request):
    return render(request , 'core/add_vehicle.html')

def my_bookings(request):
    return render(request , 'core/my_bookings.html')

def vehicle_detail(request , vehicle_id ):
    return render(request , 'core/vehicle_detail.html')