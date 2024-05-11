from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_resume, name='generate_resume'),
    
]