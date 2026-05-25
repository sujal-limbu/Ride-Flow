from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index , name = 'index' ),
    path('profile' , views.profile , name = 'profile' ),
    path('vehicle_list/' , views.vehicle_list , name = 'vehicle_list' ),
    path('add_vehicle/' , views.add_vehicle , name = 'add_vehicle' ),
    path('my_bookings/' , views.my_bookings , name = 'my_bookings' ),
    path('vehicle_detail/<int:id>/' , views.vehicle_detail , name = 'vehicle_detail' ),
]
