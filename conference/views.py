from django.shortcuts import render, redirect
from accounting.forms import DistrictIncomeForm, DistrictExpenseForm
from  accounting.models import *
from accounts.models import *
from accounts.utils import getGlobalContext
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def take_action(request):
     if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
       
        context.update({
            'conference':conference,
            'active_week':active_week,
            'active_quarter':active_quarter,
           
        })
        return render(request,'conference/take_actions.html',context)