from django.shortcuts import render

def index(request):
    return render(request, 'core/home.html')

def vehicle_list(request):
    return render(request , 'core/vehicle_list.html')

def vehicle_detail(request , vehicle_id ):
    return render(request , 'core/vehicle_detail.html')