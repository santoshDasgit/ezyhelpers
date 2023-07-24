from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from app.models import *
from django.db.models import Q


# Dashboard or home of a superuser 
@login_required
def SuperUserDashBoard(request):
    if not request.user.is_superuser:
        return HttpResponse("<h1>Not a valid user to access this page.!</h1>")
    else:
        helper = HelperModel.objects.all().order_by('-id') # helper model object

        # post for data searching propose
        if request.method == 'POST':
            search = request.POST['search'].strip() # strip for remove space from both of sides

            # according to input data is filtering 
            helper = HelperModel.objects.filter(Q(helper_id__icontains = search) | Q(first_name__icontains = search) | Q(email_id__icontains = search) | Q(primary_phone__icontains = search))
            

        # all data sent on html file in object format 
        data = {
            'helper_list': helper
        }
        return render(request,"super/dashboard.html",data)




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
    if val:
        return val


# New user create 
@login_required
def UserCreationView(request):
    # if you are not a superuser 
    if not request.user.is_superuser:
        return HttpResponse("<h1>Not a valid user to access this page!</h1>")
    
    if request.method == "POST":
        # all input value get 
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['psw']

        # if password correct 
        if(password_check(password,request)):

            # user  exists or not check 
            if User.objects.filter(username = email).exists():
                messages.warning(request,f"{email} already exists.!")
            else:
                # User model data inserted 
                user = User(
                    username = email,
                    email=email,
                    first_name = first_name,
                    last_name=last_name,
                     
                     )
                try:
                    # email send Logic 
                    subject = "Welcome to the EzyHelpers team!!"
                    message = f'email : <b>{email}</b> <br> password : <b>{password}</b>'
                    from_email = settings.EMAIL_HOST_USER
                    to = email
                    email_box = EmailMultiAlternatives(subject,message,from_email,[to])
                    email_box.content_subtype='html'
                    email_box.send()

                    # user setpassword & save 
                    user.set_password(password)
                    user.save()

                    # show message to superuser
                    messages.success(request,f"{email} user created successful.!")
                except:
                    messages.error(request,'something error happen try again.!')
    return render(request,'super/user_creation_fm.html')


# all user detail 
@login_required
def UserListViews(request):
    # if you are not a superuser 
    if not request.user.is_superuser:
        return HttpResponse("<h1>Not a valid user to access this page!</h1>")
    user = User.objects.all()
    data = {
        'user':user
    }
    return render(request,'super/user_list.html',data)
                

# user details update 
@login_required
def userUpdate(request,id):
    if not request.user.is_superuser:
        return HttpResponse("<h1>Not a valid user to access this page!</h1>")
    
    if request.method == "POST":

        # all input value get 
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # user object get 
        user = User.objects.get(pk = id)

        try:
            # if same name of email is already exists 
            if(User.objects.filter(email = email).exists() and user.email != email):
            
                messages.error(request,f"{email} already exists try another email.!")
            else:
                # email send Logic 
                subject = "user data updated!!"
                message = f'email : <b>{email}</b> <br> first name : <b>{first_name}</b> <br> last name : <b>{last_name}</b>'
                from_email = settings.EMAIL_HOST_USER
                to = email
                email_box = EmailMultiAlternatives(subject,message,from_email,[to])
                email_box.content_subtype='html'
                email_box.send()

                # user data updated 
                user.first_name = first_name
                user.username = email
                user.email = email
                user.last_name  = last_name
                user.save()
                messages.success(request,"User update successful..!")
        except:
            messages.error(request,"Something error happen try again!")

    
    data = {
        'user':User.objects.get(pk = id)
    }
    return render(request,'super/user_update.html',data)


# user delete logic 
@login_required
def userDelete(request,id):
    if not request.user.is_superuser:
        return HttpResponse("<h1>Not a valid user to access this page!</h1>")
    
    User.objects.get(pk = id).delete()
    messages.success(request,"Remove user successfully")

    return redirect('superuser_user_list')



