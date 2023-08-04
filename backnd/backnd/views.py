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
from app.resources import HelperModelResources
from tablib import Dataset
import gspread
from django.db.models import Q

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
            username = request.POST["username"].strip()
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
                    messages.error(request,"Invalid password!")
            else:
                # if username does'not exists 
                messages.error(request,"Invalid email address!")
    else:
        return redirect("home")
    return render(request,'login.html')
                



# Logout function
@login_required 
def LogoutView(request):
    logout(request)
    messages.success(request,"Logout success!")
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
            messages.error(request,f"{email} already exists try another email!")
        else:
            url =f'http://{url}/profile_update/{id}/{email}'
            subject = "user data updated url!!"
            message = f'url link : {url}'
            from_email = settings.EMAIL_HOST_USER
            to = email
            email_box = EmailMultiAlternatives(subject,message,from_email,[to])
            email_box.content_subtype='html'
            email_box.send()
            messages.success(request,'check url on your email to update the data!')
       

    return render(request,"email_validate.html")
        
            

# Profile update 
def ProfileUpdateView(request,id,email):
    # if user is not login 
    if not request.user.is_authenticated:
        messages.warning(request,'at the time of profile update Login mandatory!')
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
            
            messages.error(request,f"{email} already exists try another email!")
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
                messages.success(request,"Profile update successful!")
            except:
                messages.error("There is an error please try again!")

            # page redirect with same page 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request,'profile_update.html',{'email':email})


# Function to validate the password
def password_check(passwd,request):
     
    SpecialSym =['$', '@', '#', '%','!','&','*','^']
    val = True
     
    if len(passwd) <= 8:
        messages.error(request,'length should be at least 8!')
        val = False
         
    if not any(char.isdigit() for char in passwd):
        messages.error(request,'Password should have at least one numeral!')
        val = False
         
    if not any(char.isupper() for char in passwd):
        messages.error(request,'Password should have at least one uppercase letter!')
        val = False
         
    if not any(char.islower() for char in passwd):
        messages.error(request,'Password should have at least one lowercase letter!')
        val = False
         
    if not any(char in SpecialSym for char in passwd):
        messages.error(request,'Password should have at least one of the symbols $@#!')
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
                    messages.success(request,'password changed successful!')

                     # page redirect with same page 
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    
                else:
                    messages.error(request,"conform password doesn't match!")
            else:
                messages.error(request,'old password is incorrect!')
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



# Dashboard or home of a superuser 
@login_required
def HelperListViews(request):

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
    return render(request,"helper_list.html",data)


# Helper data inserted
@login_required
def HelperAddView(request):
    fm = HelperForm()

    if request.method == "POST":
        
        # data input 
        language = request.POST.getlist('language')
        additional_skill = request.POST.getlist('ad-skill')
        skill = request.POST.getlist('skill')

        # language required condition 
        if language == ['']:
            messages.error(request,'* Preferred Language required!')
        else: 
            fm = HelperForm(request.POST)
            if fm.is_valid():
                data = fm.save()
                data.helper_id = generate_id(data.id) # function to create id and convert into Hexa
                data.save()
                messages.success(request,'data added successfully!')

                # preferences language inserted
                for i in language:
                    if i!='':
                        HelperPreferredLanguageModel(helper = data,language=i).save()
                
                # additional_skill inserted
                for i in additional_skill:
                    if i !='':
                        HelperAdditionalSkillSetModel(helper = data,additional_skill=i).save()

                # skill inserted
                for i in skill:
                    if i !='':
                        HelperSkillSetModel(helper = data,skill=i).save()
            else:
                messages.error(request,'please enter the valid data!')

    data = {
        'fm':fm,
    }
    return render(request,'helper_add.html',data)

                


# helper all details showing 
@login_required
def HelperDetailsView(request,id):
    helper = HelperModel.objects.get(id = id)
    data = {
      'helper':helper,
      'language':HelperPreferredLanguageModel.objects.filter(helper = helper),
       'skill':HelperSkillSetModel.objects.filter(helper = helper),
      'additional_skill':HelperAdditionalSkillSetModel.objects.filter(helper=helper)
    }
    return render(request,'helper_view.html',data)


# Helper status update logic 
@login_required
def HelperStatusUpdateView(request,id):
    if request.method == 'POST':
        helper_status_inp = request.POST['helper-status-inp']
        helper = HelperModel.objects.get(id = id)
        helper.helper_status = helper_status_inp
        helper.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# excel file through helper create 
@login_required
def ExcelFileHelperFileView(request):
    if request.method == 'POST':
        helper_resources = HelperModelResources()
        data_set = Dataset()
        myfile = request.FILES['myfile']

        # check excel file or not!
        if not myfile.name.endswith('xlsx'):
            messages.error(request,'Excel file only allow!')

            # redirect with same page 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                 # all excel data store in 'excel_data' in form of table 
                excel_data =data_set.load(myfile.read(),format='xlsx')
                for i in excel_data:
                    # row fully empty or not check
                    if((i[0]==None or i[0]=='') and (i[1]==None or i[1]=='') and (i[2]==None or i[2]=='') and (i[3]==None or i[3]=='') ):
                         pass
                    else:
                        helper = HelperModel(
                            first_name = i[0] or "not mention",
                            last_name = 'NULL',
                            primary_phone = int(i[1] or 0),
                            email_id = i[2],
                            street = 'NULL STREET',
                            city = i[3],
                            zipcode = 7540065,
                            state = "NULL STATE",
                            country = 'NULL COUNTRY'

                        )

                        helper.save()
                        helper.helper_id = generate_id(helper.pk) # helper id generate and store it 
                        helper.save()
                       

                # if all right then success message 
                messages.success(request,'file upload successful!')
            except:
                # exception handle 
                messages.error(request,'There is an error!')
            # redirect with same page 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    return render(request,'helper_excel.html')


# helper object delete 
@login_required
def HelperDeleteView(request,id):
    HelperModel.objects.get(id = id).delete()
    messages.warning(request,"Data remove successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# helper object update 
@login_required
def HelperEditView(request,id):

    # all model object get as of our requirement 
    helper = HelperModel.objects.get(id = id) 
    helper_skill = HelperSkillSetModel.objects.filter(helper = helper)
    helper_additional_skill = HelperAdditionalSkillSetModel.objects.filter(helper = helper)
    helper_language = HelperPreferredLanguageModel.objects.filter(helper = helper)
    
    fm = HelperForm(instance=helper) # form 

    if request.method == "POST":  
        # all additional input get 
        skill_inp = request.POST.getlist('skill')
        add_skill_inp = request.POST.getlist('ad-skill')
        language_inp = request.POST.getlist('language')

        fm=HelperForm(request.POST,instance=helper) # all input value 
        
        # language empty or not check 
        language_inpIsEmpty = False
        for i in language_inp:
            if i.strip()!="":
                language_inpIsEmpty  = True
                break
        
        # if language all are empty under the code not executed
        if(not language_inpIsEmpty):
            messages.error(request,"language must mandatory!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if fm.is_valid():

            # all additional data remove
            helper_skill.delete()
            helper_additional_skill.delete()
            helper_language.delete()

            #  --------update again------- 

            # skill update
            for i in skill_inp:
                if i.strip()!="":
                    HelperSkillSetModel(helper = helper , skill = i.strip()).save()
            
            # additional skill update 
            for i in add_skill_inp:
                if i.strip() != "":
                    HelperAdditionalSkillSetModel(helper = helper ,additional_skill = i.strip()).save()
            
            # language update 
            for i in language_inp:
                if i.strip()!="":
                    HelperPreferredLanguageModel(helper = helper , language = i.strip()).save()

            # Helper form save  
            fm.save()
            messages.success(request,'Data updated successfully!')
        else:
            messages.error(request,'please enter valid data!')

    data = {
        'fm':fm,
        'skill': helper_skill,
        'additional_skill':helper_additional_skill,
        'helper_language':helper_language
    }
    return render(request,'helper_edit.html',data)



def lead_generate_id(id):
    # Generate a random number
    random_num = str(id+1000000000).encode()

    # Generate a SHA-256 hash of the random number.
    hash_obj = hashlib.sha256(random_num)
    hex_digit = hash_obj.hexdigest()
    return hex_digit[:10]

# lead logic on the basics of google sheet 
@login_required
def LeadList(request):
    all_value = ''
    try:
        # configuration json file 
        gc = gspread.service_account(filename = "app\\testsample-393218-c2720cf831ca.json")

        # open google sheet by help of key
        worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
    
        # which sheet you want to open! 
        current_sheet = worksheet.worksheet('Sheet1')

        # Data get dictionary format 
        all_value = current_sheet.get_all_records()
    except:
        # exception handle 
        messages.error(request,'Something error try again! may be network issue!')
    
    data = {
        'data':all_value,
        'length':len(all_value)
    }
    return render(request,'lead_list.html',data)   


# lead details show 
@login_required
def LeadDetailsView(request,no):
    data = {}
    try:
        # configuration json file 
        gc = gspread.service_account(filename = "app\\testsample-393218-c2720cf831ca.json")

        # open google sheet by help of key
        worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
        
        # which sheet you want to open! 
        current_sheet = worksheet.worksheet('Sheet1')
        
        # all row data
        row_num = int(no)+1
        values_list = current_sheet.row_values(row_num)
        data = {
            'name' : values_list[0],
            'phone' : values_list[1],
            'email' : values_list[2],
            'addr' : values_list[3],
            'id': values_list[8]
        }
    except:
         # exception handle 
        messages.error(request,'Something error try again! may be network issue!')

    return render(request,'lead_details.html',data)  


# update the lead 
@login_required
def LeadEditView(request,no):
    data = {}
    try:
           # configuration json file 
        gc = gspread.service_account(filename = "app\\testsample-393218-c2720cf831ca.json")

        # open google sheet by help of key
        worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
        
        # which sheet you want to open! 
        current_sheet = worksheet.worksheet('Sheet1')
        
        # all row data
        row_num = int(no)+1
        values_list = current_sheet.row_values(row_num)

        data = {
            'name' : values_list[0],
            'phone' : values_list[1],
            'email' : values_list[2],
            'addr' : values_list[3],
        }
        
    
        # POST
        if request.method == "POST":

            # all value get by input in lead_edit.html
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            addr = request.POST['addr']

            # values set/update in sheets 
            current_sheet.update_cell(row_num, 1, name)
            current_sheet.update_cell(row_num, 2, phone)
            current_sheet.update_cell(row_num, 3, email)
            current_sheet.update_cell(row_num, 4, addr)
            

            # message to success
            messages.success(request,'Data updated successful!')

            # redirect with same page 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     
    except:
         # exception handle 
        messages.error(request,'Something error try again! may be network issue!')
    return render(request,'lead_edit.html',data)
     

# delete data from sheet 
@login_required
def LeadDeleteView(request,no):
    try:
        # configuration json file 
        gc = gspread.service_account(filename = "app\\testsample-393218-c2720cf831ca.json")

        # open google sheet by help of key
        worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
        
        # which sheet you want to open! 
        current_sheet = worksheet.worksheet('Sheet1')
        
        # all row data
        row_num = int(no)+1

        # delete the row by help of row num 
        current_sheet.delete_row(row_num)

        # success message 
        messages.success(request,'data remove successful!')
    except:
         # exception handle 
        messages.error('Data not to be deleted something error try again!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# data insert into lead sheet 
@login_required
def LeadInsertDataView(request):
    if request.method == 'POST':
        try:
            # configuration json file 
            gc = gspread.service_account(filename = "app\\testsample-393218-c2720cf831ca.json")

            # open google sheet by help of key
            worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
            
            # which sheet you want to open! 
            current_sheet = worksheet.worksheet('Sheet1')
            
            
            
            

            # value get from lead_add.html
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            addr = request.POST['addr']
            id = lead_generate_id(len(current_sheet.get_all_records())+2)

            # all value in list format 
            lst = [name,phone,email,addr," "," "," ","pending",id]

            # row append in sheet 
            current_sheet.append_row(lst)

            # notification 
            lead = id
            employee = request.user
            msg = "pending message"
            status = "pending"
            LeadStatusNotificationModel(
                lead = lead,
                employee = employee,
                status = status,
                msg = msg
            ).save()

            messages.success(request,"Data add successful!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            # exception handle 
            messages.error(request,'Something error try again! may be network issue!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request,'lead_add.html')

@login_required
def LeadStatusUpdateView(request,row):
    row = int(row)+1
    col = 8
    try:
        # configuration json file 
        gc = gspread.service_account(filename = "app\\testsample-393218-c2720cf831ca.json")

        # open google sheet by help of key
        worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
            
        # which sheet you want to open! 
        current_sheet = worksheet.worksheet('Sheet1')
        
        lead_status_inp = request.POST['lead_status_inp']

        # update status 
        current_sheet.update_cell(row,col,lead_status_inp)

        messages.success(request,"Data update successful.!")
    except:
        # exception handle 
        messages.error(request,'Something error try again! may be network issue!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))








      

       

       

        







