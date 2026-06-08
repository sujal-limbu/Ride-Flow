from django.urls import path
from . import views

urlpatterns = [
    path( 'register/', views.register_view , name = 'register' ),
    path( 'login/', views.login_view , name = 'login' ),
    path( 'index/', views.logout_view , name = 'logout' ),
    path('dashboard/' , views.dashboard_info , name = 'dashboard' ),
    path('dashboard/delete/<int:pk>/', views.delete_dashboard, name='delete_dashboard'),
]
