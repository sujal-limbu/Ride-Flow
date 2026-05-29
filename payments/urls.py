from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/',  views.payments,        name='payments'),
    path('success/',   views.payment_success, name='payment_success'),
    path('failure/',   views.payment_failure, name='payment_failure'),
    path('my-bookings/', views.my_bookings,   name='my_bookings'),
]