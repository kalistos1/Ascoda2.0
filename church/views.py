
from accounts.utils import getGlobalContext
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from accounts.models import *
from accounts.forms import *
from accounting.forms import *
from accounting.models import BalanceBroughtForward
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from urllib import request
from django.db.models import Count, Sum, Q, F
from datetime import datetime
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse




 # member CRUD starts  ========================================================================
@login_required
def add_new_member(request):
    context = getGlobalContext(request.user)
    church_members = Member.objects.all()
    active_week= context.get('active_week')
    
    active_week_month = active_week.month if active_week else None
    associated_church  = context.get('associated_church')

    # Updated code to get members associated with the church
    if context.get('associated_church'):
        associated_members = Member.objects.filter(church=context['associated_church'])
    else:
        associated_members = None

    if request.method == "POST":
        form = AddMemberForm(request.POST)
        if form.is_valid():
            new_member = form.save()
            messages.success(request, 'New Member added successfully')
            context.update({
                
                'form': AddMemberForm(),  # Resetting the form after successful submission
                'church_members': church_members,
                'associated_members': associated_members,
                'active_week':active_week.sabbath_alias,
                'active_week_month':active_week_month,
                'church_name':associated_church,
                'district': associated_church.district,
            })
            return redirect('church:add_new_member')
        else:
            messages.error(request, 'Unable to add New Member')
            context.update({
                'error': form.errors,
                'form': form,
                'church_members': church_members,
                'associated_members': associated_members,
                'active_week':active_week.sabbath_alias,
            })
            return redirect('church:add_new_member')
    else:
        form = AddMemberForm()
        form1 = UploadMembersForm()
        context.update({
            'form1':form1,
            'church_members': church_members,
            'form': form,
            'associated_members': associated_members,
            'active_week':active_week.sabbath_alias,
            'church_name':associated_church,
            'district': associated_church.district,
            'active_week_month':active_week_month,
            'associated_members_number': associated_members.count(),
            
        })

    return render(request, 'church/add_member.html', context) 
    
    
@login_required
def view_member(request, pk):
    context = getGlobalContext(request.user)
    member = Member.objects.get(pk=pk)
    context.update({
        'member':member,    
    })
    return render(request, "backend/users/parent-details.html", context)
    
    
    
@login_required
def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    context = getGlobalContext(request.user)   
    member.delete()
    messages.success(request, f'{member.member_name} deleted successfully' )
    return redirect("church:add_new_member")
    
# Member CRUD Ends ===========================================================================


# Tithe And Offering CRUD Starts ==============================================================    

@login_required
def add_tithe_offering(request, member_id):
    context = getGlobalContext(request.user)
    active_week = context.get('active_week')
    associated_church = context.get('associated_church')
    
    active_week_month = active_week.month if active_week else None
    # Get the specific church member based on member_id
    church_member = get_object_or_404(Member, member_id=member_id) 

    if request.method == "POST":
        # Set the sabbath_week and church_member fields before saving the form
        form = TitheOfferingForm(request.POST)
        if active_week:
            form.instance.sabbath_week = active_week
        if church_member:
            form.instance.church_member = church_member

        # Try to get an existing TitheOffering for the specified week and member
        try:
            tithe_offering = TitheOffering.objects.get(
                sabbath_week=active_week,
                church_member=church_member
            )
        except TitheOffering.DoesNotExist:
            tithe_offering = None

        # If an existing record is found, update it; otherwise, create a new one
        if tithe_offering:
            form.instance = tithe_offering  # Update the existing instance
            form.save()
            messages.success(request, f' {church_member}\'s Tithe and Offering for the week was added successfully')
            return redirect('church:tithe_offering')
        
        else:
            form.save()
            messages.success(request, f' {church_member}\'s Tithe and Offering for the week was added successfully')
            context.update({
              
                'member_id':member_id,
                'church_member':church_member
            })
            return redirect('church:tithe_offering')
        
    form = TitheOfferingForm()
    form1 = UploadTitheOfferingForm()

    context.update({
            'form':form,
            'form1': form1,
            'member_id':member_id,
            'church_member':church_member,
            'church_name':associated_church,
            'district':associated_church.district,
            'active_week':active_week,
            'active_week_month':active_week_month,
            })
      
    return render(request, 'church/add_user_tithe.html',context)
    


@login_required
def tithe_offering(request):
    context = getGlobalContext(request.user)
    church_members = Member.objects.all()
    associated_church = context.get('associated_church')
    active_week = context.get('active_week')
    active_week_month = active_week.month if active_week else None

    # Updated code to get members associated with the church
    if context.get('associated_church'):
        associated_members = Member.objects.filter(church=context['associated_church'])
    else:
        associated_members = None

    tithe_offering_details = []

    if context.get('active_week'):
        # Get TitheOffering details for each associated member for the active week
        for member in associated_members:
            tithe_offering, created = TitheOffering.objects.get_or_create(
                sabbath_week=context['active_week'],
                church_member=member
            )
            tithe_offering_details.append({
                'member': member,
                'tithe_offering': tithe_offering,
            })

    # Use only the TitheOfferingForm for rendering
    form = TitheOfferingForm()
    form1 = UploadTitheOfferingForm()

    context.update({
        'church_members': church_members,
        'form': form,
        'form1': form1,
        'associated_members': associated_members,
        'tithe_offering_details': tithe_offering_details,
        'church_name':associated_church,
        'district':associated_church.district,
        'active_week':active_week,
        'active_week_month':active_week_month,
    })

    return render(request, 'church/add_tithe_and_offering.html', context)


@login_required
def delete_tithe_offering(request, pk):
    tithe_offering = get_object_or_404(TitheOffering, pk=pk)
    tithe_offering.delete()
    messages.success(request, f't')
    return redirect('your_app:tithe_offering_list')  # Replace 'your_app' with your actual app name


@login_required
def add_church_income(request):
    context = getGlobalContext(request.user)
    active_week = context.get('active_week')
    associated_church = context.get('associated_church')
    active_week_month = active_week.month if active_week else None

    # Load all incomes for the active week and associated church
    incomes_for_active_week = ChurchIncome.objects.filter(sabbath=active_week, church=associated_church)

    if request.method == "POST":
        form = ChurchIncomeForm(request.POST)

        # Set the sabbath and church fields before saving the form
        if active_week:
            form.instance.sabbath = active_week
        if associated_church:
            form.instance.church = associated_church

        # Assign zero values to tithe, offering, and project
        tithe_transaction = WeeklyTransaction.objects.filter(sabbath_week=active_week).first()
        offering_transaction = WeeklyTransaction.objects.filter(sabbath_week=active_week).first()
        project_transaction = WeeklyTransaction.objects.filter(sabbath_week=active_week).first()

        form.instance.tithe = tithe_transaction.tithe_sum if tithe_transaction else None
        form.instance.offering = offering_transaction.offering_sum if offering_transaction else None
        form.instance.project = project_transaction.project_sum if project_transaction else None

        if form.is_valid():
            form.save()

            messages.success(request,'Income Added successfully')
            return redirect('church:church_income')
        else:
            messages.error(request,'Unable to Add income')
    else:
        form = ChurchIncomeForm()

    context.update({
        'form': form,
        'church_name':associated_church,
        'district':associated_church.district,
        'incomes_for_active_week': incomes_for_active_week,
        'church_name':associated_church,
        'active_week_month':active_week_month,
    })
    return render(request, 'church/church_income.html', context)



# @login_required
# @transaction.atomic
# def calculate_weekly_transaction(request):
#     context = getGlobalContext(request.user)
#     active_week = context.get('active_week')
#     active_week_month = active_week.month if active_week else None
#     associated_church = context.get('associated_church')

#     if active_week:
#         churches = Church.objects.all()  

#         for church in churches:
#             # Calculate the sum of tithe, offering, and project for the active week
#             tithe_sum = TitheOffering.objects.filter(
#                 sabbath_week=active_week,
#                 church_member__church=church
#             ).aggregate(tithe_sum=Sum('tithe'))['tithe_sum'] or 0

#             offering_sum = TitheOffering.objects.filter(
#                 sabbath_week=active_week,
#                 church_member__church=church
#             ).aggregate(offering_sum=Sum('offering'))['offering_sum'] or 0

#             project_sum = TitheOffering.objects.filter(
#                 sabbath_week=active_week,
#                 church_member__church=church
#             ).aggregate(project_sum=Sum('project'))['project_sum'] or 0

#             # Create or update the WeeklyTransaction entry
#             weekly_transaction, created = WeeklyTransaction.objects.update_or_create(
#                 sabbath_week=active_week,
#                 church=church,
#                 defaults={
#                     'tithe_sum': tithe_sum,
#                     'offering_sum': offering_sum,
#                     'project_sum': project_sum,
#                 }
#             )

#         context.update({
#             'message': 'Weekly transaction calculated successfully',
#         })

#         # Call create_weekly_income view
#         create_weekly_income(request)
        
#         return redirect('church:your_success_url')  # Replace 'your_success_url' with the appropriate URL
#     else:
#         context.update({
#             'error': 'Active week not set',
#         })

#     return redirect('church:your_error_url')  



@login_required
@transaction.atomic
def create_weekly_income(request):
    context = getGlobalContext(request.user)
    active_week = context.get('active_week')

    if active_week:
        churches = Church.objects.all()  # Replace YourChurchModel with the actual model for your churches

        for church in churches:
            # Get the WeeklyTransaction data for the active week
            weekly_transaction = WeeklyTransaction.objects.filter(
                sabbath_week=active_week,
                church=church
            ).first()

            if weekly_transaction:
                # Create ChurchIncome entry
                ChurchIncome.objects.create(
                    sabbath=active_week,
                    tithe=weekly_transaction.tithe_sum,
                    offering=weekly_transaction.offering_sum,
                    project=weekly_transaction.project_sum,
                    comment='tithe offering weekly income',
                    income_type='T_O_P',
                    payment_method='others',
                    amount=0
                )

        context.update({
            'message': 'Weekly income records created successfully',
        })
    else:
        context.update({
            'error': 'Active week not set',
        })

    return redirect('church:your_success_url') 



login_required
def church_expense(request):
    context = getGlobalContext(request.user)
    active_week = context.get('active_week')
    associated_church = context.get('associated_church')
    active_week_month = active_week.month if active_week else None
    

    # Load current church expenses for the active week and associated church
    current_expenses = ChurchExpense.objects.filter(sabbath=active_week, church=associated_church)

    if request.method == "POST":
        form = ChurchExpenseForm(request.POST)

        # Set the Sabbath and church fields before saving the form
        if active_week:
            form.instance.sabbath = active_week
        if associated_church:
            form.instance.church = associated_church

        if form.is_valid():
            form.save()
            messages.success(request, 'expense was added successfully')
            return redirect('church:church_expenses')  # Replace 'your_success_url' with the appropriate URL
        else:
            messages.error(request, 'Unable to add expense')
            return redirect('church:church_expenses')  # Replace 'your_error_url' with the appropriate URL

    else:
        form = ChurchExpenseForm()

    context.update({
        'form': form,
        'current_expenses': current_expenses,
        'church_name':associated_church,
        'active_week_month':active_week_month,
        'district':associated_church.district,
    })

    return render(request, 'church/church_expense.html', context)


@login_required
def church_cash_account(request):
    context = getGlobalContext(request.user)
    active_week = context.get('active_week')
    associated_church = context.get('associated_church')
    active_sabbath = Sabbath.objects.filter(is_active=True).first()
    active_quarter = context.get('active_quarter')
    active_week_month = active_week.month if active_week else None


    # Load current Church Cash Account records for the active week and associated church
    current_cash_accounts = ChurchCashAccount.objects.filter(sabbath_week=active_week, church=associated_church, sabbath_week__month__quarter = active_quarter)

    if request.method == "POST":
        form = ChurchCashAccountForm(request.POST)

        # Set the Sabbath and church fields before saving the form
        if active_week:
            form.instance.sabbath_week = active_week
        if associated_church:
            form.instance.church = associated_church

        if form.is_valid():
            form.save()
            messages.success(request, 'cash transaction addd successfully')
            return redirect('church:cash_account')  # Replace 'your_success_url' with the appropriate URL
        else:
            messages.error(request, 'Unable to add cash transactions')
            return redirect('church:cash_account')  # Replace 'your_error_url' with the appropriate URL

    else:
        form = ChurchCashAccountForm()

    context.update({
        'form': form,
        'current_cash_accounts': current_cash_accounts,
        'church_name':associated_church,
        'district':associated_church.district,
        'active_week_month':active_week_month,
    })

    return render(request, 'church/cash_account.html', context)



@login_required
def update_trust_fund(request):
    try:
        # Ensure that this view can only be accessed by an admin
        if not request.user.is_staff:
            return HttpResponse("Unauthorized", status=403)

        # Fetch the active Sabbath
        active_sabbath = Sabbath.objects.filter(is_active=True).first()

        if not active_sabbath:
            raise Exception('No active Sabbath found')

        # Fetch all active churches
        churches = Church.objects.all()

        with transaction.atomic():
            for church in churches:
                # Fetch the tithe_sum for the active week
                tithe_sum = WeeklyTransaction.objects.filter(
                    sabbath_week=active_sabbath,
                    church=church
                ).aggregate(tithe_sum=Sum('tithe_sum'))['tithe_sum'] or 0

                # Fetch the amount_due_conference for the active week
                combined_offering = CombinedOffering.objects.get(
                    church=church,
                    sabbath_week=active_sabbath
                )
                amount_due_conference = combined_offering.amount_due_conference

                # Create or update the TrustFund entry
                trust_fund, created = TrustFund.objects.update_or_create(
                    church=church,
                    sabbath_week=active_sabbath,
                    defaults={
                        'tithe_amount': tithe_sum,
                        'offering_amount': amount_due_conference,
                    }
                )

                # Calculate and update the total_amount
                trust_fund.total_amount = trust_fund.tithe_amount + trust_fund.offering_amount
                trust_fund.save()

        return HttpResponse("Trust Fund updated successfully")
    except Exception as e:
        return HttpResponse(f"Error updating Trust Fund: {e}", status=500)



@login_required
def view_trust_fund(request):
    # Get the global context for the logged-in user
    global_context = getGlobalContext(request.user)
    active_sabbath = Sabbath.objects.filter(is_active=True).first()
    active_week_month = active_sabbath.month if active_sabbath else None

    # Fetch the associated church from the global context
    associated_church = global_context['associated_church']

    # Fetch the active quarter from the global context
    active_quarter = global_context['active_quarter']

    if not associated_church or not active_quarter:
        # Handle the case where the associated church or active quarter is not found
        return render(request, 'error_template.html', {'error_message': 'Data not found'})

    # Fetch the TrustFund records for the associated church and active quarter
    trust_fund_data = TrustFund.objects.filter(
        church=associated_church,
        sabbath_week__month__quarter=active_quarter
    )

    context = {
        'trust_fund_data': trust_fund_data,
        **global_context  # Include the rest of the global context
    }

    return render(request, 'church/trust_fund.html', context)
  




@login_required
def calculate_combined_offering(request):
    # Get the global context using your function
    context = getGlobalContext(request.user)
    active_week = context.get('active_week')
    associated_church = context.get('associated_church')

    # Check if the user has a valid associated church
    if not associated_church:
       messages.error(request, "Unable to calculate combined offering")
       return redirect('dashboard:church_dashboard')
    
    # Get the active Sabbath
    active_sabbath = active_week #context.get('active_sabbath')

    # Get all TitheOffering entries for the associated church and active Sabbath
    tithe_offerings = TitheOffering.objects.filter(
        church_member__church=associated_church,
        sabbath_week=active_sabbath
    )

    # Calculate combined offering from TitheOffering
    combined_offering_amount = tithe_offerings.aggregate(
        combined_offering=Sum('offering')
    )['combined_offering'] or 0
  
    # Fetch amounts of specific income types from ChurchIncome
    specific_income_types = ['APPRECIATION', 'LOOSE_OFFERING', 'CHILD_DEDICATION', 'THANKS_OFFERING', 'SABBATH_SCHOOL_EXPENSE_OFFERING']
    specific_income_amount = ChurchIncome.objects.filter(
        church=associated_church,
        sabbath=active_sabbath,
        income_type__in=specific_income_types
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    
   
    # Add specific income amount to combined offering amount
    combined_offering_amount += specific_income_amount

    # Create or update the CombinedOffering entry
    combined_offering_entry, created = CombinedOffering.objects.update_or_create(
        associated_church=associated_church,
        sabbath_week=active_sabbath,
        defaults={
            'combined_offering': combined_offering_amount,
            'amount_due_district': float(combined_offering_amount) * 0.10,
            'amount_due_church': float(combined_offering_amount) * 0.50,
            'amount_due_conference': float(combined_offering_amount) * 0.40,
            'total_available_income': combined_offering_amount,
        }
    )
    
    messages.success(request, "combined offering calculated and updated  successfully")
    return redirect('dashboard:church_dashboard')
    


@login_required
@transaction.atomic
def update_weekly_trustfund():
    pass
    


"""
@transaction.atomic
def calculate_weekly_totals(request):
    try:
        # Fetch all active churches
        churches = Church.objects.all()

        # Fetch the active Sabbath
        active_sabbath = Sabbath.objects.filter(is_active=True).first()

        if not active_sabbath:
            raise Exception('No active Sabbath found')

        # Iterate through each church
        for church in churches:
            # Fetch TitheOffering entries for the specified church and active Sabbath
            tithe_offering_entries = TitheOffering.objects.filter(
                sabbath_week=active_sabbath,
                church_member__church=church
            )

            # Calculate tithe, offering, and project sums
            tithe_sum = sum(entry.tithe for entry in tithe_offering_entries)
            offering_sum = sum(entry.offering for entry in tithe_offering_entries)
            project_sum = sum(entry.project for entry in tithe_offering_entries)

            # Create or update the WeeklyTransaction entry
            weekly_transaction, created = WeeklyTransaction.objects.update_or_create(
                sabbath_week=active_sabbath,
                church=church,
                defaults={
                    'tithe_sum': tithe_sum,
                    'offering_sum': offering_sum,
                    'project_sum': project_sum,
                }
            )

        messages.success(request, 'Weekly totals updated successfully')
    except Exception as e:
        messages.error(request, f'Error updating weekly totals: {e}')

    return redirect('your_template')

"""

# @login_required
# @transaction.atomic
# def calculate_combined_offering(request):
#     try:
#         # Fetch all active churches
#         churches = Church.objects.all()

#         # Fetch the active Sabbath
#         active_sabbath = Sabbath.objects.filter(is_active=True).first()

#         if not active_sabbath:
#             raise Exception('No active Sabbath found')

#         # Iterate through each church
#         for church in churches:
#             # Fetch ChurchIncome entries for the specified church and active Sabbath
#             church_income_entries = ChurchIncome.objects.filter(
#                 sabbath=active_sabbath,
#                 church=church,
#                 income_type__in=['APPRECIATION', 'LOOSE_OFFERING', 'CHILD_DEDICATION', 'THANKS_OFFERING', 'SABBATH_SCHOOL_EXPENSE_OFFERING']
#             )

#             # Call the class method to calculate combined offering and amounts due
#             combined_offering_entry, created = CombinedOffering.calculate_combined_offering(church_income_entries, church)

#             # Call the method to update total_available_income
#             combined_offering_entry.update_total_available_income()

#         messages.success(request, 'Combined offerings calculated and stored successfully')
#     except Exception as e:
#         messages.error(request, f'Error calculating combined offerings: {e}')

#     return redirect('conference:take_action')