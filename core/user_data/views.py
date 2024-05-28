from django.shortcuts import render, redirect
from .forms import UserDataForm

def home(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('generate_resume')  # Redirect to a success page
    else:
        form = UserDataForm()
    
    return render(request, 'user_data/index_form.html', {'form': form})