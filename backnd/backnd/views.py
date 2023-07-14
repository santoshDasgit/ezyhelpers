from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpRequest
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
import random
from app.form import *
import hashlib
import random

# Home page 
def HomeView(request):

    if request.user.is_authenticated: # check user login or not
        # If user superuser 
        if request.user.is_superuser:
            return redirect("super_user_dashboard")
        else:
            return redirect("employee_dashboard")
    else:
        return redirect('login')


# Login page 
def LoginView(request):
    # if user not login 
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            

            # Check user exists or not 
            if(User.objects.filter(username = username).exists()):
                user =  authenticate(username = username,password =password)
                # if user and password is correct 
                if user is not None:
                    login(request ,user)
                    # messages.success(request,f"Welcome {username}..!")
                    return redirect("home") # if all are correct redirect to home
                else:
                    # if password invalid
                    messages.error(request,"Invalid password")
            else:
                # if username does'not exists 
                messages.error(request,"Invalid email address.")
    else:
        return redirect("home")
    return render(request,'login.html')
                



# Logout function
@login_required 
def LogoutView(request):
    logout(request)
    messages.success(request,"Logout success.!")
    return redirect('/')


# profile details 
@login_required
def ProfileView(request,id):
    return render(request,'profile.html')

# email verify from profile update
@login_required
def EmailVerifyProfileView(request,id,url):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.get(pk = id)
        if(User.objects.filter(email = email).exists() and user.email != email):
            messages.error(request,f"{email} already exists try another email.!")
        else:
            url =f'http://{url}/profile_update/{id}/{email}'
            subject = "user data updated url!!"
            message = f'url link : {url}'
            from_email = settings.EMAIL_HOST_USER
            to = email
            email_box = EmailMultiAlternatives(subject,message,from_email,[to])
            email_box.content_subtype='html'
            email_box.send()
            messages.success(request,'check url on your email to update the data.!')
       

    return render(request,"email_validate.html")
        
            

# Profile update 
def ProfileUpdateView(request,id,email):
    # if user is not login 
    if not request.user.is_authenticated:
        messages.warning(request,'at the time of profile update Login mandatory!!')
        return redirect('login')
        

    # if id doesn't match redirect to another page 
    if request.user.id != int(id):
        return HttpResponse("<h1>Not a valid user to access this page.!</h1>")
    
    # post 
    if request.method == 'POST':
        # all input value get 
        email = email
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # user model 
        user = User.objects.get(id = id)

        # if same name of email is already exists 
        if(User.objects.filter(email = email).exists() and user.email != email):
            
            messages.error(request,f"{email} already exists try another email.!")
        else:
            # try catch from network issue handle 
            try:
                # email send Logic 
                subject = "user data updated!!"
                message = f'email : <b>{email}</b> <br> first name : <b>{first_name}</b> <br> last name : <b>{last_name}</b>'
                from_email = settings.EMAIL_HOST_USER
                to = email
                email_box = EmailMultiAlternatives(subject,message,from_email,[to])
                email_box.content_subtype='html'
                email_box.send()
        
            
                # value configurations
                user.username = email
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # messages to update 
                messages.success(request,"Profile update successful.!")
            except:
                messages.error("Something error happen please try again!!")

            # page redirect with same page 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request,'profile_update.html',{'email':email})


# Function to validate the password
def password_check(passwd,request):
     
    SpecialSym =['$', '@', '#', '%','!','&','*','^']
    val = True
     
    if len(passwd) <= 8:
        messages.error(request,'length should be at least 8')
        val = False
         
    if not any(char.isdigit() for char in passwd):
        messages.error(request,'Password should have at least one numeral')
        val = False
         
    if not any(char.isupper() for char in passwd):
        messages.error(request,'Password should have at least one uppercase letter')
        val = False
         
    if not any(char.islower() for char in passwd):
        messages.error(request,'Password should have at least one lowercase letter')
        val = False
         
    if not any(char in SpecialSym for char in passwd):
        messages.error(request,'Password should have at least one of the symbols $@#')
        val = False
    if  ' ' in  passwd:
        messages.error(request,'Space not allow!')
        val = False
    if val:
        return val


# profile password changed 
@login_required
def PasswordChangedView(request):
    # user 
    user = User.objects.get(username = request.user)
    
    if request.method == "POST":

        # all data get from input 
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        conform_pass = request.POST['conform_password']

        # password format check 
        if password_check(new_password,request):
            # check old password correct or not 
            if user.check_password(old_password):
                # check conform password match 
                if(new_password == conform_pass):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request,user)

                    # message 
                    messages.success(request,'password changed successful!!')

                     # page redirect with same page 
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    
                else:
                    messages.error(request,"conform password doesn't match")
            else:
                messages.error(request,'old password is incorrect!!')
        else:
            pass

    return render(request,'password_change.html')

# unique id generated Hexadec
def generate_id(id):
    # Generate a random number
    random_num = str(id+1000000000).encode()

    # Generate a SHA-256 hash of the random number.
    hash_obj = hashlib.sha256(random_num)
    hex_digit = hash_obj.hexdigest()
    return hex_digit[:10]


# lead data inserted
@login_required
def LeadAdd(request):
    fm = LeadForm()

    if request.method == "POST":
        
        # data input 
        language = request.POST.getlist('language')
        additional_details = request.POST.getlist('ad')

        # language required condition 
        if language == ['']:
            messages.error(request,'* Preferred Language required')
        else:
            fm = LeadForm(request.POST)
            if fm.is_valid():
                data = fm.save()
                data.lead_id = generate_id(data.id) # function to create id and convert into Hexa
                data.save()
                messages.success(request,'data added successful..!')

                # preferences language inserted
                for i in language:
                    LeadPreferredLanguageModel(lead = data,language=i).save()
                
                # additional_details inserted
                for i in additional_details:
                    LeadAdditionalDetailsModel(lead = data,additional_details=i).save()

                
            else:
                messages.error(request,'please enter the valid data')
    data = {
        'fm':fm,
    }
    return render(request,'lead_add.html',data)






