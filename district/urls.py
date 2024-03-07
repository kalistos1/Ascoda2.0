from django.urls import path
from . import views

app_name ="district"

urlpatterns =[
    path('district_income/', views.district_income, name="district_income"),
    path('district_expense/', views.district_expense, name="district_expense"),
    

]