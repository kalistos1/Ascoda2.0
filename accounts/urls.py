from django.urls import path
from .import views


app_name = "account"

urlpatterns = [
    path('', views.signin, name ='signin'),
    path('logout/', views.signout, name ='signout'),
]
