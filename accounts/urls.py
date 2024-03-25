from django.urls import path
from .import views


app_name = "account"

urlpatterns = [
    path('', views.signin, name ='signin'),
    path('logout/', views.signout, name ='signout'),
    path ('user_profile_information/', views.edit_user_info, name='edit_user_info'),
    path ('user_profile/change_password/', views.change_password, name='change_password'),
    path ('user_profile/change_email/', views.change_email, name='change_email'),
    path ('user_profile/update_user_profile', views.update_profile_info, name='update_profile_info'),
]
