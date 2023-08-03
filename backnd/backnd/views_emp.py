from django.shortcuts import render,HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from app.models import *
from django.db.models import Q
from django.utils import timezone

# Employee dashboard 
@login_required
def EmployeeDashboard(request):
    if request.user.is_superuser:
        return HttpResponse("<h1>Not a valid user to access this page.!</h1>")
    else:
        # Get the current date and time as a datetime object
        current_datetime = timezone.now()

        # Calculate the threshold date (current date and time minus 24 hours)
        threshold_datetime = current_datetime - timezone.timedelta(hours=24)
        notify = LeadStatusNotificationModel.objects.filter(date__lt = threshold_datetime)    
        # all data sent on html file in object format 
        data = {
            'notify': notify
        }
    return render(request,'employee/dashboard.html',data)