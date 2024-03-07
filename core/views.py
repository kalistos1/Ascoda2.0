from django.shortcuts import render
from accounts.forms import LoginForm
from django.contrib import messages
# Create your views here.


# index view

def index(request):
    form = LoginForm()
    context = {
     'form':form,
    }
    return render(request, 'pages/index.html', context)