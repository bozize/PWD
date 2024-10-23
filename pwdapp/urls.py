from django.urls import path
from . import views


urlpatterns = [
    path('process-violation/', views.process_violation, name='process_violation'),
    path('pwd/<str:mac_address>/', views.get_pwd_by_mac, name='get_pwd_by_mac'),  # Updated to use mac_address
]
