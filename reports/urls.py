from django.urls import path
from .import views

app_name='reports'

urlpatterns = [
    path('admin_reports',views.admin_reports, name ="admin_reports"),
    path('church_trustfund_report',views.church_trustfund_report, name ="church_trustfund_report"),
]