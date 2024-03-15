from django.shortcuts import render

# Create your views here.
def admin_reports(request):
    return render(request, 'reports/church_reports.html')


def church_trustfund_report(request):
    return render(request, 'reports/report_template.html')