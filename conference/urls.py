from django.urls import path
from .import views


app_name = "conference"


urlpatterns = [
     path('ad_usr_actions/', views.take_action, name="take_action"),
]
