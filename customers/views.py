from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('home')
        else:
            return redirect('signup')
    else:
        form = UserRegistrationForm()
        return render(request, 'customers/signup.html', {'form': form})
