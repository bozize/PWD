from django.urls import path
from . import views
from .views import upload_violation

urlpatterns = [
    path('process-violation/', views.process_violation, name='process_violation'),
    path('pwd/<str:mac_address>/', views.get_pwd_by_mac, name='get_pwd_by_mac'),  # Updated to use mac_address
    path('upload-violation/', upload_violation, name='upload_violation'),
]
