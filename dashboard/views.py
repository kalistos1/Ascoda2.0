from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import *
from accounting.models import *
from accounting.forms import *
from accounts.forms import *
from django.contrib.auth.decorators import login_required
from accounts.utils import getGlobalContext
from django.http import HttpResponse
from urllib import request
from django.db.models import Count, Sum, Q, F
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import csv

# Create your views here.


@login_required
def church_dashboard(request):
    user_context = getGlobalContext(request.user)

    # Check if the user is a church secretary or treasurer
    if request.user.role in ['Church_secretary', 'Church_treasurer']:
    
        associated_church = user_context.get('associated_church')
        active_week = user_context.get('active_week')
   
        sabbath_week_start = user_context.get('sabbath_week_start')
        sabbath_week_ends = user_context.get('sabbath_week_ends')
       
       
        active_week_month = active_week.month if active_week else None
       
        if associated_church:
            # Get all information concerning the church
            church_info = {
                'church_name': associated_church,
                'district': associated_church.district,
                'church_address': associated_church.address,
                'church_email': associated_church.email,
                'church_phone': associated_church.phone,
                'church_facebook': associated_church.facebook,
                'active_week':active_week,
                'active_week_month': active_week_month,

            }
            user_context.update(church_info)

            conference_info = user_context.get('conference')
            district_info= user_context.get('associated_district')
            active_quarter_info = user_context.get('active_quarter')

        # Get expenses and income for the district
        church_expenses = ChurchExpense.objects.filter(church=associated_church, sabbath=active_week,sabbath__month__quarter=active_quarter_info)
        church_incomes = ChurchIncome.objects.filter(church=associated_church, sabbath=active_week, sabbath__month__quarter=active_quarter_info)
        cash = ChurchCashAccount.objects.filter(church=associated_church, sabbath_week=active_week, sabbath_week__month__quarter=active_quarter_info)

        total_week_cash = cash.aggregate(Sum('cash_generated'))['cash_generated__sum'] or 0
        total_cash_spent = cash.aggregate(Sum('cash_spent'))['cash_spent__sum'] or 0
        total_cash_to_bank = cash.aggregate(Sum('cash_to_bank'))['cash_to_bank__sum'] or 0
        cash_out =  float(total_cash_spent) +  float(total_cash_to_bank)
        cash_at_hand = float(total_week_cash) - float(cash_out)
        
        #total_week_income = church_incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        # Calculate total income excluding specific income_types
        excluded_income_types = ['APPRECIATION', 'LOOSE_OFFERING', 'CHILD_DEDICATION', 'THANKS_OFFERING', 'SABBATH_SCHOOL']
        total_week_income = church_incomes.exclude(income_type__in=excluded_income_types).aggregate(Sum('amount'))['amount__sum'] or 0

        total_week_expense = church_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

            
         #sum of tithe and offering from titheofferiing model
        church_tithes_and_offerings = TitheOffering.objects.filter(
        church_member__church= associated_church,
        sabbath_week=active_week, sabbath_week__month__quarter=active_quarter_info
        ).aggregate(
            total_tithe=Sum('tithe'),
            total_offering=Sum('offering'),
            total_project=Sum('project')
        )
        total_tithe=  church_tithes_and_offerings['total_tithe'] or 0
        total_offering=  church_tithes_and_offerings['total_offering'] or 0
        total_project=  church_tithes_and_offerings['total_project'] or 0
        combined_offering_church = CombinedOffering.objects.filter(associated_church=associated_church, sabbath_week=active_week, sabbath_week__month__quarter=active_quarter_info).first()
    
        weeks_combined_top_2=  total_tithe+ total_project + combined_offering_church.amount_due_church
       # Calculate the combined income for the week using data fromm tithe offering model
        weeks_combined_income_2= weeks_combined_top_2 + total_week_income
        weeks_combined_expense = total_week_expense 
        income_expence_balance = weeks_combined_income_2 - weeks_combined_expense

       
    user_context.update({
        'combined_offering_church':combined_offering_church ,
        'conference_info':conference_info,
        'district_info': district_info,
        'active_quarter_info': active_quarter_info,
        'total_tithe': total_tithe,
        'total_offering': total_offering,
        'total_project': total_project,
        'cash_at_hand':cash_at_hand ,
        'church_expenses': church_expenses,
        'church_incomes': church_incomes,
        'sabbath_week_start': sabbath_week_start,
        'sabbath_week_ends': sabbath_week_ends,
        'active_week_month': active_week_month,
        'total_week_cash': total_week_cash,
        'total_week_income': total_week_income,
        'weeks_combined_expense': weeks_combined_expense,
        'income_expence_balance':income_expence_balance,
        'weeks_combined_top_2': weeks_combined_top_2,
        'weeks_combined_income_2': weeks_combined_income_2,

      
    })

    return render(request, 'church/dashboard.html', user_context)



@login_required
def district_dashboard(request):
    context = getGlobalContext(request.user)

    # Check if the user is a district secretary or treasurer
    if request.user.role in ['District_secretary', 'District_treasurer']:
        associated_district = context.get('associated_district')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        active_week_month = active_week.month if active_week else None
       
        if associated_district:
            district_expenses = DistrictExpense.objects.filter(district=associated_district, sabbath_week=active_week, sabbath_week__month__quarter=active_quarter)
            district_incomes = DistrictIncome.objects.filter(district=associated_district, sabbath_week=active_week, sabbath_week__month__quarter=active_quarter)

            total_weekly_expense = district_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
            # Calculate the sum of all district incomes for the active week
            total_weekly_income = district_incomes.aggregate(Sum('amount'))['amount__sum'] or 0

            combined_offering_entry = CombinedOffering.objects.filter(
            church__district=associated_district,
            sabbath_week=active_week
            )
            total_amount_due_district = combined_offering_entry.aggregate(Sum('amount_due_district'))['amount_due_district__sum'] or 0

            # Get the value of amount_due_district_field for the active week
       

            combined_total_weekly_income =  total_amount_due_district + total_weekly_income 

            weekly_balance = combined_total_weekly_income - total_weekly_expense
            active_week_month = active_week.month if active_week else None
            
            
            # Get all information concerning the district
            income_form  = DistrictIncomeForm()
            expense_form = DistrictExpenseForm()

            district_info = {
                'combined_offering_entry':combined_offering_entry,
                'weekly_balance': weekly_balance,
                'combined_total_weekly_income':combined_total_weekly_income,
                'total_weekly_income':total_weekly_income,
                'total_weekly_expense':total_weekly_expense,
                'district_name': associated_district.district_name,
                'district_address': associated_district.address,
                'district_email': associated_district.email,
                'district_phone': associated_district.pastors_phone,
                'district_facebook': associated_district.facebook,
                'income_form':income_form,
                'expense_form':expense_form,
                'active_week_month':active_week_month,
                'total_amount_due_district': total_amount_due_district,
                'district_incomes': district_incomes,
                'district_expenses': district_expenses,
            }
            context['district_info'] = district_info

    return render(request, 'district/dashboard.html', context)
   
   
@login_required  
def conference_dashboard(request):
   if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        associated_church = context.get('associated_church')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        sabbath_week_start = context.get('sabbath_week_start')
        sabbath_week_ends = context.get('sabbath_week_ends')

        members = Member.objects.all()

        current_weeks_trustfunds = TrustFund.objects.filter(
                                                             sabbath_week = active_week,
                                                               sabbath_week__month__quarter=active_quarter
                                                               ).aggregate(
                                                                   total_tithe=Sum('tithe_amount'),
                                                                   total_offering=Sum('offering_amount'),
                                                                   
                                                                   )
        current_quater_trustfunds = TrustFund.objects.filter(                                              
                                                            sabbath_week__month__quarter=active_quarter
                                                               ).aggregate(
                                                                   total_tithe=Sum('tithe_amount'),
                                                                   total_offering=Sum('offering_amount'),
                                                                    total_amount=Sum('total_amount'),                                                                   
                                                                   )

        quater_total_tithe = current_quater_trustfunds['total_tithe'] or 0
        quater_total_offering = current_quater_trustfunds['total_offering'] or 0      
        quater_total_amount = current_quater_trustfunds['total_amount'] or 0               

        total_tithe = current_weeks_trustfunds['total_tithe'] or 0
        total_offering = current_weeks_trustfunds['total_offering'] or 0
        sum_off_trustfund = total_tithe + total_offering
        context.update({
            'conference':conference,
            'active_week':active_week,
            'active_quarter':active_quarter,
            'members': members,
            'sabbath_week_start':sabbath_week_start,
            'sabbath_week_ends': sabbath_week_ends,
            'total_tithe': total_tithe,
            'total_offering':total_offering,
            'sum_off_trustfund':sum_off_trustfund,
            'quater_total_tithe':quater_total_tithe,
            'quater_total_offering':quater_total_offering,
            'quater_total_amount':quater_total_amount,


        })
        return render(request,'conference/dashboard.html',context)
  
   

@login_required
def setup_accounting(request):
    context = getGlobalContext(request.user)
    form1 = AddQuarterForm()
    form2 = AddMonthForm()
    form3 = AddSabbathForm()
    all_quater= Quarter.objects.all()
    months = Month.objects.all()
    sabbaths = Sabbath.objects.all()
    context.update({
        'form1':form1,
        'form2':form2,
        'form3':form3,
        'all_quater':all_quater,
        'months':months,
        'sabbaths':sabbaths,
    })
    return render(request, 'conference/setup_accounts.html',context)



@login_required
def add_user(request):
  
    if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        districts = District.objects.all()
        context.update({
            'active_week':active_week,
            'active_quarter':active_quarter,
            'conference':conference,        
             })

    
        assign_officer_form = AddAssignedOfficerForm(request.POST)
        add_officer_form = AddOfficer(request.POST, request.FILES)
        

        
        context.update({
            'assign_officer_form':assign_officer_form,
            'add_officer_form':add_officer_form
        })
        
        return render(request, 'conference/add_users.html',context)
    


@login_required
def process_add_officer_form(request):
    if request.method == 'POST':
        form = AddOfficer(request.POST, request.FILES)
       

        if form.is_valid():
            role_mapping = {
                'admin_form': 'Admin',
                'church_tre_form': 'Church_treasurer',
                'church_sec_form': 'Church_secretary',
                'district_sec_form': 'District_secretary',
                'district_tre_form': 'District_treasurer',
            }

            # Determine the form submitted based on the button name
            submitted_form = next((key for key in role_mapping.keys() if key in request.POST), None)

            if submitted_form:
                user = form.save(commit=False)
                # Set the role based on the mapping
                user.set_password('abcd123')
                user.role = role_mapping[submitted_form]
                user.save()
                
                return redirect('dashboard:assign_officer')  # Redirect to a success page

    else:
        form = AddOfficer()

    return render(request, 'conference/add_users.html', {'form': form})
       
    
   
 #list of admins and add new admin modal  
@login_required
def admins(request):
    context = getGlobalContext(request.user)
    admins = User.objects.filter(role="Admin")

    if request.method == 'POST':
        form = AddAdminForm(request.POST, request.FILES)
        if form.is_valid:
            admin = form.save(commit=False)
            admin.role = "Admin"
            admin.raw_password = "abcd123"
            admin.set_password("abcd123")
            admin.username = "admin" + str(random.randint(100,999))
            admin.save()

            form = AddAdminForm()
            context.update({
                'message': 'New admin added successfully',
                'form':form,
                'admins':admins

            })
        else:
            
            context.update({
                'error': form.errors, 
                'admins':admins               
            })

            form = AddAdminForm()
            context.update({
                'form':form,
            })

    else:
       
        form = AddAdminForm()
        context.update({
            'admins':admins,
            'form':form,
        })
    return render(request, "backend/users/admins.html", context)
   

# view single admin
@login_required
def admin(request, pk):
    context = getGlobalContext(request.user)
    admin = User.objects.get(pk=pk)
    context.update({
        'admin':admin,
    })
    return render(request, "backend/users/admin-details.html", context)
    
    

@login_required
def disable_church_treasurer(request, pk):
    church_treasurer = get_object_or_404(User, pk=pk)
    context = getGlobalContext(request.user)
    form = AddChurchTreasurer()

    church_treasurer.active = False
    church_treasurer.save()

    context.update({
        'message': 'Parent disabled successfully',
        'form':form,
        'parents':parents,

    })
    return render(request, "backend/users/parents.html", context)



@login_required
def delete_church_treasurer(request, pk):
    church_treasurer = get_object_or_404(User, pk=pk)
    context = getGlobalContext(request.user)
    form = AddChurchTreasurer()
    church_treasurers = User.objects.filter(role="Church_treasurer")

    church_treasurer.delete()

    context.update({
        'message': 'Parent deleted successfully',
        
        'form':form,
        'church_treasurers ':church_treasurers ,
    })
    return redirect("backend:parents")
    


@login_required
def disable_secretary(request, pk):
    church_secretary = get_object_or_404(User, pk=pk)
    context = getGlobalContext(request.user)
    form = AddChurchSecretary()

    church_secretary.active = False
    church_secretary.save()

    context.update({
        'message': 'Secretary disabled successfully',
        'form':form,
        

    })
    return render(request, "backend/users/parents.html", context)


@login_required
def delete_church_secretary(request, pk):
    church_secretary = get_object_or_404(User, pk=pk)
    context = getGlobalContext(request.user)
    form = AddChurchSecretary()
    church_secretaries = User.objects.filter(role="Church_secretary")

    church_secretary.delete()

    context.update({
        'message': 'Secretary deleted successfully',
        
        'form':form,
        'church_secretaries':church_secretaries ,
    })
    return redirect("backend:parents")
    


@login_required
def disable_district_treasurer(request, pk):
    district_treasurer = get_object_or_404(User, pk=pk)
    context = getGlobalContext(request.user)
    form = AddDistrictTreasurer()

    district_treasurer.active = False
    district_treasurer.save()

    context.update({
        'message': 'Parent disabled successfully',
        'form':form,        

    })
    return render(request, "backend/users/parents.html", context)


@login_required
def delete_district_treasurer(request, pk):
    district_treasurer = get_object_or_404(User, pk=pk)
    context = getGlobalContext(request.user)
    form = AddDistrictTreasurer()
    district_treasurers = User.objects.filter(role="District_treasurer")

    district_treasurer.delete()

    context.update({
        'message': 'Parent deleted successfully',
        
        'form':form,
        'district_treasurers':district_treasurers ,
    })
    return redirect("backend:parents")
    


@login_required
def disable_secretary(request, pk):
    district_secretary = get_object_or_404(User, pk=pk)
    context = getGlobalContext(request.user)
    form = AddDistrictSecretary()

    district_secretary.active = False
    district_secretary.save()

    context.update({
        'message': 'Parent disabled successfully',
        'form':form,
        

    })
    return render(request, "backend/users/parents.html", context)


@login_required
def delete_district_secretary(request, pk):
    district_secretary = get_object_or_404(User, pk=pk)
    context = getGlobalContext(request.user)
    form = AddDistrictSecretary()
    district_secretaries = User.objects.filter(role="District_secretary")

    district_secretary.delete()

    context.update({
        'message': 'Parent deleted successfully',
        
        'form':form,
        'district_secretaries':district_secretaries ,
    })
    return redirect("backend:parents")
    


@login_required
def districts(request):
    context = getGlobalContext(request.user)
    #districts = District.objects.all()

    if request.method == 'POST':
        form = AddDistrictForm(request.POST, request.FILES)
        if form.is_valid:
            district = form.save(commit=False)
            
            district.save()
            messages.success(request, "Districted add successfull. Add A church")
            return redirect('dashboard:create_church')
        else:   
            messages.success(request, "Something Went Wrong Unable to Create District")
            return redirect('dashboard:create_district')       
           
    else:      
        form = AddDistrictForm()
        context.update({
            'form':form,            
        })
    return render(request, "conference/create_district.html", context)


@login_required
def edit_district(request, pk):
    context = getGlobalContext(request.user)
    district = District.objects.get(pk=pk)
    form = AddDistrictForm(instance=district)

    if request.method == "POST":
        form = AddDistrictForm(request.POST, instance=district)
        district = form.save(commit=False)
        district.save()
        context.update({
            'message':'Section edited successfully'
        })   
    context.update({
        'district':district,
        'form':form,       
    })
    return render(request, "backend/sections/section-details.html", context)


@login_required
def admin_view_district(request, district_id):
    if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        sabbath_week_start = context.get('sabbath_week_start')
        sabbath_week_ends = context.get('sabbath_week_ends')

        district = get_object_or_404(District, district_id=district_id)
        churches = Church.objects.filter(district=district)
        assigned_officers = AssignedOfficer.objects.filter(district=district)

        # Get expenses and income for the district
        district_expenses = DistrictExpense.objects.filter(district=district, sabbath_week=active_week, sabbath_week__month__quarter = active_quarter)
        district_incomes = DistrictIncome.objects.filter(district=district, sabbath_week=active_week, sabbath_week__month__quarter= active_quarter)

        total_weekly_expense = district_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        # Calculate the sum of all district incomes for the active week
        total_weekly_income = district_incomes.aggregate(Sum('amount'))['amount__sum'] or 0

        combined_offering_entry = CombinedOffering.objects.filter(
            church__district=district,
            sabbath_week=active_week,
            sabbath_week__month__quarter = active_quarter
        )
        # Sum up the amount_due_district for all entries
        total_amount_due_district = combined_offering_entry.aggregate(Sum('amount_due_district'))['amount_due_district__sum'] or 0

        # Get the value of amount_due_district_field for the active week
       

        combined_total_weekly_income =  total_amount_due_district + total_weekly_income 

        weekly_balance = combined_total_weekly_income - total_weekly_expense
        active_week_month = active_week.month if active_week else None

        context.update({
            'active_week':active_week,
            'active_quarter':active_quarter,
            'conference':conference,  
            'combined_offering_entry': combined_offering_entry,
            'combined_total_weekly_income': combined_total_weekly_income,
            'district': district,
            'churches': churches,
            'assigned_officers':assigned_officers,
            'district_expenses':district_expenses,
            'district_incomes': district_incomes,
            'sabbath_week_start':sabbath_week_start,
            'sabbath_week_ends':sabbath_week_ends,
            'total_weekly_expense':total_weekly_expense,
            'total_weekly_income':total_weekly_income,
            'active_week_month': active_week_month,
            'weekly_balance':weekly_balance,
            
             })

    return render(request, 'conference/view_district_info.html', context)



@login_required
def delete_district(request, pk):
    district = get_object_or_404(District, pk=pk)
    context = getGlobalContext(request.user)
    form = AddDistrictForm()
    district = district.objects.all()

    district.delete()
    messages.success(request, "District Deleted successfully")
    context.update({
        'form':form,
        'district':district,
    })
    return redirect("backend:sections")

    
@login_required
def all_church(request):
    if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        churches = Church.objects.all()

        context.update({
            'active_week':active_week,
            'active_quarter':active_quarter,
            'conference':conference,    
            'churches':churches
             })
   
        return render(request,'conference/all_churches.html',context)


@login_required
def all_members(request):
    if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        members = Member.objects.all()

        context.update({
            'active_week':active_week,
            'active_quarter':active_quarter,
            'conference':conference,  
            'members':members    
             })
   
        return render(request,'conference/all_members.html',context)


@login_required
def all_officers(request):
    if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        officers = AssignedOfficer.objects.all()

        context.update({
            'active_week':active_week,
            'active_quarter':active_quarter,
            'conference':conference,   
            'officers':officers     
             })
   
        return render(request,'conference/all_officers.html',context)


@login_required
def all_districts(request):
    if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        districts = District.objects.all()

        context.update({
            'active_week':active_week,
            'active_quarter':active_quarter,
            'conference':conference, 
            'districts':districts       
             })
   
    return render(request,'conference/all_districts.html', context)
    
    
    
@login_required
def churches(request):
    context = getGlobalContext(request.user)
    #churches = Church.objects.all()

    if request.method == 'POST':
        form = AddChurchForm(request.POST, request.FILES)
        if form.is_valid:
            church = form.save(commit=False)
            
            church.save()

            form = AddChurchForm()
            messages.success(request, "Church  added Successfully, Add Church Account Officer")
            return redirect('dashboard:add_user')
        else:
            
            context.update({
                'error': form.errors,            
            })

            form = AddChurchForm()
            messages.error(request,'Unable to add church, Try Again') 
            context.update({
                'form':form,
            })

    else:
       
        form = AddChurchForm()
        context.update({
            'churches':churches,
            'form':form,
             
        })
    return render(request, "conference/create_church.html", context)

@login_required
def admin_view_church(request, church_id):
    if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        sabbath_week_start = context.get('sabbath_week_start')
        sabbath_week_ends = context.get('sabbath_week_ends')
       

        church = get_object_or_404(Church, church_id=church_id)
        members = Member.objects.filter(church=church)
        assigned_officers = AssignedOfficer.objects.filter(church=church)

        # Get expenses and income for the district
        church_expenses = ChurchExpense.objects.filter(church=church, sabbath=active_week, sabbath__month__quarter=active_quarter)
        church_incomes = ChurchIncome.objects.filter(church=church, sabbath=active_week, sabbath__month__quarter=active_quarter)
        cash = ChurchCashAccount.objects.filter(church=church, sabbath_week=active_week, sabbath_week__month__quarter=active_quarter)

        total_week_cash = cash.aggregate(Sum('cash_generated'))['cash_generated__sum'] or 0
        total_cash_spent = cash.aggregate(Sum('cash_spent'))['cash_spent__sum'] or 0
        total_cash_to_bank = cash.aggregate(Sum('cash_to_bank'))['cash_to_bank__sum'] or 0

        cash_out =  float(total_cash_spent) +  float(total_cash_to_bank)
        cash_at_hand = float(total_week_cash) - float(cash_out)

        # Calculate the sum of income for the church
        total_week_income = church_incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_week_expense = church_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        # this is  not in use ->Calculate the sum of WeeklyTransaction (tithe_sum + offering_sum + project_sum) for the active week and church
        # starts
        # weekly_transaction_data = WeeklyTransaction.objects.filter(
        #     sabbath_week=active_week,
        #     church=church
        # ).aggregate(
        #     total_tithe=Sum('tithe_sum'),
        #     total_offering=Sum('offering_sum'),
        #     total_project=Sum('project_sum')
        # )
        # total_week_tithe = weekly_transaction_data['total_tithe'] or 0
        # total_week_offering = weekly_transaction_data['total_offering'] or 0
        # total_week_project = weekly_transaction_data['total_project'] or 0
        # # ends
        
        #sum of tithe and offering from titheofferiing model
        church_tithes_and_offerings = TitheOffering.objects.filter(
        church_member__church=church,
        sabbath_week=active_week,sabbath_week__month__quarter=active_quarter
        ).aggregate(
            total_tithe=Sum('tithe'),
            total_offering=Sum('offering'),
            total_project=Sum('project')
        )
        total_tithe=  church_tithes_and_offerings['total_tithe'] or 0
        total_offering=  church_tithes_and_offerings['total_offering'] or 0
        total_project=  church_tithes_and_offerings['total_project'] or 0
        # sum of weekly income ffrom tithe and offering model
        weeks_combined_top_2=  total_tithe+ total_project + total_offering
        # sum of weekly transaction from weekly transaction
        #weeks_combined_t_o_p = total_week_tithe + total_week_offering + total_week_project

        # Calculate the combined income for the week using data fromm weekly transaction model
       # weeks_combined_income = total_week_income + total_week_tithe + total_week_offering + total_week_project
       
        # Calculate the combined income for the week using data fromm tithe offering model
        weeks_combined_income_2= weeks_combined_top_2 + total_week_income


        weeks_combined_expense = total_week_expense

        income_expence_balance = weeks_combined_income_2 - weeks_combined_expense

        active_week_month = active_week.month if active_week else None

        context.update({
            'active_week': active_week,
            'active_quarter': active_quarter,
            'cash_at_hand': cash_at_hand,
            'conference': conference,
            'church': church,
            'church_name': church,
            'assigned_officers': assigned_officers,
            'church_expenses': church_expenses,
            'church_incomes': church_incomes,
            'sabbath_week_start': sabbath_week_start,
            'sabbath_week_ends': sabbath_week_ends,
            'active_week_month': active_week_month,
            'total_week_cash': total_week_cash,
            'total_week_income': total_week_income,
            # 'total_week_tithe': total_week_tithe,
            # 'total_week_offering': total_week_offering,
            # 'total_week_project': total_week_project,
            # 'weeks_combined_income': weeks_combined_income,
            # 'weeks_combined_t_o_p': weeks_combined_t_o_p ,
            'weeks_combined_expense': weeks_combined_expense,
            'income_expence_balance':income_expence_balance,
            #updated from tithe offering model instead of weekly 
            'total_tithe':total_tithe,
            'total_offering':total_offering,
            'total_project':total_project,
            'weeks_combined_top_2': weeks_combined_top_2,
            'weeks_combined_income_2': weeks_combined_income_2,

        })

    return render(request, 'conference/view_church_info.html', context)



@login_required
def delete_class(request, pk):
    church = get_object_or_404(Church, pk=pk)
    context = getGlobalContext(request.user)
    form = AddChurchForm()
    churches = Church.objects.all()


    church.delete()

    context.update({
        'message': 'class deleted successfully',
        
        'form':form,
        'churches':churches,
    })
    return redirect("backend:classes")
    
    
@login_required
def assign_officer(request):
    context = getGlobalContext(request.user)
   
    if request.method == 'POST':
        form = AddAssignedOfficerForm(request.POST)
        if form.is_valid():
            # Check if the officer is already assigned to a church or district
            officer = form.cleaned_data['officer']
            existing_assignment = AssignedOfficer.objects.filter(officer=officer).exists()

            if existing_assignment:
                messages.error(request, ' Cannot assign officer. This officer is already assigned to a Church/District.')
                return redirect('dashboard:assign_officer')

            assigned_officer = form.save()

            messages.success(request, 'New officer assigned successfully')
            context.update({
                'form': form,
            })
            return redirect('dashboard:users_overview')
        else:
            context.update({
                'error': form.errors,
            })
            messages.error(request, 'Unable to assign the user to a Church/District')
            return redirect('dashboard:assign_officer')
    else:
        assign_officer_form = AddAssignedOfficerForm()
        context.update({
            'assign_officer_form': assign_officer_form,     
        })
    return render(request, 'conference/assign_officer.html', context)




@login_required
def delete_assigned_officer(request, pk):
    assigned_officer = get_object_or_404(Assignedofficer, pk=pk)
    context = getGlobalContext(request.user)
    form = AddAssignedOfficerForm()
    assigned_Officers = AssignedOfficer.objects.all()


    assigned_officer.delete()

    context.update({
        'message': 'Assigned class deleted successfully',
        
        'form':form,
        'assigned_officers':assigned_officers,
    })
    return redirect("backend:assigned_classes")



@login_required
def add_quarter(request):
    context = getGlobalContext(request.user)

    if request.method == 'POST':
        form = AddQuarterForm(request.POST)
        if form.is_valid:
            quarter = form.save(commit=False)
            
            quarter.save()

            form = AddQuarterForm()
            messages.success(request, 'Quarter Created successfuly')
            context.update({
                
                'form':form,

            })
            return redirect('dashboard:setup_accounting')
        else:
            messages.error(request, 'unable to create New quarted ')
            context.update({
                'error': form.errors,
                          
            })

            form = AddQuarterForm()
            context.update({
                'form':form,
            })
        return redirect('dashboard:setup_accounting')
    else:
       
        form = AddQuarterForm()
        context.update({
            'form':form,
             
        })
    return redirect('dashboard:setup_accounting')


# Activate Sabbath
@login_required
def activate_quarter(request, quarter_id):
    context = getGlobalContext(request.user)

    if request.user.role == 'Admin':

        try:
           current_active_quarter = Quarter.objects.get(is_active=True)
           current_active_quarter.is_active = False
           current_active_quarter.save()


           selected_quarter = get_object_or_404(Quarter, quarter_id=quarter_id)
           selected_quarter.is_active = True
           selected_quarter.save()

           messages.success(request, 'Quarter activated successfully')
        except Exception as e:
            messages.error(request, f'Unable to activate quarter: {str(e)}')
            
    return redirect('dashboard:setup_accounting')
 


@login_required
def delete_quarter(request, quarter_id):
     
    quarter = get_object_or_404(Quarter, quarter_id=quarter_id)
    if quarter:
        context = getGlobalContext(request.user)
        quarter.delete()

        messages.success(request, 'Quarter Was Deleted')
        return redirect("dashboard:setup_accounting")
    else:
        messages.error(request, 'unable to delete quarter, try again')
        return redirect("dashboard:setup_accounting")



@login_required
def add_month(request):
    context = getGlobalContext(request.user)

    if request.method == 'POST':
        form = AddMonthForm(request.POST, request.FILES)
        if form.is_valid:
            month = form.save(commit=False)
            month.save()
            form = AddMonthForm()
            context.update({
                'message': 'New Month added successfully',
                'form':form,
                
            })
            return redirect('dashboard:setup_accounting')
        else:
            
            context.update({
                'error': form.errors,
                  
            })

            form = AddMonthForm()
            context.update({
                'form':form,
               
            })
        return redirect('dashboard:setup_accounting')
    else:
       
        form = AddMonthForm()
        context.update({
            'form':form,
             
        })
    return redirect('dashboard:setup_accounting')



@login_required
def edit_month(request, month_id):
    context = getGlobalContext(request.user)
    month = Month.objects.get(month_id=month_id)
    form = AddMonthForm(instance=month)

    if request.method == "POST":
        form = AddMonthForm(request.POST, instance=month)
        month = form.save(commit=False)
        month.save()
        context.update({
            'message':'Quarter edited successfully'
        })
    
    context.update({
        'month':month,
        'form':form,
         
    })
    return render(request, "backend/sessions/session-details.html", context)


# Activate Sabbath
@login_required
def activate_month(request, month_id):
    context = getGlobalContext(request.user)

    if request.user.role == 'Admin':

        try:
           current_active_month = Month.objects.get(is_active=True)
           current_active_month.is_active = False
           current_active_month.save()


           selected_month = get_object_or_404(Month, month_id=month_id)
           selected_month.is_active = True
           selected_month.save()

           messages.success(request, 'Month activated successfully')
        except Exception as e:
            messages.error(request, f'Unable to activate Month: {str(e)}')
            
    return redirect('dashboard:setup_accounting')
 
    

@login_required
def delete_month(request, month_id):
    month = get_object_or_404(Month, month_id=month_id)
    context = getGlobalContext(request.user)

    month.delete()

    context.update({
        'message': 'Month deleted successfully',
     
    })
    return redirect("dashboard:setup_accounting")



@login_required
def add_sabbath(request):
    context = getGlobalContext(request.user)
    

    if request.method == 'POST':
        form = AddSabbathForm(request.POST)
        if form.is_valid:
            sabbath = form.save(commit=False)
            sabbath.save()
            form = AddSabbathForm()
            context.update({
                'message': 'New Sabbath Day added successfully',
                'form':form,
            })
            return redirect('dashboard:setup_accounting')
        else:
          
            context.update({
                'error': form.errors,
                  
            })

            form = AddSabbathForm()
            context.update({
                'form':form,
            })
        return redirect('dashboard:setup_accounting')
    else:
       
        form = AddSabbathForm()
        context.update({
            'form':form,
             
        })
    return redirect('dashboard:setup_accounting')



@login_required
def edit_sabbath(request, sabbath_id):
    context = getGlobalContext(request.user)
    sabbath = Sabbath.objects.get(sabbath_id=sabbath_id)
    form = AddSabbathForm(instance=sabbath)

    if request.method == "POST":
        form = AddSabbathForm(request.POST, instance=sabbath)
        month = form.save(commit=False)
        month.save()
        context.update({
            'message':'Sabbath edited successfully'
        })
    
    context.update({
        'sabbath':sabbath,
        'form':form,
         
    })
    return render(request, "backend/sessions/session-details.html", context)
    

# Activate Sabbath
@login_required
def activate_sabbath(request, sabbath_id):
    context = getGlobalContext(request.user)

    if request.user.role == 'Admin':

        try:
           current_active_sabbath = Sabbath.objects.get(is_active=True)
           current_active_sabbath.is_active = False
           current_active_sabbath.save()


           selected_sabbath = get_object_or_404(Sabbath, sabbath_id=sabbath_id)
           selected_sabbath.is_active = True
           selected_sabbath.save()

           messages.success(request, 'Sabbath activated successfully')
        except Exception as e:
            messages.error(request, f'Unable to activate Sabbath: {str(e)}')
            
    return redirect('dashboard:setup_accounting')
 

@login_required
def delete_sabbath(request, sabbath_id):
    sabbath = get_object_or_404(Sabbath, sabbath_id=sabbath_id)
    context = getGlobalContext(request.user)

    sabbath.delete()

    context.update({
        'message': 'Sabbath deleted successfully',
    })
    return redirect("dashboard:setup_accounting")




@login_required
def change_login_details(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = request.user
    user.username = username
    user.raw_password = password
    user.set_password(password)
    user.save()

    return redirect('backend:signin')

@login_required
def edit_user(request, pk):
    context = getGlobalContext(request.user)
    user = get_object_or_404(User, pk=pk)

    if user.role == "Admin":
        form = AddAdminForm(instance=user)
    if user.role == "Church_treasurer":
        form = AddTeacherForm(instance=user)
    if user.role == "Church_secretary":
        form = AddAccountantForm(instance=user)
    if user.role == "District_treasurer":
        form = AddParentForm(instance=user)
    if user.role == "District_secretary":
        form = AddStudentForm(instance=user)

    if request.method == "POST":
        
        if user.role == "Admin":
            form = AddAdminForm(request.POST, request.FILES, instance=user)
        if user.role == "Church_treasurer":
            form = AddTeacherForm(request.POST, request.FILES, instance=user)
        if user.role == "Church_secretary":
            form = AddAccountantForm(request.POST, request.FILES, instance=user)
        if user.role == "District_secretary":
            form = AddParentForm(request.POST, request.FILES, instance=user)
        if user.role == "District_treasurer":
            form = AddStudentForm(request.POST, request.FILES, instance=user)
        
        user = form.save(commit=False)
        user.save()


    context.update({
        'target':user,
        'form':form,
    })

    return render(request, "backend/users/edit-user.html", context)



@login_required
def profile(request):
    user_context = getGlobalContext(request.user)

    # Check if the user is a church secretary or treasurer
    if request.user.role in ['Church_secretary', 'Church_treasurer','District_secretary','District_treasurer','Admin']:
    
        associated_church = user_context.get('associated_church')
       
        if associated_church:
            # Get all information concerning the church
            church_info = {
                'church_name': associated_church.church_name,
                'church_district': associated_church.district,
                'church_address': associated_church.address,
                'church_email': associated_church.email,
                'church_phone': associated_church.phone,
                'church_facebook': associated_church.facebook,
                # Add more fields as needed
            }
            user_context.update(church_info)
            
   
            form = EditProfileForm(instance=request.user)

            if request.method == "POST":
                form = EditProfileForm(request.POST, request.FILES, instance=request.user)
                u = form.save(commit=False)
                u.save()
            else:

                user_context.update({
                      'form.errors':form.errors,
                       'form':form,
                      })
        return render(request, "pages/profile.html", user_context)
    else:
        return   HttpResponse('You are not perimitted to view this page')
    
 
 
@login_required
def users_overview(request):
    if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        active_year = context.get('active_year')

        role_users= User.objects.all().count()
        churches = Church.objects.all().count()
        assigned_officer =AssignedOfficer.objects.all()
        districts = District.objects.all().count()
        members = Member.objects.all().count()
        context.update({
            'active_week':active_week,
            'active_quarter':active_quarter,
            'conference':conference,
            'role_users':role_users,
            'churches':churches,
            'districts': districts,
            'assigned_officer':assigned_officer,
            'members':members,

            'active_year':active_year,
                            })

        return render(request, 'conference/users_overview.html',context)
    
    
 
@login_required
def view_member(request, member_id):
    
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        church_name =context.get('associated_church')
        active_year = context.get('active_year')
        
        active_week_month = active_week.month if active_week else None
        

        member = get_object_or_404(Member, member_id=member_id)
        tithe_offerings = TitheOffering.objects.filter(church_member=member, sabbath_week__month__quarter=active_quarter)
   
        context.update({
            'active_week':active_week,
            'active_quarter':active_quarter,
            'conference':conference,
            'tithe_offerings':tithe_offerings,            
            'member':member,
            'active_week_month': active_week_month,
            'church_name':church_name,
            
                            })

        return render(request, 'conference/view_member_info.html',context)
    

@login_required
def admin_view_church_account_detail(request, church_id):
    
        context = getGlobalContext(request.user)
        conference = context.get('conference')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        active_week_month = active_week.month if active_week else None
        church = get_object_or_404(Church, church_id=church_id)
        
        church_tithes_and_offerings = TitheOffering.objects.filter(
        church_member__church=church,
        sabbath_week=active_week
        )
        weekly_cash_transaction = ChurchCashAccount.objects.filter(church=church, sabbath_week=active_week )

        context.update({
            'active_week': active_week,
            'active_quarter': active_quarter,
            'conference': conference,          
            'active_week_month': active_week_month,
            'church_tithes_and_offerings': church_tithes_and_offerings,
            'church':church,
            'church_name':church,
            'weekly_cash_transaction': weekly_cash_transaction,
        })

        return render(request, 'conference/view_church_weekly_accounting.html', context)
 



@login_required
def upload_tithe_offering(request):
    context = getGlobalContext(request.user)
    associated_church = context.get('associated_church')
    active_week = context.get('active_week')

    if request.method == 'POST':
        form = UploadTitheOfferingForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
                # Process the CSV file
                process_csv_file(csv_file, associated_church, active_week)
                messages.success(request, 'Tithe and offering data uploaded successfully.')
            except Exception as e:
                messages.error(request, f'Error uploading CSV file: {str(e)}')
            return redirect('church:tithe_offering')
        else:
            messages.error(request, 'Error uploading CSV file. Please try again.')
    else:
        form = UploadTitheOfferingForm()
        messages.error(request, 'Error uploading CSV file. Please try again.')

    return redirect('church:tithe_offering')

def process_csv_file(csv_file, associated_church, active_week):
   

    try:
        reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

        for row in reader:
            # Ensure all required fields are present in each row
            required_fields = ['tithe_card_number', 'tithe_amount', 'offering_amount', 'project_amount', 'payment_method']
            for field in required_fields:
                if field not in row:
                    raise ValidationError(f'Missing required field: {field}')

            tithe_card_number = row['tithe_card_number']
            tithe_amount = row['tithe_amount']
            offering_amount = row['offering_amount']
            project_amount = row['project_amount']
            payment_method = row['payment_method']

            # Get the member associated with the tithe_card_number and the associated_church
            member = Member.objects.filter(
                tithe_card_number=tithe_card_number,
                church=associated_church
            ).first()

            if member:
                # Create or update TitheOffering entry for the week
                tithe_offering, created = TitheOffering.objects.update_or_create(
                    church_member=member,
                    sabbath_week=active_week,
                    defaults={
                        'tithe': tithe_amount,
                        'offering': offering_amount,
                        'project': project_amount,
                        'payment_method': payment_method,
                    }
                )
    except Exception as e:
        raise e  # Propagate the exception to the caller
    


@login_required
def upload_members(request):
    context = getGlobalContext(request.user)
    associated_church = context.get('associated_church')

    if request.method == 'POST':
        form = UploadMembersForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
                process_members_csv_file(csv_file, associated_church)
                messages.success(request, 'Member data uploaded successfully.')
            except Exception as e:
                messages.error(request, f'Error uploading CSV file: {str(e)}')
            return redirect('church:add_new_member')
        else:
            messages.error(request, 'Error uploading CSV file. Please try again.')
    else:
        form = UploadMembersForm()
        messages.error(request, 'Error uploading CSV file. Please try again.')
    return redirect('church:add_new_member')



def process_members_csv_file(csv_file, associated_church):
    try:
        # Try decoding with ISO-8859-1
        try:
            reader = csv.DictReader(csv_file.read().decode('ISO-8859-1').splitlines())
        except UnicodeDecodeError:
            # If decoding with ISO-8859-1 fails, try UTF-8
            csv_file.seek(0)  # Reset file pointer
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

        for row in reader:
            tithe_card_number = row.get('tithe_card_number')
            member_name = row.get('member_name')
            member_email = row.get('member_email')
            member_phone = row.get('member_phone')
            member_gender = row.get('member_gender')

            # Create or update Member entry
            member, created = Member.objects.update_or_create(
                tithe_card_number=tithe_card_number,
                church=associated_church,
                defaults={
                    'member_name': member_name,
                    'member_email': member_email,
                    'member_phone': member_phone,
                    'member_Gender': member_gender,
                }
            )
    except Exception as e:
        raise e  # Propagate the exception to the caller



def view_trustfunds (request):
    if request.user.role == "Admin":
        context = getGlobalContext(request.user)
        conference  = context.get('conference')
        associated_church = context.get('associated_church')
        active_week = context.get('active_week')
        active_quarter = context.get('active_quarter')
        sabbath_week_start = context.get('sabbath_week_start')
        sabbath_week_ends = context.get('sabbath_week_ends')
        
        current_weeks_trustfunds = TrustFund.objects.filter(
                                                            sabbath_week = active_week,
                                                            sabbath_week__month__quarter=active_quarter
                                                               )
                                                               
                                                   
                                                               
        context.update({
            'conference':conference,
            'active_week':active_week,
            'active_quarter':active_quarter,
            'current_weeks_trustfunds':current_weeks_trustfunds,
           
        })
        

        return render(request,'conference/trustfund_weekly_detail.html', context)