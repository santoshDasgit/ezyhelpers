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
from datetime import date
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from app.models import LeadModel,Localities



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

    helper = HelperModel.objects.filter(phone_valid = False).order_by('-id') # helper model object

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

    # location value get in Gspreed 
    location_values = ''
    try:
        # configuration json file 
        # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

        # # open google sheet by help of key
        # worksheet = gc.open_by_key('1XvBPqKzz3fl0qWODP6gIYjTI03_17Ul8pqGGe2RSg9c')
    
        # # which sheet you want to open! 
        # current_sheet = worksheet.worksheet('Sheet1')

        # # Data get dictionary format 
        # location_values = current_sheet.get_all_records()
        location_values = Localities.objects.all()
    except:
        # exception handle 
        messages.error(request,'Something error try again! may be network issue!')


    fm = HelperForm()
    if request.method == "POST":
        
        # data input 
        language = request.POST.getlist('language')
        additional_skill = request.POST.getlist('ad-skill')
        skill = request.POST.getlist('skill')
        job_role = request.POST.getlist('job_role')

        # language required condition 
        if language == ['']:
            messages.error(request,'* Preferred Language required!')
        else: 
            fm = HelperForm(request.POST,request.FILES)
            if fm.is_valid():
                # phone number exist or not valid (phone_valid)

                # if secondary phone empty 
                if fm.instance.secondary_phone != None and HelperModel.objects.filter(Q(primary_phone = fm.instance.primary_phone) | Q(secondary_phone = fm.instance.secondary_phone) | Q(primary_phone = fm.instance.secondary_phone) | Q(secondary_phone = fm.instance.primary_phone)).exists():
                    fm.instance.phone_valid = True
                    messages.warning(request,'Redundant phone number , please check in dashboard ! ')

                # if secondary phone not empty 
                if fm.instance.secondary_phone == None and HelperModel.objects.filter(Q(primary_phone = fm.instance.primary_phone) | Q(secondary_phone = fm.instance.primary_phone)).exists():
                    fm.instance.phone_valid = True
                    messages.warning(request,'Redundant phone number , please check in dashboard ! ')
                    

                data = fm.save()
                data.helper_id = generate_id(data.id) # function to create id and convert into Hexa
                data.admin_user = request.user

                # first name and last name in upper case first char 
                data.first_name = data.first_name[0].upper() + data.first_name[1:]
                data.last_name = data.last_name[0].upper() + data.last_name[1:]

                # locality 
                data.locality = request.POST['locality']

                # helper_save 
                data.save()


                # History store 
                current_datetime = datetime.now()
                helper_history = HelperHistoryModel(
                    helper_id = data.helper_id,
                    first_name = data.first_name,
                    middle_name = data.middle_name,
                    last_name = data.last_name,
                    primary_phone = data.primary_phone,
                    email_id = data.email_id,
                    dob = data.dob,
                    create_date = current_datetime,

                    admin_user = request.user,
                    history_status = 'create'
                )
                helper_history.save()
                HistoryModel(
                    helper = helper_history,
                    date = current_datetime
                ).save()
                
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
                
                # job role
                for i in job_role:
                    if i !='':
                        HelperJobRoleModel(helper = data,job=i).save()
            else:
                messages.error(request,'please enter the valid data!')

    data = {
        'fm':fm,
        'locations':location_values
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
      'additional_skill':HelperAdditionalSkillSetModel.objects.filter(helper=helper),
      'job_role':HelperJobRoleModel.objects.filter(helper=helper),
    }
    return render(request,'helper_view.html',data)

# Helper all data into pdf 
def HelperPdfView(request,id):
    helper = HelperModel.objects.get(id = id)
    
    data = {
      'helper':helper,
      'language':HelperPreferredLanguageModel.objects.filter(helper = helper),
       'skill':HelperSkillSetModel.objects.filter(helper = helper),
      'additional_skill':HelperAdditionalSkillSetModel.objects.filter(helper=helper),
      'job_role':HelperJobRoleModel.objects.filter(helper=helper),
    }
    template = get_template('helper_pdf.html')
    context = data # Add any context data you need for the template
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{helper}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error while generating PDF', status=500)
    return response
    


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
                            country = 'NULL COUNTRY',
                            dob = '2021-2-12'

                        )

                        helper.save()
                        helper.helper_id = generate_id(helper.pk) # helper id generate and store it 
                        helper.save()
                       

                # if all right then success message 
                messages.success(request,'file upload successful!')
            except Exception as e:
                # exception handle 
                messages.error(request,f'There is an error!')
            # redirect with same page 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    return render(request,'helper_excel.html')

# excel file through lead create 
@login_required
def ExcelFileLeadFileView(request):
    if request.method == 'POST':
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
                    if((i[0]==None or i[0]=='') and (i[1]==None or i[1]=='') and (i[2]==None or i[2]=='') and (i[3]==None or i[3]=='') and (i[4]==None or i[4]=='') and (i[7]==None or i[7]=='') and (i[8]==None or i[8]=='') and (i[9]==None or i[9]=='') and (i[10]==None or i[10]=='')and (i[11]==None or i[11]=='')):
                         pass
                    else:
                        leads = LeadModel.objects.all()
                        id = lead_generate_id(len(leads)+2)
                        lead_data_all =LeadModel(
                            lead_id = i[8] or id,
                            name = i[0] or "not mention",
                            phone = i[1],
                            email_id = i[2],
                            address=i[3],
                            phone_valid_status=i[4],
                            agent=i[5] or "",
                            additional_comment=i[6] or "",

                            availability_status =i[11],
                            # locality 
                            locality =i[9],
                            near_by = i[10],
                            lead_status = i[7],
                            flat_number = i[12] or '',
                            lead_req_date = i[13] or None,
                            lead_placement_date = i[14] or None,
                            lead_status2 = i[15] or '',
                            role_on_demand_start_date = i[16] or None,
                            role_on_demand_start_from_time = i[17] or None,
                            role_on_demand_start_to_time = i[18] or None,
                            role_on_demand_end_date =i[19] or None,
                            role_on_demand_end_from_time =i[20] or None,
                            role_on_demand_end_to_time = i[21] or None,
                            lead_source = i[22] or '',
                            job_category=i[23] or '',
                            admin_user = request.user,
                        )
                        

                        lead_data_all.save()
                       
                       

                # if all right then success message 
                messages.success(request,'file upload successful!')
            except Exception as e:
                # exception handle 
                messages.error(request,f'There is an error! (Duplicate Entry)')
            # redirect with same page 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    return render(request,'lead_excel.html')

# excel file through helper create 
@login_required
def ExcelFileLocalityFileView(request):
    if request.method == 'POST':
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
                    if(i[0]==None or i[0]=='' ):
                         pass
                    else:
                        localities =Localities(
                            name = i[0]
                        )
                        localities.save()
                # if all right then success message 
                messages.success(request,'file upload successful!')
            except Exception as e:
                # exception handle 
                messages.error(request,f'There is an error! (Duplicate Entry)')
            # redirect with same page 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    return render(request,'locality_excel.html')
# helper delete 
@login_required
def HelperDeleteView(request,id):
    data = HelperModel.objects.get(id = id)

    current_datetime = datetime.now()
    helper_history = HelperHistoryModel(
                helper_id = data.helper_id,
                first_name = data.first_name,
                middle_name = data.middle_name,
                last_name = data.last_name,
                primary_phone = data.primary_phone,
                email_id = data.email_id,
                dob = data.dob,
                create_date = data.create_date,
                update_date = current_datetime.today(),
                admin_user = request.user,
                history_status = 'delete'
                )
    
    helper_history.save()
    HistoryModel(helper = helper_history , date = current_datetime.today()).save()
    data.delete()
    
    messages.warning(request,"Data remove successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# helper  update 
@login_required
def HelperEditView(request,id):

    # location value get in Gspreed 
    location_values = ''
    try:
        # configuration json file 
        # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

        # # open google sheet by help of key
        # worksheet = gc.open_by_key('1XvBPqKzz3fl0qWODP6gIYjTI03_17Ul8pqGGe2RSg9c')
    
        # # which sheet you want to open! 
        # current_sheet = worksheet.worksheet('Sheet1')

        # # Data get dictionary format 
        # location_values = current_sheet.get_all_records()
        location_values = Localities.objects.all()
    except:
        # exception handle 
        messages.error(request,'Something error try again! may be network issue!')
   
    # all model object get as of our requirement 
    helper = HelperModel.objects.get(id = id) 
    helper_skill = HelperSkillSetModel.objects.filter(helper = helper)
    helper_additional_skill = HelperAdditionalSkillSetModel.objects.filter(helper = helper)
    helper_language = HelperPreferredLanguageModel.objects.filter(helper = helper)
    job_role = HelperJobRoleModel.objects.filter(helper = helper)
    
    fm = HelperEditForm(instance=helper) # form 

    if request.method == "POST":  
        # all additional input get 
        skill_inp = request.POST.getlist('skill')
        add_skill_inp = request.POST.getlist('ad-skill')
        language_inp = request.POST.getlist('language')
        job_role_inp = request.POST.getlist('job_role')
        id_pdf = request.FILES.get('id_pdf')

        fm=HelperEditForm(request.POST,request.FILES,instance=helper) # all input value 
        
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
            job_role.delete()
     

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

            # language update 
            for i in job_role_inp:
                if i.strip()!="":
                    HelperJobRoleModel(helper = helper , job = i.strip()).save()

            # update_date is updated 
            fm.instance.update_date = date.today()

            
            # pdf upload logic 
            if (id_pdf is None or id_pdf is "") and (fm.instance.id_pdf is not None or fm.instance.id_pdf != ""):
                id_pdf = fm.instance.id_pdf
            
            # Helper form save
            data = fm.save()

            # first name and last name in upper case first char 
            data.first_name = data.first_name[0].upper() + data.first_name[1:]
            data.last_name = data.last_name[0].upper() + data.last_name[1:]
            data.locality = request.POST['locality']
            # helper_save 
            data.save()


            # History store 
            current_datetime = datetime.now()
            if not HelperHistoryModel.objects.filter(Q(helper_id = data.helper_id) & Q(history_status = 'update')).exists():
                helper_history = HelperHistoryModel(
                helper_id = data.helper_id,
                first_name = data.first_name,
                middle_name = data.middle_name,
                last_name = data.last_name,
                primary_phone = data.primary_phone,
                email_id = data.email_id,
                dob = data.dob,
                create_date = data.create_date,
                update_date = current_datetime.today(),
                admin_user = request.user,
                history_status = 'update'
                )

                helper_history.save()

                HistoryModel(
                    helper =HelperHistoryModel.objects.get(Q(helper_id = data.helper_id) & Q(history_status = 'update')),
                    date = current_datetime
                ).save()

                

            else:
                helper_history = HelperHistoryModel.objects.filter(Q(helper_id = data.helper_id) & Q(history_status = 'update'))
                helper_history.update(
                        helper_id = data.helper_id,
                        first_name = data.first_name,
                        middle_name = data.middle_name,
                        last_name = data.last_name,
                        primary_phone = data.primary_phone,
                        email_id = data.email_id,
                        dob = data.dob,
                        create_date = data.create_date,
                        update_date = current_datetime.today(),
                        admin_user = request.user,
                        history_status = 'update'
                )
                HistoryModel.objects.filter(helper = HelperHistoryModel.objects.get(Q(helper_id = data.helper_id) & Q(history_status = 'update'))).update(
                    helper = HelperHistoryModel.objects.get(Q(helper_id = data.helper_id) & Q(history_status = 'update')),
                    date = current_datetime
                )

            messages.success(request,'Data updated successfully!')
        else:
            messages.error(request,'please enter valid data!')

    data = {
        'fm':fm,
        'skill': helper_skill,
        'additional_skill':helper_additional_skill,
        'helper_language':helper_language,
        'job_role':HelperJobRoleModel.objects.filter(helper=helper),
        'locations':location_values,
        'locality':helper.locality
    }
    return render(request,'helper_edit.html',data)

# helper phone exist or not logic 
@login_required
def HelperPhoneNoValidateDetailsView(request,id):
        helper = HelperModel.objects.get(id = id)
        data = {
        'helper':helper,
        'language':HelperPreferredLanguageModel.objects.filter(helper = helper),
        'skill':HelperSkillSetModel.objects.filter(helper = helper),
        'additional_skill':HelperAdditionalSkillSetModel.objects.filter(helper=helper),
        'job_role':HelperJobRoleModel.objects.filter(helper=helper),
        }  
        return render(request,'helper_valid_check.html',data)  

# accept helper 
@login_required
def HelperPhoneNoValidateAcceptView(request,id):
    helper = HelperModel.objects.get(id = id)
    helper.phone_valid = False
    helper.save()
    return redirect('home')

# reject helper 
@login_required
def HelperPhoneNoValidateRejectedView(request,id):
    helper = HelperModel.objects.get(id = id)
    helper.delete()
    return redirect('home')


# lead random id generate 
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
        # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

        # # open google sheet by help of key
        # worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
    
        # # which sheet you want to open! 
        # current_sheet = worksheet.worksheet('Sheet1')

        # # Data get dictionary format 
        # all_value = current_sheet.get_all_records()
        leads = LeadModel.objects.all()
    except:
        # exception handle 
        messages.error(request,'Something error try again! may be network issue!')
    
    data = {
        'data':leads,
        'length':len(leads)
    }
    return render(request,'lead_list.html',data)   


# lead details show 
@login_required
def LeadDetailsView(request,no):
    data = {}
    try:
        # configuration json file 
        # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

        # # open google sheet by help of key
        # worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
        
        # # which sheet you want to open! 
        # current_sheet = worksheet.worksheet('Sheet1')
        
        # all row data
        # row_num = int(no)+1
        # values_list = current_sheet.row_values(row_num)
        leads = LeadModel.objects.get(id=no)
        data = {
            'name' : leads.name,
            'phone' : leads.phone,
            'email' : leads.email_id,
            'addr' : leads.address,
            'id': leads.lead_id,
            'locality':leads.locality,
            'near_by':leads.near_by,
            'availability':leads.availability_status
        }
    except:
         # exception handle 
        messages.error(request,'Something error try again! may be network issue!')

    return render(request,'lead_details.html',data)  

import sys

# update the lead 
@login_required
def LeadEditView(request,no):
    # locality's value get in Gspreed 
    location_values = ''
    try:
        # configuration json file 
        # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

        # # open google sheet by help of key
        # worksheet = gc.open_by_key('1XvBPqKzz3fl0qWODP6gIYjTI03_17Ul8pqGGe2RSg9c')
    
        # # which sheet you want to open! 
        # current_sheet = worksheet.worksheet('Sheet1')

        # # Data get dictionary format 
        # location_values = current_sheet.get_all_records()
        location_values = Localities.objects.all()
    except:
        # exception handle 
        messages.error(request,'Something error try again! may be network issue!')

    # lead data get 
    data = {}
    try:
        current_datetime = datetime.now()

           # configuration json file 
        # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

        # # open google sheet by help of key
        # worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
        
        # # which sheet you want to open! 
        # current_sheet = worksheet.worksheet('Sheet1')
        
        # # all row data
        # row_num = int(no)+1
        # values_list = current_sheet.row_values(row_num)
        leads = LeadModel.objects.get(id=no)
        job_category = leads.job_category.split(',')
        excluded_roles = ['nanny', ' housekeeper',' caregiver']
        included_roles = [role for role in job_category if role not in excluded_roles]

        data = {
            'name' : leads.name,
            'phone' : leads.phone,
            'email' : leads.email_id,
            'addr' : leads.address,
            'locality':leads.locality,
            'near_by':leads.near_by,
            'availability':leads.availability_status,
            'locations':location_values,
            'flat_number':leads.flat_number, 
            'lead_req_date':leads.lead_req_date,
            'lead_placement_date' :leads.lead_placement_date,
            'lead_status2' :leads.lead_status2,
            'additional_comment':leads.additional_comment,
            'job_role' :leads.job_category,
            'other_roles':', '.join(included_roles),
            'lead_source':leads.lead_source,
            'role_on_demand_start_date':leads.role_on_demand_start_date,
             'role_on_demand_start_from_time':   leads.role_on_demand_start_from_time, 
            'role_on_demand_start_to_time':  leads.role_on_demand_start_to_time ,
            'role_on_demand_end_date':    leads.role_on_demand_end_date, 
            'role_on_demand_end_from_time':   leads.role_on_demand_end_from_time, 
            'role_on_demand_end_to_time':   leads.role_on_demand_end_to_time 
        }
        
    
        # POST
        if request.method == "POST":

            # all value get by input in lead_edit.html
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            addr = request.POST['addr']
            locality = request.POST['locality']
            near_by = request.POST.get('near_by',False)
            availability = request.POST['availability']
            flat_number = request.POST['flat_num']
            lead_req_date =  request.POST['LeadRequirementDate']
            lead_placement_date = request.POST['LeadPlacementDate']
            lead_status = request.POST['LeadStatus']
            additional_comment=request.POST['AdditionalComment']
            job_role = ', '.join(request.POST.getlist('job_role'))  
            lead_source=request.POST['LeadSource']

            # near_by set
            if near_by == 'on':
                near_by = True

            # values set/update in sheets 
            # current_sheet.update_cell(row_num, 1, name)
            # current_sheet.update_cell(row_num, 2, phone)
            # current_sheet.update_cell(row_num, 3, email)
            # current_sheet.update_cell(row_num, 4, addr)
            # current_sheet.update_cell(row_num, 10, locality)
            # current_sheet.update_cell(row_num, 11, near_by)
            # current_sheet.update_cell(row_num, 12, availability)
            if LeadModel.objects.get(id =no):
                    lead_data_all =LeadModel.objects.get(id =no)
                    lead_data_all.lead_id = leads.lead_id
                    lead_data_all.name = name
                    lead_data_all.phone = phone
                    lead_data_all.email_id = email
                    lead_data_all.address=addr
                    lead_data_all.availability_status =availability
                    lead_data_all.locality =locality
                    lead_data_all.near_by = near_by
                    lead_data_all.lead_status = "pending"
                    lead_data_all.flat_number = flat_number
                    lead_data_all.lead_req_date = lead_req_date
                    lead_data_all.lead_placement_date = lead_placement_date
                    lead_data_all.lead_status2 = lead_status
                    lead_data_all.lead_source=lead_source
                    lead_data_all.additional_comment=additional_comment
                    lead_data_all.job_category=job_role
                    if request.POST['Start_Date'] != '':
                        lead_data_all.role_on_demand_start_date =request.POST['Start_Date']
                        lead_data_all.role_on_demand_start_from_time = request.POST.get('s_StartDuration')
                        lead_data_all.role_on_demand_start_to_time = request.POST.get('s_EndDuration')
                        lead_data_all.role_on_demand_end_date =request.POST['End_Date']
                        lead_data_all.role_on_demand_end_from_time = request.POST.get('e_StartDuration')
                        lead_data_all.role_on_demand_end_to_time  =request.POST.get('e_EndDuration')
                    lead_data_all.save()
            # lead_history model 
            if not leadHistoryModel.objects.filter(Q(lead_id = leads.lead_id) & Q(history_status = 'update')).exists():
                lead_history = leadHistoryModel(
                    lead_id = leads.lead_id,
                    name = name,
                    phone = phone,
                    email = email,
                    admin_user = request.user,
                    history_status = 'update'
                )
                lead_history.save()

                # history model 
                HistoryModel(lead = lead_history).save()
            
            else:
                lead_history = leadHistoryModel.objects.filter(Q(lead_id = leads.lead_id) & Q(history_status = 'update'))
                lead_history.update(
                     lead_id = leads.lead_id,
                    name = name,
                    phone = phone,
                    email = email,
                    admin_user = request.user,
                    history_status = 'update'
                )

                HistoryModel.objects.filter(lead = leadHistoryModel.objects.get(Q(lead_id = leads.lead_id) & Q(history_status = 'update'))).update(
                    lead =  leadHistoryModel.objects.get(Q(lead_id = leads.lead_id) & Q(history_status = 'update')),
                    date = current_datetime.today()
                )

            # message to success
            messages.success(request,'Data updated successful!')

            # redirect with same page 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     
    except Exception as e:
       
        messages.error(request,f'Something error try again! may be network issue!')
    return render(request,'lead_edit.html',data)
     

# delete data from sheet 
@login_required
def LeadDeleteView(request,no):
    try:
        current_datetime = datetime.now()
        # configuration json file 
        # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

        # # open google sheet by help of key
        # worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
        
        # # which sheet you want to open! 
        # current_sheet = worksheet.worksheet('Sheet1')
        
        # # all row data
        # row_num = int(no)+1
        leads = LeadModel.objects.get(id=no)

        # get data 
        # values_list = current_sheet.row_values(row_num)

        # id = values_list[8]
        # phone = values_list[1]
        # name = values_list[0]
        # email = values_list[2]
       

        id = leads.lead_id
        phone = leads.phone
        name = leads.name
        email = leads.email_id
        
        # lead_history model 
        lead_history = leadHistoryModel(
            lead_id = id,
            name = name,
            phone = phone,
            email = email,
            admin_user = request.user,
            update_date = current_datetime.today(),
            history_status = 'delete'
        )
        lead_history.save()

        # history 
        HistoryModel(
            lead = lead_history
        ).save()

        # delete the row by help of row num 
        leads.delete()

        # success message 
        messages.success(request,'data remove successful!')
    except:
         # exception handle 
        messages.error('Data not to be deleted something error try again!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# data insert into lead sheet 
@login_required
def LeadInsertDataView(request):
    # locality's value get in Gspreed 
    location_values = ''
    try:
        # configuration json file 
        # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

        # # open google sheet by help of key
        # worksheet = gc.open_by_key('1XvBPqKzz3fl0qWODP6gIYjTI03_17Ul8pqGGe2RSg9c')
    
        # # which sheet you want to open! 
        # current_sheet = worksheet.worksheet('Sheet1')

        # # Data get dictionary format 
        # location_values = current_sheet.get_all_records()
        location_values = Localities.objects.all()
    except:
        # exception handle 
        messages.error(request,'Something error try again! may be network issue!')

        
    if request.method == 'POST':
        try:
            # configuration json file 
            # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

            # # open google sheet by help of key
            # worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
            
            # # which sheet you want to open! 
            # current_sheet = worksheet.worksheet('Sheet1')
            

            # value get from lead_add.html
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            addr = request.POST['addr']
            locality = request.POST['locality']
            near_by = request.POST.get('near_by',False)
            availability = request.POST['availability']
            flat_number = request.POST['flat_num']
            lead_req_date =  request.POST['LeadRequirementDate']
            lead_placement_date = request.POST['LeadPlacementDate']
            lead_status = request.POST['LeadStatus']
            additional_comment=request.POST['AdditionalComment']
            job_role = ', '.join(request.POST.getlist('job_role')) 
            lead_source=request.POST['LeadSource']
            # id generate 
            leads = LeadModel.objects.all()
            id = lead_generate_id(leads.count()+20)

            # near_by field
            if near_by == 'on':
                near_by = True

            # all value in list format 
            lst = [name,phone,email,addr," "," "," ","pending",id,locality,near_by,availability]
            
            # row append in sheet 
            # current_sheet.append_row(lst)

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

            # lead_history mode  
            lead_history = leadHistoryModel(
                lead_id = id,
                name = name,
                phone = phone,
                email = email,
                admin_user = request.user,
                history_status = 'create'
            )
            lead_history.save()
            #main lead model 
            lead_data_all =LeadModel(
                lead_id = id,
                name = name,
                phone = phone,
                email_id = email,
                address=addr,
                availability_status =availability,
                # locality 
                locality =locality,
                near_by = near_by,
                lead_status = "pending",
                admin_user = request.user,
                flat_number = flat_number,
                lead_req_date = lead_req_date,
                lead_placement_date = lead_placement_date,
                lead_status2 = lead_status,
                lead_source=lead_source,
                additional_comment=additional_comment,
                job_category=job_role)
            if request.POST['Start_Date'] != '':
                lead_data_all.role_on_demand_start_date =request.POST['Start_Date']
                lead_data_all.role_on_demand_start_from_time = request.POST.get('s_StartDuration')
                lead_data_all.role_on_demand_start_to_time = request.POST.get('s_EndDuration')
                lead_data_all.role_on_demand_end_date =request.POST['End_Date']
                lead_data_all.role_on_demand_end_from_time = request.POST.get('e_StartDuration')
                lead_data_all.role_on_demand_end_to_time  =request.POST.get('e_EndDuration')
              
            
            lead_data_all.save()

            # history model 
            HistoryModel(
                lead = lead_history,
            ).save()

            messages.success(request,"Data add successful!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception as e:
            # exception handle
           
            print(f"{type(request.POST['Start_Date'])} {type(request.POST['s_StartDuration'])}")
            messages.error(request,f'Something error try again! may be network issue!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    data = {
        'locations':location_values
    }
    return render(request,'lead_add.html',data)

@login_required
def LeadStatusUpdateView(request,row):
    # row = int(row)+1
    col = 8
    try:
        # configuration json file 
        # gc = gspread.service_account(filename = "app/testsample-393218-c2720cf831ca.json")

        # # open google sheet by help of key
        # worksheet = gc.open_by_key('1vFDeyQbaSetQRmjq7V7f_Uv9dQ0CJb9cXRp03lK_H0Y')
            
        # # which sheet you want to open! 
        # current_sheet = worksheet.worksheet('Sheet1')
        leads = LeadModel.objects.get(id=row)
        leads.lead_status = request.POST['lead_status_inp']
        leads.save()
        # lead_status_inp = request.POST['lead_status_inp']

        # # update status 
        # current_sheet.update_cell(row,col,lead_status_inp)

        messages.success(request,"Data update successful.!")
    except:
        # exception handle 
        messages.error(request,'Something error try again! may be network issue!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def HistoryView(request):
    data = {
        'data':HistoryModel.objects.all().order_by('-date')
    }
    return render(request,'history.html',data)

def HistoryDetailsView(request,id):
    data = {
      'data':HistoryModel.objects.get(id = id)
    }
    return render(request,"history_details.html",data)









      

       

       

        







