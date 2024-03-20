from django.urls import path
from .import views

app_name='reports'

urlpatterns = [
    path('admin_reports/',views.reports, name ="admin_reports"),
    path('church_income_expense_report/admin/',views.admin_church_income_expense_report, name ="church_income_expense_report"),
    path('church_trustfund_report/admin/',views.admin_church_trustfund_report, name ="church_trustfund_report"),
    path('district_trustfund_report/admin/',views.admin_district_trustfund_report, name ="district_trustfund_report"),
    path('member_tithe_offering_report/admin/<int:member_id>/',views.admin_member_tithe_offering_report, name ="member_tithe_offering_report"),
    path('church_income_expense_report/',views.church_income_expense_report, name ="user_church_income_expense_report"),
    path('church_trustfund_report/',views.church_trustfund_report, name ="user_church_trustfund_report"),
    path('member_tithe_offering_report/<int:member_id>/',views.member_tithe_offering_report, name ="church_member_tithe_offering_report"),
    path('district_trustfund_report/',views.district_trustfund_report, name ="user_district_trustfund_report"),
   
] 