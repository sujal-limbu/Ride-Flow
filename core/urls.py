from django.urls import path
from . import views

urlpatterns = [
    path('' , views.index , name = 'index' ),
    path('vehicle_list/' , views.vehicle_list , name = 'vehicle_list' ),
    path('vehicle_detail/<int:vehicle_id/' , views.vehicle_detail , name = 'vehicle_detail' ),
]
