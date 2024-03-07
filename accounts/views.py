
from decimal import Decimal
import pkgutil
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Conference, Church, District, Quarter, Month, Sabbath, User, AssignedOfficer
import random
from django.db.models import Count, Sum, Q, F
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .utils import getGlobalContext
from .forms import LoginForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages


# Create your views here.
def signin(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # If the user is authenticated, redirect to their dashboard based on their role
        user = request.user
        return redirect(get_dashboard_url(user.role))  # Replace with the actual function to get the dashboard URL

    context = {}  # Initialize the context dictionary

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        else:
            context['form_errors'] = form.errors
            user = None

        if user is not None:
            login(request, user)

            # Redirect to the appropriate dashboard based on the user's role
            return redirect(get_dashboard_url(user.role))

        else:
            context['message'] = 'Invalid login details'
            context['form'] = form

    if request.method == 'GET':
        form = LoginForm()
        context = {'form': form, 'name': "hello"}

    return render(request, "pages/signin.html", context)


def get_dashboard_url(user_role):
    # Add logic to determine the dashboard URL based on the user's role
    if user_role == "Admin":
        return 'dashboard:conference_dashboard'
    elif user_role == "District_treasurer" or user_role == "District_secretary":
        return 'dashboard:district_dashboard'
    elif user_role == "Church_treasurer" or user_role == "Church_secretary":
        return 'dashboard:church_dashboard'
    else:
        return 'dashboard:default_dashboard' 
   

@login_required
def signout(request):
   # if request.user.is_authenticated and 'next' in request.GET:
    #    return redirect(request.GET['next'])

    logout(request)
    return redirect('core:index')



def forgot_password(request):
    pass
    
    
    
def recover_password (request):
    pass



def signup_confirm(request):
    pass
    
    

def email_confirm(request):
    pass
    
    
    