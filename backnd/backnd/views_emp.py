from django.shortcuts import render,HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from app.models import *

# Employee dashboard 
@login_required
def EmployeeDashboard(request):
    data = {
            'lead_list': LeadModel.objects.all() # lead model object
        }
    return render(request,'employee/dashboard.html',data)