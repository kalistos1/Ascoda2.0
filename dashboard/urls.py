from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
   path('church/user_ad_dash_tre_sec/analytics/', views.church_dashboard, name="church_dashboard"),
   path('district/user_ad_dash/analytics/', views.district_dashboard, name="district_dashboard"),
   path('conference/admin/', views.conference_dashboard, name="conference_dashboard"),
   path('profile/', views.profile, name="profile"),
   path('conference/admin/users_overview/', views.users_overview, name="users_overview"),
   path('conference/admin/set_up/delete_month/<int:month_id>', views.delete_month, name="delete_month"),
   path('conference/admin/set_up/delete_sabbath/<int:sabbath_id>', views.delete_sabbath, name="delete_sabbath"),
   path('conference/admin/set_up/delete_quarter/<int:quarter_id>', views.delete_quarter, name="delete_quarter"),
   path('conference/admin/create_new_church/', views.churches, name="create_church"),
   path('conference/admin/create_new_district/', views.districts, name="create_district"),
   path('conference/admin/church_list/', views.all_church, name="all_churches"),
   path('conference/admin/district_list/', views.all_districts, name="all_districts"),
   path('conference/admin/district_list/view_district/<int:district_id>', views.admin_view_district, name="view_district"),
   path('conference/admin/church_list/view_church/<int:church_id>', views.admin_view_church, name="view_church"),
   path('admin/church_list/view_user/<int:member_id>', views.view_member, name="view_member"),
   path('conference/admin/acct_officers_list/', views.all_officers, name="all_officers"),
   path('conference/admin/church_members_list/', views.all_members, name="all_members"),
   path('conference/admin_add_user/', views.add_user, name="add_user"),
   path('conference/admin_add_user/process_user/',views.process_add_officer_form, name="process_add_officer_form"),
   path('conference/admin_setup_acct/', views.setup_accounting, name="setup_accounting"),
   path('conference/admin_setup_acct/quaters/', views.add_quarter, name="add_quarter"),
   path('conference/admin_setup_acct/quaters/activate/<int:quarter_id>/', views.activate_quarter, name="activate_quarter"),
   path('conference/admin_setup_acct/sabbath/activate/<int:sabbath_id>/', views.activate_sabbath, name="activate_sabbath"),
   path('conference/admin_setup_acct/month/', views.add_month, name="add_month"),
   path('conference/admin_setup_acct/sabbath/', views.add_sabbath, name="add_sabbath"),
   path('conference/admin_setup_acct/assign_officer/', views.assign_officer, name ="assign_officer"),
   path('conference/admin/church_list/church/accounting_details/<int:church_id>', views.admin_view_church_account_detail, name ="view_church_acct") ,
   path('conference/admin/trustfund/details/', views.view_trustfunds, name ="view_trustfunds") ,


]
