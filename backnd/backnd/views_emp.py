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

# Employee dashboard 
@login_required
def EmployeeDashboard(request):
    if request.user.is_superuser:
        return HttpResponse("<h1>Not a valid user to access this page.!</h1>")
    else:
        lead = LeadModel.objects.all().order_by('-id') # lead model object

        # post for data searching propose
        if request.method == 'POST':
            search = request.POST['search'].strip()  # strip for remove space from both of sides

            # according to input data is filtering 
            lead = LeadModel.objects.filter(Q(lead_id__icontains = search) | Q(first_name__icontains = search) | Q(email_id__icontains = search) | Q(primary_phone__icontains = search))
            

        # all data sent on html file in object format 
        data = {
            'lead_list': lead
        }
    return render(request,'employee/dashboard.html',data)











