# core/urls.py
from django.urls import path
from . import views
from .views import upload_violation


urlpatterns = [
    path('process-violation/', views.process_violation, name='process_violation'),
    path('pwd/<str:id_number>/', views.get_pwd_by_id, name='get_pwd_by_id'),
    path('upload-violation/', upload_violation, name='upload-violation'),
]