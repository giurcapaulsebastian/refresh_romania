from django.contrib.auth import decorators
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

# Create your views here.
from .forms import CreateUserForm
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only

import folium

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account ({}) created succesfully!'.format(username))
                return redirect('login')

        context = {'form':form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect!')

        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def profilePage(request):
    context={}
    return render(request, 'accounts/profile.html', context)

def products(request):
    return render(request, 'accounts/products.html')

def customer(request):
    return render(request, 'accounts/customer.html')

def map(request):
    map1 = folium.Map()
    map1 = map1._repr_html_()
    context={
        'map1':map1
    }
    return render(request, 'accounts/map.html', context)