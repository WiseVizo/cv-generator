from django.shortcuts import render

# Create your views here.
def generate_resume(request):
    return render(request, "generator/cv.html")

