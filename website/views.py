from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from website.forms import SignUpForm
from .models import Record


# Checks for authenticated users
def is_auth(request) -> bool:
    return request.user.is_authenticated


# Create your views here.
def home(request):
    records = Record.objects.all()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate users
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You've been logged in!")
            return redirect('home')
        else:
            messages.error(request, "There was an error logged in, please try again!")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


# logout user
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out....")
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Welcome! You've successfully registered")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


# Get a single customer record
def customer_records(request, pk: int):
    if is_auth(request):
        # Look up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "you must be logged in to view that page")
        return redirect('home')


# Delete a customer record
def delete_record(request, pk: int):
    if is_auth(request):
        deleted = Record.objects.get(id=pk)
        deleted.delete()
        messages.success(request, "Record deleted successfully")
        return redirect('home')
    else:
        messages.error(request, "you must be logged in to perform this action")
        return redirect('home')
