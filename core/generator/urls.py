from django.urls import path
from . import views


urlpatterns = [
    path('', views.generate_resume, name='generate_resume'),
    path('generate-resume-pdf/',views.download_resume_as_pdf, name='generate_resume_pdf'),
]