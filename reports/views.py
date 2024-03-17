from django.shortcuts import render
from .forms import *
from accounts.models import *
from accounting.models import *
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def admin_reports(request):
    if request.user.role == "Admin":
        form1 =  IncomeExpenseReportForm()
        form2= DistrictTrustfundForm()

        context = {
            'form1':form1,
            'form2':form2,
        }
        return render(request, 'reports/church_reports.html',context)



@login_required
def church_income_expense_report(request):
    if request.user.role == "Admin":
        form = IncomeExpenseReportForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            church = form.cleaned_data['church']
            month = form.cleaned_data['month']

            # Query the Sabbath instances for the selected month
            sabbaths = Sabbath.objects.filter(month=month)

            # Query ChurchIncome and ChurchExpense for the selected church and sabbaths
            church_income = ChurchIncome.objects.filter(church=church, sabbath__in=sabbaths)
            church_expense = ChurchExpense.objects.filter(church=church, sabbath__in=sabbaths)
        

            context = {
                'church':church,
                'month':month,
                'church_income': church_income,
                'church_expense': church_expense,
            }
        return render(request, 'reports/report_template.html', context)



def church_trustfund_report(request):
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
                
            }
        return render(request, 'reports/report_trustfund_template.html', context)



@login_required
def district_trustfund_report(request):
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
                'data': data
            }
            return render(request, 'reports/district_trustfund_template.html', context)



@login_required
def  member_tithe_offering_report(request, member_id):
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
        }

        
        return render(request, 'reports/member_tithe_offering_report_template.html', context)