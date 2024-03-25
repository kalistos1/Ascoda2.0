
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
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from . import utils

def signin(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        # If the user is authenticated, redirect to their dashboard based on their role
        user = request.user
        return redirect(get_dashboard_url(user.role))  # Replace with the actual function to get the dashboard URL

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                # Redirect to the appropriate dashboard based on the user's role
               
                return redirect(get_dashboard_url(user.role))
            else:
                messages.error(request, 'Invalid login details')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = LoginForm()

    return render(request, "pages/signin.html", {'form': form})


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

@login_required
def edit_user_info(request):
    user_context = getGlobalContext(request.user)

    profile =request.user
    form = EditProfileForm(instance=profile)

    context={
        'form':form,
       
    }

    return render(request, 'pages/security.html',context)


@login_required
def change_email(request):
    if request.method =="POST":
        new_email = request.POST.get("new_email")
        old_email = request.POST.get("old_email")
        user = request.user

    try:
        User.objects.get(email=new_email)
        messages.error(request,'User Email already Exists')
        return redirect('authentication:change_email')

    except User.DoesNotExist:
        confirm = User.objects.get(email=old_email)         
        if confirm == request.user:

            user.email = new_email
            user.save()
            messages.success(request,'mail changed successfully!')
            return redirect('dashboard:profile')
            
        else:
            messages.error(request,'unforeseen error while trying tp change user email. try again')
            return redirect('authentication:change_email')



@login_required
def change_password(request):
    if request.method =="POST":

        new_password = request.POST.get("new_password")
        old_password = request.POST.get("old_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user

    if confirm_password != new_password:
        messages.error(request, 'password mismatch (new password and confirm password)')
        return redirect('account:edit_user_info')

    try:
        User.objects.filter(id=user.id).update(password=make_password(new_password))
        messages.success(request, 'password was successfully changed')
        return redirect('account:edit_user_info')
        
    except User.DoesNotExist:
        messages.error(request, ' An unforeseen error occured while attempting to change your password. Please retry')
        return redirect('account:edit_user_info')



@login_required
def update_profile_info(request):
    if request.method =="POST":
        user_context = getGlobalContext(request.user)

        profile =request.user
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'profile was updates successfully')
            return redirect('account:edit_user_info')
        else:
            messages.error(request, 'form was not saved successfully')
            return redirect('account:edit_user_info')
    else:
       profile = request.user
       form = EditProfileForm(instance=profile)
    
       context = {        
        'form':form,
    }   

       return redirect('account:edit_user_info')
