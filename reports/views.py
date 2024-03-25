from django.shortcuts import render
from .forms import *
from accounts.models import *
from accounting.models import *
from django.contrib.auth.decorators import login_required
from accounts.utils import getGlobalContext



# Create your views here.
@login_required
def reports(request):
    context = getGlobalContext(request.user)
    role = request.user.role
    active_week= context.get('active_week')
    active_quarter = context.get('active_quarter')  
    active_week_month = active_week.month if active_week else None

    form1 =  IncomeExpenseReportForm()
    form2= DistrictTrustfundForm()
    form3 = MonthForm()

    context = {
        'form1':form1,
        'form2':form2,
        'form3':form3,
        'active_week':active_week,
        'active_week_month':active_week_month,
        'active_quarter':active_quarter,

        }
    return render(request, 'reports/reports.html',context)



@login_required
def admin_church_income_expense_report(request):
    context = getGlobalContext(request.user)
    active_week= context.get('active_week')
    active_quarter = context.get('active_quarter')  
    active_week_month = active_week.month if active_week else None
    
    if request.user.role == "Admin":
        form = IncomeExpenseReportForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            church = form.cleaned_data['church']
            month = form.cleaned_data['month']

            sabbaths = Sabbath.objects.filter(month=month)

            # Query ChurchIncome and ChurchExpense for the selected church and sabbaths
            church_income = ChurchIncome.objects.filter(church=church, sabbath__in=sabbaths)
            church_expense = ChurchExpense.objects.filter(church=church, sabbath__in=sabbaths)
           

            context = {
                'church':church,
                'month':month,
                'church_income': church_income,
                'church_expense': church_expense,
                'active_week':active_week,
                'active_week_month':active_week_month,
                'active_quarter':active_quarter,

            }
        return render(request, 'reports/report_template.html', context)



def admin_church_trustfund_report(request):
    context = getGlobalContext(request.user)
    church_members = Member.objects.all()
    active_week= context.get('active_week')
    active_quarter = context.get('active_quarter')  
    active_week_month = active_week.month if active_week else None
    
    if request.user.role == "Admin":
        form = IncomeExpenseReportForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            church = form.cleaned_data['church']
            month = form.cleaned_data['month']

            # Query the Sabbath instances for the selected month
            sabbaths = Sabbath.objects.filter(month=month)

            # Query ChurchIncome and ChurchExpense for the selected church and sabbaths
            church_trustfunds = TrustFund.objects.filter(church=church, sabbath_week__in=sabbaths)
          
        
            context = {
                'church':church,
                'month':month,
                'church_trustfunds': church_trustfunds,
                'active_week':active_week,
                'active_week_month':active_week_month,
                'active_quarter':active_quarter,
            }
        return render(request, 'reports/report_trustfund_template.html', context)



@login_required
def admin_district_trustfund_report(request):
    context = getGlobalContext(request.user)
    active_week= context.get('active_week')
    active_quarter = context.get('active_quarter')  
    active_week_month = active_week.month if active_week else None
    
    if request.user.role == "Admin":
        form = DistrictTrustfundForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            district = form.cleaned_data['district']
            month = form.cleaned_data['month']

            # Query CombinedOffering for the selected district and month
            combined_offerings = CombinedOffering.objects.filter(
                associated_church__district=district,
                sabbath_week__month=month
            )

            # Preprocess data to group by week and church
            data = {}
            for offering in combined_offerings:
                week = offering.sabbath_week.sabbath_alias
                church = offering.associated_church
                if week not in data:
                    data[week] = {
                        'total_amount_due_district': 0,
                        'churches': {}
                    }
                if church not in data[week]['churches']:
                    data[week]['churches'][church] = {
                        'church_name': church.church_name,
                        'amount_due_district': 0
                    }
                data[week]['churches'][church]['amount_due_district'] += offering.amount_due_district
                data[week]['total_amount_due_district'] += offering.amount_due_district

            context = {
                'district': district,
                'month': month,
                'data': data,
                'active_week':active_week,
                'active_week_month':active_week_month,
                'active_quarter':active_quarter,
            }
            return render(request, 'reports/district_trustfund_template.html', context)



@login_required
def  admin_member_tithe_offering_report(request, member_id):
    context = getGlobalContext(request.user)
    active_week= context.get('active_week')
    active_quarter = context.get('active_quarter')  
    active_week_month = active_week.month if active_week else None
    
    if request.user.role == "Admin":

        member = Member.objects.get(member_id=member_id)

        active_quarter = Quarter.objects.get(is_active=True)
        tithe_offering = TitheOffering.objects.filter(
            church_member=member,
            sabbath_week__month__quarter=active_quarter
        )

        monthly_data = {}
        for offering in tithe_offering:
            month = offering.sabbath_week.month
            if month not in monthly_data:
                monthly_data[month] = []
            monthly_data[month].append(offering)

        context = {
            'member': member,
            'monthly_data': monthly_data,
            'active_quarter': active_quarter,
            'active_week':active_week,
            'active_week_month':active_week_month,
            'active_quarter':active_quarter,
        }

        
        return render(request, 'reports/member_tithe_offering_report_template.html', context)
    


# church user report 
# ========================================================================================================== 
    
@login_required
def church_income_expense_report(request):
    user_context = getGlobalContext(request.user)
    active_week= user_context.get('active_week')
    active_quarter = user_context.get('active_quarter')  
    active_week_month = active_week.month if active_week else None
    church = user_context.get('associated_church')
    context = {}  # Initialize an empty context dictionary

    if request.user.role in ['Church_secretary', 'Church_treasurer']:
        form = MonthForm(request.POST or None)

        if request.method == 'POST' and form.is_valid():
            month = form.cleaned_data['month']
            sabbaths = Sabbath.objects.filter(month=month)

            church_income = ChurchIncome.objects.filter(church=church, sabbath__in=sabbaths)
            church_expense = ChurchExpense.objects.filter(church=church, sabbath__in=sabbaths)

            context = {
                'church': church,
                'month': month,
                'church_income': church_income,
                'church_expense': church_expense,
                'active_week':active_week,
                'active_week_month':active_week_month,
                'active_quarter':active_quarter,
            }

    else:
        form = MonthForm()  # Instantiate the form for GET requests

    context['form'] = form  # Add the form to the context dictionary

    return render(request, 'reports/church_report_template.html', context)



def church_trustfund_report(request):
        user_context = getGlobalContext(request.user)
        active_week= user_context.get('active_week')
        active_quarter = user_context.get('active_quarter')  
        active_week_month = active_week.month if active_week else None

        church = user_context.get('associated_church')
        context = {}
        if request.user.role in ['Church_secretary', 'Church_treasurer']:
           form = MonthForm(request.POST or None)

           if request.method == 'POST' and form.is_valid():
           
                month = form.cleaned_data['month']

                sabbaths = Sabbath.objects.filter(month=month)

                church_trustfunds = TrustFund.objects.filter(church=church, sabbath_week__in=sabbaths)
        
                context = {
                   'church':church,
                   'month':month,
                   'church_trustfunds': church_trustfunds,
                    'active_week':active_week,
                    'active_week_month':active_week_month,
                    'active_quarter':active_quarter,
                
                 }
        else:
            form = MonthForm()  # Instantiate the form for GET requests

        context['form'] = form  # Add the form to the context dictionary

        return render(request, 'reports/report_trustfund_template.html', context)
    


@login_required
def member_tithe_offering_report(request, member_id):
    user_context = getGlobalContext(request.user)
    active_week= user_context.get('active_week')
    active_quarter = user_context.get('active_quarter')  
    active_week_month = active_week.month if active_week else None

    if request.user.role in ['Church_secretary', 'Church_treasurer']:

        member = Member.objects.get(member_id=member_id)
        
        active_quarter = Quarter.objects.get(is_active=True)
        tithe_offering = TitheOffering.objects.filter(
            church_member=member,
            sabbath_week__month__quarter=active_quarter
        )

        monthly_data = {}
        for offering in tithe_offering:
            month = offering.sabbath_week.month
            if month not in monthly_data:
                monthly_data[month] = []
            monthly_data[month].append(offering)

        context = {
            'member': member,
            'monthly_data': monthly_data,
            'active_quarter': active_quarter,      
            'active_week':active_week,
            'active_week_month':active_week_month,
        
        }

        
        return render(request, 'reports/member_tithe_offering_report_template.html', context)



        # district report 
    # ==================================================================================================



# @login_required
# def district_trustfund_report(request):
#     user_context = getGlobalContext(request.user)
#     district = user_context.get('associated_district')
#     context = {}

#     if request.user.role in ['District_treasurer', 'District_secretary']:
#         form = MonthForm(request.POST or None)

#         if request.method == 'POST' and form.is_valid():
#             month = form.cleaned_data['month']
#             sabbaths = Sabbath.objects.filter(month=month)

#             # Get trust funds for all churches in the district for the specified month
#             trust_funds = {}
#             total_amount_due_district = 0
            
#             # Iterate through all churches in the district
#             for church in Church.objects.filter(district=district):
#                 # Calculate the total amount due for the church for the specified month
#                 amount_due_district = CombinedOffering.objects.filter(
#                     associated_church=church,
#                     sabbath_week__in=sabbaths
#                 ).aggregate(total_amount_due=Sum('amount_due_district'))['total_amount_due'] or 0

#                 # Add church trust fund data to the trust_funds dictionary
#                 trust_funds[church.church_name] = {
#                     'amount_due_district': amount_due_district
#                 }
                
#                 # Update the total amount due for the district
#                 total_amount_due_district += amount_due_district

    

#             context = {
#                 'district': district,
#                 'month': month,
#                 'trust_funds': trust_funds,
#                 'total_amount_due_district': total_amount_due_district,
#             }
#     else:
#         form = MonthForm()  # Instantiate the form for GET requests

#     context['form'] = form  # Add the form to the context dictionary

#     return render(request, 'reports/user_district_trustfund_template.html', context)



@login_required
def district_trustfund_report(request):
    user_context = getGlobalContext(request.user)
     
    active_week= user_context.get('active_week')
    active_quarter = user_context.get('active_quarter')  
    active_week_month = active_week.month if active_week else None

    district = user_context.get('associated_district')
    context = {}
    
    if request.user.role in ['District_treasurer', 'District_secretary']:
        form = MonthForm(request.POST or None)

        if request.method == 'POST' and form.is_valid():
           
            month = form.cleaned_data['month']

            # Query CombinedOffering for the selected district and month
            combined_offerings = CombinedOffering.objects.filter(
                associated_church__district=district,
                sabbath_week__month=month
            )

            # Preprocess data to group by week and church
            data = {}
            for offering in combined_offerings:
                week = offering.sabbath_week.sabbath_alias
                church = offering.associated_church
                if week not in data:
                    data[week] = {
                        'total_amount_due_district': 0,
                        'churches': {}
                    }
                if church not in data[week]['churches']:
                    data[week]['churches'][church] = {
                        'church_name': church.church_name,
                        'amount_due_district': 0
                    }
                data[week]['churches'][church]['amount_due_district'] += offering.amount_due_district
                data[week]['total_amount_due_district'] += offering.amount_due_district

            context = {
                'district': district,
                'month': month,
                'data': data,
                'active_week':active_week,
                'active_week_month':active_week_month,
                'active_quarter':active_quarter,
            }
    return render(request, 'reports/district_trustfund_template.html', context)