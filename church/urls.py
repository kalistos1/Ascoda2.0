from django.urls import path
from . import views
from dashboard.views import upload_tithe_offering, upload_members

app_name = "church"

urlpatterns =[
    path('add_new_member/', views.add_new_member, name="add_new_member"),
    path('delete_member/<int:pk>/', views.delete_member, name="delete_member"),
    path('tithe_offering/', views.tithe_offering, name="tithe_offering"),
    path('add_tithe_offering/<int:member_id>/', views.add_tithe_offering, name="add_tithe_offering"),
    path('church_income/', views.add_church_income, name="church_income"),
    path('church_expenses/', views.church_expense, name="church_expenses"),
    path('cash_accounts/', views.church_cash_account, name="cash_account"),
    path('trustfunds/', views.view_trust_fund, name="trustfund"),
    path('cal_trustfunds/', views.update_trust_fund, name="cal_trustfund"),
    path('upload_tithe_offering/', upload_tithe_offering, name='upload_tithe_offering'),
    path('upload_members/', upload_members, name='upload_members'),
    path('calculate_combined_offering/', views.calculate_combined_offering, name='calculate_combined_offering'),


]
