from django.shortcuts import render, redirect
from accounting.forms import DistrictIncomeForm, DistrictExpenseForm
from  accounting.models import *
from accounts.models import *
from accounts.utils import getGlobalContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required
def district_income(request):
    context = getGlobalContext(request.user)
    active_week = context.get('active_week')
    associated_district = context.get('associated_district')
    active_quarter = context.get('active_quarter')
    active_week_month = active_week.month if active_week else None

    # Load all incomes for the active week and associated church
    incomes_for_active_week = DistrictIncome.objects.filter(sabbath_week=active_week, district=associated_district)

    if request.method == "POST":
        form = DistrictIncomeForm(request.POST)

        # Set the sabbath and church fields before saving the form
        if active_week:
            form.instance.sabbath_week = active_week
        if associated_district:
            form.instance.district = associated_district

        if form.is_valid():
            print(form)
            form.save()
            messages.success(request, 'Church income added successfully')
            return redirect('district:district_income')
        else:
            messages.error(request, 'Unable to add income')
            return redirect('district:district_income')
    else:
        form = DistrictIncomeForm()

    context.update({
        'form': form,
        'incomes_for_active_week': incomes_for_active_week,
        'associated_district':associated_district,
        'active_week_month': active_week_month,
        'active_quarter': active_quarter,
    })
    return render(request, 'district/district_income.html', context)



@login_required
def district_expense(request):
    context = getGlobalContext(request.user)
    active_week = context.get('active_week')
    associated_district = context.get('associated_district')
    active_quarter = context.get('active_quarter')
    active_week_month = active_week.month if active_week else None


    # Load current church expenses for the active week and associated church
    current_expenses = DistrictExpense.objects.filter(sabbath_week=active_week, district=associated_district)

    if request.method == "POST":
        form = DistrictExpenseForm(request.POST)

        # Set the Sabbath and church fields before saving the form
        if active_week:
            form.instance.sabbath_week = active_week
        if associated_district:
            form.instance.district = associated_district

        if form.is_valid():
            form.save()
            messages.success(request,'District expense added successfully')
            return redirect('district:district_expense') 
        else:
            messages.error(request,'Unable to add Expense')
            return redirect('district:district_expense') 

    else:
        form = DistrictExpenseForm()

    context.update({
        'form': form,
        'current_expenses': current_expenses,
        'associated-district':associated_district,
        'active_week_month':active_week_month,
        'active_quarter': active_quarter,
    })

    return render(request, 'district/district_expense.html', context)

