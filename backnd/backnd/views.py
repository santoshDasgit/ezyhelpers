import hashlib
import traceback
import re

from datetime import date
from datetime import datetime

from app.form import *
from app.models import LeadModel, Localities, Skills, HelperModel
from app.resources import HelperModelResources
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from tablib import Dataset
from xhtml2pdf import pisa


# Home page
def HomeView(request):
    if request.user.is_authenticated:  # check user login or not
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
            if (User.objects.filter(username=username).exists()):
                user = authenticate(username=username, password=password)
                # if user and password is correct
                if user is not None:
                    login(request, user)
                    # messages.success(request,f"Welcome {username}..!")
                    # if all are correct redirect to home
                    return redirect("home")
                else:
                    # if password invalid
                    messages.error(request, "Invalid password!")
            else:
                # if username does'not exists
                messages.error(request, "Invalid email address!")
    else:
        return redirect("home")
    return render(request, 'login.html')


# Logout function
@login_required
def LogoutView(request):
    logout(request)
    messages.success(request, "Logout success!")
    return redirect('/')


# profile details
@login_required
def ProfileView(request, id):
    return render(request, 'profile.html')


# email verify from profile update


@login_required
def EmailVerifyProfileView(request, id, url):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.get(pk=id)
        if (User.objects.filter(email=email).exists() and user.email != email):
            messages.error(
                request, f"{email} already exists try another email!")
        else:
            url = f'http://{url}/profile_update/{id}/{email}'
            subject = "user data updated url!!"
            message = f'url link : {url}'
            from_email = settings.EMAIL_HOST_USER
            to = email
            email_box = EmailMultiAlternatives(
                subject, message, from_email, [to])
            email_box.content_subtype = 'html'
            email_box.send()
            messages.success(
                request, 'check url on your email to update the data!')

    return render(request, "email_validate.html")


# Profile update
def ProfileUpdateView(request, id, email):
    # if user is not login
    if not request.user.is_authenticated:
        messages.warning(
            request, 'at the time of profile update Login mandatory!')
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
        user = User.objects.get(id=id)

        # if same name of email is already exists
        if (User.objects.filter(email=email).exists() and user.email != email):

            messages.error(
                request, f"{email} already exists try another email!")
        else:
            # try catch from network issue handle
            try:
                # email send Logic
                subject = "user data updated!!"
                message = f'email : <b>{email}</b> <br> first name : <b>{first_name}</b> <br> last name : <b>{last_name}</b>'
                from_email = settings.EMAIL_HOST_USER
                to = email
                email_box = EmailMultiAlternatives(
                    subject, message, from_email, [to])
                email_box.content_subtype = 'html'
                email_box.send()

                # value configurations
                user.username = email
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # messages to update
                messages.success(request, "Profile update successful!")
            except:
                messages.error("There is an error please try again!")

            # page redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'profile_update.html', {'email': email})


# Function to validate the password
def password_check(passwd, request):
    SpecialSym = ['$', '@', '#', '%', '!', '&', '*', '^']
    val = True

    if len(passwd) <= 8:
        messages.error(request, 'length should be at least 8!')
        val = False

    if not any(char.isdigit() for char in passwd):
        messages.error(request, 'Password should have at least one numeral!')
        val = False

    if not any(char.isupper() for char in passwd):
        messages.error(
            request, 'Password should have at least one uppercase letter!')
        val = False

    if not any(char.islower() for char in passwd):
        messages.error(
            request, 'Password should have at least one lowercase letter!')
        val = False

    if not any(char in SpecialSym for char in passwd):
        messages.error(
            request, 'Password should have at least one of the symbols $@#!')
        val = False
    if ' ' in passwd:
        messages.error(request, 'Space not allow!')
        val = False
    if val:
        return val


# profile password changed
@login_required
def PasswordChangedView(request):
    # user
    user = User.objects.get(username=request.user)

    if request.method == "POST":

        # all data get from input
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        conform_pass = request.POST['conform_password']

        # password format check
        if password_check(new_password, request):
            # check old password correct or not
            if user.check_password(old_password):
                # check conform password match
                if (new_password == conform_pass):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)

                    # message
                    messages.success(request, 'password changed successful!')

                    # page redirect with same page
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                else:
                    messages.error(request, "conform password doesn't match!")
            else:
                messages.error(request, 'old password is incorrect!')
        else:
            pass

    return render(request, 'password_change.html')


# unique id generated Hexadec


def generate_id(id):
    # Generate a random number
    random_num = str(id + 1000000000).encode()

    # Generate a SHA-256 hash of the random number.
    hash_obj = hashlib.sha256(random_num)
    hex_digit = hash_obj.hexdigest()
    return hex_digit[:10]


# Dashboard or home of a superuser
@login_required
def HelperListViews(request):
    helper = HelperModel.objects.filter(
        phone_valid=False).order_by('-id')  # helper model object

    # post for data searching propose
    if request.method == 'POST':
        # strip for remove space from both of sides
        if request.POST.get('search', None) is not None:
            search = request.POST['search'].strip()

            # according to input data is filtering
            helper = HelperModel.objects.filter(Q(helper_id__icontains=search) | Q(
                first_name__icontains=search) | Q(email_id__icontains=search) | Q(primary_phone__icontains=search))

    # all data sent on html file in object format
    data = {
        'helper_list': helper
    }
    return render(request, "helper_list.html", data)


# Helper data inserted
@login_required
def HelperAddView(request):
    # location value get in Gspreed
    location_values = ''
    helpers_skills = ''
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
        helpers_skills = Skills.objects.all()
        job_cat = JobCat.objects.all()
    except:
        # exception handle
        messages.error(
            request, 'Something error try again! may be network issue!')

    fm = HelperForm()
    if request.method == "POST":

        # data input
        language = request.POST.getlist('language')
        additional_skill = request.POST.getlist('ad-skill')
        skill = request.POST.getlist('skill')
        job_role = request.POST.getlist('job_role')

        # language required condition
        if language == ['']:
            messages.error(request, '* Preferred Language required!')
        else:
            fm = HelperForm(request.POST, request.FILES)
            if fm.is_valid():
                # phone number exist or not valid (phone_valid)

                # if secondary phone empty
                if fm.instance.secondary_phone != None and HelperModel.objects.filter(
                        Q(primary_phone=fm.instance.primary_phone) | Q(secondary_phone=fm.instance.secondary_phone) | Q(
                            primary_phone=fm.instance.secondary_phone) | Q(
                            secondary_phone=fm.instance.primary_phone)).exists():
                    fm.instance.phone_valid = True
                    messages.warning(
                        request, 'Redundant phone number , please check in dashboard ! ')

                # if secondary phone not empty
                if fm.instance.secondary_phone == None and HelperModel.objects.filter(
                        Q(primary_phone=fm.instance.primary_phone) | Q(
                            secondary_phone=fm.instance.primary_phone)).exists():
                    fm.instance.phone_valid = True
                    messages.warning(
                        request, 'Redundant phone number , please check in dashboard ! ')

                data = fm.save()
                # function to create id and convert into Hexa
                data.helper_id = generate_id(data.id)
                data.admin_user = request.user

                # first name and last name in upper case first char
                data.first_name = data.first_name[0].upper(
                ) + data.first_name[1:]
                data.last_name = data.last_name[0].upper() + data.last_name[1:]

                # locality
                data.locality = request.POST['locality']

                # helper_save
                data.save()

                # History store
                current_datetime = datetime.now()
                helper_history = HelperHistoryModel(
                    helper_id=data.helper_id,
                    first_name=data.first_name,
                    middle_name=data.middle_name,
                    last_name=data.last_name,
                    primary_phone=data.primary_phone,
                    email_id=data.email_id,
                    dob=data.dob,
                    create_date=current_datetime,

                    admin_user=request.user,
                    history_status='create'
                )
                helper_history.save()
                HistoryModel(
                    helper=helper_history,
                    date=current_datetime
                ).save()

                messages.success(request, 'data added successfully!')

                # preferences language inserted
                for i in language:
                    if i != '':
                        HelperPreferredLanguageModel(
                            helper=data, language=i).save()

                # additional_skill inserted
                for i in additional_skill:
                    if i != '':
                        HelperAdditionalSkillSetModel(
                            helper=data, additional_skill=i).save()

                # skill inserted
                for i in skill:
                    if i != '':
                        HelperSkillSetModel(helper=data, skill=i).save()

                # job role
                for i in job_role:
                    if i != '':
                        HelperJobRoleModel(helper=data, job=i).save()

                return HelperListViews(request)
            else:
                messages.error(request, 'please enter the valid data!')

    data = {
        'fm': fm,
        'locations': location_values,
        'helpers_skills': helpers_skills,
        'job_cat': job_cat
    }
    return render(request, 'helper_add.html', data)


# helper all details showing
@login_required
def HelperDetailsView(request, id):
    helper = HelperModel.objects.get(id=id)
    data = {
        'helper': helper,
        'language': HelperPreferredLanguageModel.objects.filter(helper=helper),
        'skill': HelperSkillSetModel.objects.filter(helper=helper),
        'additional_skill': HelperAdditionalSkillSetModel.objects.filter(helper=helper),
        'job_role': HelperJobRoleModel.objects.filter(helper=helper),
    }
    return render(request, 'helper_view.html', data)


# Helper all data into pdf


def HelperPdfView(request, id):
    helper = HelperModel.objects.get(id=id)

    data = {
        'helper': helper,
        'language': HelperPreferredLanguageModel.objects.filter(helper=helper),
        'skill': HelperSkillSetModel.objects.filter(helper=helper),
        'additional_skill': HelperAdditionalSkillSetModel.objects.filter(helper=helper),
        'job_role': HelperJobRoleModel.objects.filter(helper=helper),
    }
    template = get_template('helper_pdf.html')
    context = data  # Add any context data you need for the template
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{helper}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error while generating PDF', status=500)
    return response


# Helper status update logic
@login_required
def HelperStatusUpdateView(request, id):
    if request.method == 'POST':
        helper_status_inp = request.POST['helper-status-inp']
        helper = HelperModel.objects.get(id=id)
        helper.helper_status = helper_status_inp
        helper.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def create_helper(request, i):
    first_name = ''
    middle_name = ''
    last_name = ''

    if i[0] is not None or i[1] != '':
        names = i[0].split(' ')
        first_name = names[0]
        if len(names) == 2:
            last_name = names[1]
        if len(names) == 3:
            middle_name = names[1]
            last_name = names[2]

    primary_phone = get_mobile_number(str(i[1]))
    if primary_phone is None:
        raise Exception('Invalid phone number')

    return HelperModel(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        primary_phone=primary_phone,
        job_role_2=(i[2] or ''),
        availability_status=(i[3] or ''),
        helper_locality=(i[4] or ''),
        society=(i[5] or ''),
        listed_by=(i[6] or ''),
        language_known=(i[7] or ''),
        age=i[8],
        gender=(i[9] or ''),
        sunday=(i[10] or ''),
        smartphone=(i[11] or ''),
        whatsApp=(i[12] or ''),
        start_time_1=i[13],
        end_time_1=i[14],
        start_time_2=i[15],
        end_time_2=i[16],
        start_time_3=i[17],
        end_time_3=i[18],
        start_time_4=i[19],
        end_time_4=i[20],
        charges=i[21],
        preferences=(i[22] or ''),
        id_proof_status=(i[23] or ''),
        aadhar_verification=(i[24] or ''),
        id_pdf=(i[25] or ''),
        other_id_proof=(i[26] or ''),
        police_verification=(i[27] or ''),
        engagement_date=i[28],
        previous_employer_name=(i[30] or ''),
        previous_employer_contact=(i[31] or ''),
        previous_employer_society=(i[32] or ''),
        rating=i[33],
        remarks=(i[34] or ''),
        additional_comment=(i[35] or ''),
        attempt_2=(i[36] or '')
    )


def get_mobile_number(phone):
    if len(phone) != 10:
        return None

    number = re.search("(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})", phone)
    if number is not None:
        return number.group()
    else:
        return None


def get_helper(request, helper):
    fields = helper.split(',')

    primary_phone = get_mobile_number(fields[4].split(':')[1])
    if primary_phone is None:
        raise Exception('Invalid phone number')

    return HelperModel(
        helper_id=fields[0].split(':')[1],
        first_name=fields[1].split(':')[1],
        middle_name=fields[2].split(':')[1] or '',
        last_name=fields[3].split(':')[1] or '',
        primary_phone=primary_phone,
        job_role_2=fields[5].split(':')[1] or '',
        availability_status=fields[6].split(':')[1] or '',
        helper_locality=helper.split(',helper_locality:')[1].split(',society:')[0] or '',
        society=helper.split(',society:')[1].split(',listed_by:')[0] or '',
        listed_by=helper.split(',listed_by:')[1].split(',language_known:')[0] or '',
        language_known=helper.split(',language_known:')[1].split(',age:')[0] or '',
        age=None if helper.split(',age:')[1].split(',gender:')[0] == 'None' else
        helper.split(',age:')[1].split(',gender:')[0],
        gender=helper.split(',gender:')[1].split(',sunday:')[0] or '',
        sunday=helper.split(',sunday:')[1].split(',smartphone:')[0] or '',
        smartphone=helper.split(',smartphone:')[1].split(',whatsApp:')[0] or '',
        whatsApp=helper.split(',whatsApp:')[1].split(',start_time_1:')[0] or '',
        start_time_1=None if helper.split(',start_time_1:')[1].split(',end_time_1:')[0] == 'None' else
        helper.split(',start_time_1:')[1].split(',end_time_1:')[0],
        end_time_1=None if helper.split(',end_time_1:')[1].split(',start_time_2:')[0] == 'None' else
        helper.split(',end_time_1:')[1].split(',start_time_2:')[0],
        start_time_2=None if helper.split(',start_time_2:')[1].split(',end_time_2:')[0] == 'None' else
        helper.split(',start_time_2:')[1].split(',end_time_2:')[0],
        end_time_2=None if helper.split(',end_time_2:')[1].split(',start_time_3:')[0] == 'None' else
        helper.split(',end_time_2:')[1].split(',start_time_3:')[0],
        start_time_3=None if helper.split(',start_time_3:')[1].split(',end_time_3:')[0] == 'None' else
        helper.split(',start_time_3:')[1].split(',end_time_3:')[0],
        end_time_3=None if helper.split(',end_time_3:')[1].split(',start_time_4:')[0] == 'None' else
        helper.split(',end_time_3:')[1].split(',start_time_4:')[0],
        start_time_4=None if helper.split(',start_time_4:')[1].split(',end_time_4:')[0] == 'None' else
        helper.split(',start_time_4:')[1].split(',end_time_4:')[0],
        end_time_4=None if helper.split(',end_time_4:')[1].split(',charges:')[0] else
        helper.split(',end_time_4:')[1].split(',charges:')[0],
        charges=helper.split(',charges:')[1].split(',preferences:')[0] or '',
        preferences=helper.split(',preferences:')[1].split(',id_proof_status:')[0] or '',
        id_proof_status=helper.split(',id_proof_status:')[1].split(',aadhar_verification:')[0] or '',
        aadhar_verification=helper.split(',aadhar_verification:')[1].split(',id_pdf:')[0] or '',
        id_pdf=helper.split(',id_pdf:')[1].split(',other_id_proof:')[0],
        other_id_proof=helper.split(',other_id_proof:')[1].split(',police_verification:')[0] or '',
        police_verification=helper.split(',police_verification:')[1].split(',engagement_date:')[0] or '',

        # YYYY-MM-DD
        engagement_date=None if helper.split(',engagement_date:')[1].split(',previous_employer_name:')[0] == 'None' else helper.split(',engagement_date:')[1].split(',previous_employer_name:')[0].split(' ')[0],
        previous_employer_name=helper.split(',previous_employer_name:')[1].split(',previous_employer_contact:')[0] or '',
        previous_employer_contact=helper.split(',previous_employer_contact:')[1].split(',previous_employer_society:')[0] or '',
        previous_employer_society=helper.split(',previous_employer_society:')[1].split(',rating:')[0] or '',
        rating=None if helper.split(',rating:')[1].split(',remarks:')[0] == 'None' else
        helper.split(',rating:')[1].split(',remarks:')[0],
        remarks=helper.split(',remarks:')[1].split(',additional_comment:')[0] or '',
        additional_comment=helper.split(',additional_comment:')[1].split(',attempt_2:')[0] or '',
        attempt_2=helper.split(',attempt_2:')[1] or '',
    )


# excel file through helper create TBD
@login_required
def ExcelFileHelperFileView(request):
    duplicates = []
    if request.method == 'POST':
        helper_resources = HelperModelResources()
        data_set = Dataset()
        myfile = request.FILES['myfile']

        # check excel file or not!
        if not myfile.name.endswith('xlsx'):
            messages.error(request, 'Excel file only allow!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                # all excel data store in 'excel_data' in form of table
                excel_data = data_set.load(myfile.read(), format='xlsx')
                contains_duplicate = False
                for i in excel_data:
                    # row fully empty or not check
                    if (i[0] is None or i[0] == '') and (i[1] is None or i[1] == '') and (i[3] is None or i[3] == ''):
                        pass
                    else:
                        primary_phone = get_mobile_number(str(i[1]))
                        if primary_phone is None:
                            raise Exception('Invalid phone number')

                        if HelperModel.objects.filter(primary_phone = primary_phone).exists():
                            duplicates.append(create_helper(request, i))
                            contains_duplicate = True
                            pass
                        else:
                            helper = create_helper(request, i)
                            helper.save()

                            # helper id generate and store it
                            helper.helper_id = generate_id(helper.pk)
                            helper.save()
                if contains_duplicate:
                    data = {
                        'data': duplicates,
                        'length': len(duplicates)
                    }
                    return render(request, 'helper_excel.html', data)

                # if all right then success message
                messages.success(request, 'file upload successful!')
            except Exception as e:
                # exception handle
                messages.error(request, f'Invalid data in ' + str(i) + ', Error:' + e.__str__())
                print(traceback.format_exc())
            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'helper_excel.html')


# excel file through lead create
@login_required
def ExcelFileLeadFileView(request):
    duplicates = []
    if request.method == 'POST':
        data_set = Dataset()
        myfile = request.FILES['myfile']

        # check excel file or not!
        if not myfile.name.endswith('xlsx'):
            messages.error(request, 'Excel file only allow!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                # all excel data store in 'excel_data' in form of table
                excel_data = data_set.load(myfile.read(), format='xlsx')
                contains_duplicate = False
                for i in excel_data:
                    # row fully empty or not check
                    if (i[1] is None or i[1] == ''):
                        pass
                    else:
                        primary_phone = get_mobile_number(str(i[1]))
                        if primary_phone is None:
                            raise Exception('Invalid phone number')

                        if LeadModel.objects.filter(phone=primary_phone).exists():
                            duplicates.append(create_lead(request, i, ''))
                            contains_duplicate = True
                            pass
                        else:
                            leads = LeadModel.objects.all()

                            lead_id = lead_generate_id(len(leads) + 20)
                            lead = create_lead(request, i, lead_id)

                            lead.save()

                if contains_duplicate:
                    data = {
                        'data': duplicates,
                        'length': len(duplicates)
                    }
                    return render(request, 'lead_excel.html', data)

                # if all right then success message
                messages.success(request, 'file upload successful!')
            except Exception as e:
                # exception handle
                messages.error(request, f'Invalid data in ' + str(i) + ', Error:' + e.__str__())
                print(traceback.format_exc())
            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'lead_excel.html', None)


@login_required
def ExcelFileLeadFileDuplicateAcceptView(request):
    if request.method == 'POST':
        duplicates = request.POST.get('duplicates_leads')
        duplicates = duplicates[1:-1]
        leads = duplicates.split('<LeadModel: ')
        for duplicate in leads:
            if duplicate != "":
                lead = get_lead(request, duplicate.split('>')[0])
                lead_db = LeadModel.objects.get(phone=lead.phone)
                update_lead(lead, lead_db)
        messages.success(request, 'Leads updated successfully!')
    return LeadList(request)


def update_lead(lead_excel, lead_db):
    try:
        if lead_excel.name is not None and lead_excel.name != "":
            lead_db.name = lead_excel.name

        if lead_excel.email_id is not None and lead_excel.email_id != "":
            lead_db.email_id = lead_excel.email_id

        if lead_excel.availability_status is not None and lead_excel.availability_status != "":
            lead_db.availability_status = lead_excel.availability_status

        if lead_excel.job_category is not None and lead_excel.job_category != "":
            lead_db.job_category = lead_excel.job_category

        if lead_excel.requirement_start_time is not None and lead_excel.requirement_start_time != "":
            lead_db.requirement_start_time = lead_excel.requirement_start_time

        lead_db.update_date = datetime.now()

        if lead_excel.requirement_end_time is not None and lead_excel.requirement_end_time != "":
            lead_db.requirement_end_time = lead_excel.requirement_end_time

        if lead_excel.society is not None and lead_excel.society != "":
            lead_db.society = lead_excel.society

        if lead_excel.flat_number is not None and lead_excel.flat_number != "":
            lead_db.flat_number = lead_excel.flat_number

        if lead_excel.form_fill_status is not None and lead_excel.form_fill_status != '':
            lead_db.form_fill_status = lead_excel.form_fill_status

        if lead_excel.lead_status is not None and lead_excel.lead_status != "":
            lead_db.lead_status = lead_excel.lead_status

        if lead_excel.helper_name is not None and lead_excel.helper_name != '':
            lead_db.helper_name = lead_excel.helper_name

        if lead_excel.actual_status is not None and lead_excel.actual_status != "":
            lead_db.actual_status = lead_excel.actual_status

        if lead_excel.lead_lost_reason is not None and lead_excel.lead_lost_reason != "":
            lead_db.lead_lost_reason = lead_excel.lead_lost_reason

        if lead_excel.lead_placement_date is not None and lead_excel.lead_placement_date != '':
            lead_db.lead_placement_date = lead_excel.lead_placement_date

        if lead_excel.exit_date is not None and lead_excel.exit_date != "":
            lead_db.exit_date = lead_excel.exit_date

        if lead_excel.identity_type is not None and lead_excel.identity_type != "":
            lead_db.identity_type = lead_excel.identity_type

        if lead_excel.identity_status is not None and lead_excel.identity_status != "":
            lead_db.identity_status = lead_excel.identity_status

        if lead_excel.identity_shared is not None and lead_excel.identity_shared != "":
            lead_db.identity_shared = lead_excel.identity_shared

        if lead_excel.application_form is not None and lead_excel.application_form != "":
            lead_db.application_form = lead_excel.application_form

        if lead_excel.duration is not None and lead_excel.duration != "":
            lead_db.duration = lead_excel.duration

        if lead_excel.payment_date is not None and lead_excel.payment_date != '':
            lead_db.payment_date = lead_excel.payment_date

        if lead_excel.payment_status is not None and lead_excel.payment_status != '':
            lead_db.payment_status = lead_excel.payment_status

        if lead_excel.payment_mode is not None and lead_excel.payment_mode != "":
            lead_db.payment_mode = lead_excel.payment_mode

        if lead_excel.salary is not None and lead_excel.salary != "":
            lead_db.salary = lead_excel.salary

        if lead_excel.third_party is not None and lead_excel.third_party != '':
            lead_db.third_party = lead_excel.third_party

        if lead_excel.commission is not None and lead_excel.commission != "":
            lead_db.commission = lead_excel.commission

        if lead_excel.lead_source is not None and lead_excel.lead_source != "":
            lead_db.lead_source = lead_excel.lead_source

        if lead_excel.sales_person is not None and lead_excel.sales_person != "":
            lead_db.sales_person = lead_excel.sales_person

        if lead_excel.additional_comment is not None and lead_excel.additional_comment != "":
            lead_db.additional_comment = lead_excel.additional_comment

        if lead_excel.remarks is not None and lead_excel.remarks != "":
            lead_db.remarks = lead_excel.remarks

        lead_db.save()
    except Exception as e:
        print('Error while updating: ' + str(lead_excel))
        print(traceback.format_exc())


def get_lead(request, lead):
    fields = lead.split(',')

    primary_phone = get_mobile_number(fields[2].split(':')[1])
    if primary_phone is None:
        raise Exception('Invalid phone number')

    return LeadModel(
        lead_id=fields[0].split(':')[1],
        name=fields[1].split(':')[1],
        phone=primary_phone,
        email_id=fields[3].split(':')[1],
        availability_status=lead.split(',availability_status:')[1].split(',job_category:')[0],
        job_category=lead.split(',job_category:')[1].split(',lead_in_date:')[0],

        # YYYY-MM-DD
        lead_in_date=None if lead.split(',lead_in_date:')[1].split(',requirement_start_time:')[0] == 'None' else
        lead.split(',lead_in_date:')[1].split(',requirement_start_time:')[0].split(' ')[0],

        requirement_start_time=None if lead.split(',requirement_start_time:')[1].split(',requirement_end_time:')[
                                           0] == 'None' else
        lead.split(',requirement_start_time:')[1].split(',requirement_end_time:')[0],

        requirement_end_time=None if lead.split(',requirement_end_time:')[1].split(',society:')[0] == 'None' else
        lead.split(',requirement_end_time:')[1].split(',society:')[0],

        society=lead.split(',society:')[1].split(',flat_number:')[0],
        flat_number=lead.split(',flat_number:')[1].split(',form_fill_status:')[0],
        form_fill_status=lead.split(',form_fill_status:')[1].split(',lead_status:')[0],
        lead_status=lead.split(',lead_status:')[1].split(',helper_name:')[0],
        helper_name=lead.split(',helper_name:')[1].split(',helper_no:')[0],
        helper_no=lead.split(',helper_no:')[1].split(',actual_status:')[0],
        actual_status=lead.split(',actual_status:')[1].split(',lead_lost_reason:')[0],
        lead_lost_reason=lead.split(',lead_lost_reason:')[1].split(',lead_placement_date:')[0],

        # YYYY-MM-DD
        lead_placement_date=None if lead.split(',lead_placement_date:')[1].split(',exit_date:')[0] == 'None' else
        lead.split(',lead_placement_date:')[1].split(',exit_date:')[0].split(' ')[0],

        # YYYY-MM-DD
        exit_date=None if lead.split(',exit_date:')[1].split(',identity_type:')[0] == 'None' else
        lead.split(',exit_date:')[1].split(',identity_type:')[0].split(' ')[0],

        identity_type=lead.split(',identity_type:')[1].split(',identity_status:')[0],
        identity_status=lead.split(',identity_status:')[1].split(',identity_shared:')[0],
        identity_shared=lead.split(',identity_shared:')[1].split(',application_form:')[0],
        application_form=lead.split(',application_form:')[1].split(',duration:')[0],
        duration=lead.split(',duration:')[1].split(',payment_date:')[0],

        # YYYY-MM-DD
        payment_date=None if lead.split(',payment_date:')[1].split(',payment_status:')[0] == 'None' else lead.split(',payment_date:')[1].split(',payment_status:')[0].split(' ')[0],

        payment_status=lead.split(',payment_status:')[1].split(',payment_mode:')[0],
        payment_mode=lead.split(',payment_mode:')[1].split(',salary:')[0],
        salary=lead.split(',salary:')[1].split(',third_party:')[0],
        third_party=lead.split(',third_party:')[1].split(',commission:')[0],
        commission=lead.split(',commission:')[1].split(',lead_source:')[0],
        lead_source=lead.split(',lead_source:')[1].split(',sales_person:')[0],
        sales_person=lead.split(',sales_person:')[1].split(',additional_comment:')[0],
        additional_comment=lead.split(',additional_comment:')[1].split(',remarks:')[0],
        remarks=lead.split(',remarks:')[1],
        admin_user=request.user,
    )


def create_lead(request, lead, lead_id):
    primary_phone = get_mobile_number(str(lead[1]))
    if primary_phone is None:
        raise Exception('Invalid phone number')

    return LeadModel(
        lead_id=lead_id,
        name=lead[0],
        phone=primary_phone,
        email_id=lead[2],
        availability_status=lead[3],
        job_category=lead[4],
        lead_in_date=lead[5],
        requirement_start_time=lead[6],
        requirement_end_time=lead[7],
        society=lead[8],
        flat_number=lead[9],
        form_fill_status=lead[10],
        lead_status=lead[11],
        helper_name=lead[12],
        helper_no=lead[13],
        actual_status=lead[14],
        lead_lost_reason=lead[15],
        lead_placement_date=lead[16],
        exit_date=lead[17],
        identity_type=lead[18],
        identity_status=lead[19],
        identity_shared=lead[20],
        application_form=lead[21],
        duration=lead[22],
        payment_date=lead[23],
        payment_status=lead[24],
        payment_mode=lead[25],
        salary=lead[26],
        third_party=lead[27],
        commission=lead[28],
        lead_source=lead[29],
        sales_person=lead[30],
        additional_comment=lead[31],
        remarks=lead[32],
        admin_user=request.user,
    )


@login_required
def ExcelFileHelperFileDuplicateAcceptView(request):
    if request.method == 'POST':
        duplicates = request.POST.get('duplicates_entries')
        duplicates = duplicates[1:-1]
        helpers = duplicates.split('<HelperModel: ')
        for duplicate in helpers:
            if duplicate != "":
                duplicates = duplicates[:-1]
                helper_excel = get_helper(request, duplicate.split('>')[0])
                helper_db = HelperModel.objects.get(primary_phone=helper_excel.primary_phone)
                update_helper(helper_excel, helper_db)
        messages.success(request, 'Helpers updated successfully!')
        request.method = 'GET'

    return HelperListViews(request)


def update_helper(helper_excel, helper_db):
    try:
        if helper_excel.helper_status is not None:
            helper_db.helper_status = helper_excel.helper_status

        if helper_excel.first_name is not None and helper_excel.last_name != '':
            helper_db.first_name = helper_excel.first_name

        if helper_excel.middle_name is not None and helper_excel.middle_name != '':
            helper_db.middle_name = helper_excel.middle_name

        if helper_excel.last_name is not None and helper_excel.last_name != '':
            helper_db.last_name = helper_excel.last_name

        if helper_excel.primary_phone is not None and helper_excel.primary_phone != "":
            helper_db.primary_phone = helper_excel.primary_phone

        if helper_excel.job_role_2 is not None and helper_excel.job_role_2 != "":
            helper_db.job_role_2 = helper_excel.job_role_2

        if helper_excel.availability_status is not None and helper_excel.availability_status != "":
            helper_db.availability_status = helper_excel.availability_status

        if helper_excel.helper_locality is not None and helper_excel.helper_locality != "":
            helper_db.helper_locality = helper_excel.helper_locality

        if helper_excel.society is not None and helper_excel.society != "":
            helper_db.society = helper_excel.society

        if helper_excel.listed_by is not None and helper_excel.listed_by != "":
            helper_db.listed_by = helper_excel.listed_by

        if helper_excel.language_known is not None and helper_excel.language_known != "":
            helper_db.language_known = helper_excel.language_known

        if helper_excel.age is not None and helper_excel.age != "":
            helper_db.age = helper_excel.age

        if helper_excel.gender is not None and helper_excel.gender != "":
            helper_db.gender = helper_excel.gender

        if helper_excel.sunday is not None and helper_excel.sunday != "":
            helper_db.sunday = helper_excel.sunday

        if helper_excel.smartphone is not None and helper_excel.smartphone != "":
            helper_db.smartphone = helper_excel.smartphone

        if helper_excel.whatsApp is not None and helper_excel.whatsApp != "":
            helper_db.whatsApp = helper_excel.whatsApp

        if helper_excel.start_time_1 is not None and helper_excel.start_time_1 != '':
            helper_db.start_time_1 = helper_excel.start_time_1

        if helper_excel.end_time_1 is not None and helper_excel.end_time_1 != '':
            helper_db.end_time_1 = helper_excel.end_time_1

        if helper_excel.start_time_2 is not None and helper_excel.start_time_2 != "":
            helper_db.start_time_2 = helper_excel.start_time_2

        helper_db.update_date = datetime.now()

        if helper_excel.end_time_2 is not None and helper_excel.end_time_2 != '':
            helper_db.end_time_2 = helper_excel.end_time_2

        if helper_excel.start_time_3 is not None and helper_excel.start_time_3 != '':
            helper_db.start_time_3 = helper_excel.start_time_3

        if helper_excel.end_time_3 is not None and helper_excel.end_time_3 != '':
            helper_db.end_time_3 = helper_excel.end_time_3

        if helper_excel.start_time_4 is not None and helper_excel.start_time_4 != '':
            helper_db.start_time_4 = helper_excel.start_time_4

        if helper_excel.end_time_4 is not None and helper_excel.end_time_4 != '':
            helper_db.end_time_4 = helper_excel.end_time_4

        if helper_excel.charges is not None and helper_excel.charges != '':
            helper_db.charges = helper_excel.charges

        if helper_excel.preferences is not None and helper_excel.preferences != '':
            helper_db.preferences = helper_excel.preferences

        if helper_excel.id_proof_status is not None and helper_excel.id_proof_status != '':
            helper_db.id_proof_status = helper_excel.id_proof_status

        if helper_excel.aadhar_verification is not None and helper_excel.aadhar_verification != '':
            helper_db.aadhar_verification = helper_excel.aadhar_verification

        if helper_excel.id_pdf is not None and helper_excel.id_pdf != '':
            helper_db.id_pdf = helper_excel.id_pdf

        if helper_excel.other_id_proof is not None and helper_excel.other_id_proof != '':
            helper_db.other_id_proof = helper_excel.other_id_proof

        if helper_excel.police_verification is not None and helper_excel.police_verification != '':
            helper_db.police_verification = helper_excel.police_verification

        if helper_excel.engagement_date is not None and helper_excel.engagement_date != '':
            helper_db.engagement_date = helper_excel.engagement_date

        if helper_excel.previous_employer_name is not None and helper_excel.previous_employer_name != '':
            helper_db.previous_employer_name = helper_excel.previous_employer_name

        if helper_excel.previous_employer_contact is not None and helper_excel.previous_employer_contact != '':
            helper_db.previous_employer_contact = helper_excel.previous_employer_contact

        if helper_excel.previous_employer_society is not None and helper_excel.previous_employer_society != '':
            helper_db.previous_employer_society = helper_excel.previous_employer_society

        if helper_excel.rating is not None and helper_excel.rating != '':
            helper_db.rating = helper_excel.rating

        if helper_excel.remarks is not None and helper_excel.remarks != '':
            helper_db.remarks = helper_excel.remarks

        if helper_excel.additional_comment is not None and helper_excel.additional_comment != '':
            helper_db.additional_comment = helper_excel.additional_comment

        if helper_excel.attempt_2 is not None and helper_excel.attempt_2 != '':
            helper_db.attempt_2 = helper_excel.attempt_2

        helper_db.save()
    except Exception as e:
        print('Error while updating: ' + str(helper_excel))
        print(traceback.format_exc())


@login_required
def ExcelFileLocalityFileView(request):
    localityall = Localities.objects.all()
    if request.method == 'POST':
        data_set = Dataset()
        myfile = request.FILES['myfile']

        # check excel file or not!
        if not myfile.name.endswith('xlsx'):
            messages.error(request, 'Excel file only allow!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                # all excel data store in 'excel_data' in form of table
                excel_data = data_set.load(myfile.read(), format='xlsx')
                for i in excel_data:
                    # row fully empty or not check
                    if (i[0] == None or i[0] == ''):
                        pass
                    else:
                        if Localities.objects.filter(name=i[0]).exists():
                            pass
                        localities = Localities(
                            name=i[0]
                        )
                        localities.save()
                # if all right then success message
                messages.success(request, 'file upload successful!')
            except Exception as e:
                # exception handle
                messages.error(request, f'There is an error!')
            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'locality_excel.html', {'localityall': localityall})


@login_required
def ExcelFilejob_category_upload(request):
    job_catsall = JobCat.objects.all()
    if request.method == 'POST':
        data_set = Dataset()
        myfile = request.FILES['myfile']

        # check excel file or not!
        if not myfile.name.endswith('xlsx'):
            messages.error(request, 'Excel file only allow!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                # all excel data store in 'excel_data' in form of table
                excel_data = data_set.load(myfile.read(), format='xlsx')
                for i in excel_data:
                    # row fully empty or not check
                    if (i[0] == None or i[0] == ''):
                        pass
                    else:
                        if JobCat.objects.filter(name=i[0]).exists():
                            pass
                        else:
                            job_cat = JobCat(
                                name=i[0]
                            )
                            job_cat.save()
                # if all right then success message
                messages.success(request, 'file upload successful!')
            except IntegrityError as e:
                messages.error(
                    request, f'Duplicate entries find in your excel file')
            except Exception as e:
                # exception handle
                print(f'There is an error! ')
                messages.error(request, f'There is an error!')
                # redirect with same page
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'job_cat_excel.html', {'job_cat': job_catsall})


@login_required
def ExcelFileSkillsFileView(request):
    skillsall = Skills.objects.all()
    if request.method == 'POST':
        data_set = Dataset()
        myfile = request.FILES['myfile']

        # check excel file or not!
        if not myfile.name.endswith('xlsx'):
            messages.error(request, 'Excel file only allow!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            try:
                # all excel data store in 'excel_data' in form of table
                excel_data = data_set.load(myfile.read(), format='xlsx')
                for i in excel_data:
                    # row fully empty or not check
                    if (i[0] == None or i[0] == ''):
                        pass
                    else:
                        if Skills.objects.filter(name=i[0]).exists():
                            pass
                        else:
                            skills = Skills(
                                name=i[0]
                            )
                            skills.save()
                # if all right then success message
                messages.success(request, 'file upload successful!')
            except IntegrityError as e:
                messages.error(
                    request, f'Duplicate entries find in your excel file')
            except Exception as e:
                # exception handle
                print(f'There is an error! ')
                messages.error(request, f'There is an error!')
                # redirect with same page
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'skills_excel.html', {'skills': skillsall})


# helper delete


@login_required
def HelperDeleteView(request, id):
    data = HelperModel.objects.get(id=id)

    current_datetime = datetime.now()
    helper_history = HelperHistoryModel(
        helper_id=data.helper_id,
        first_name=data.first_name,
        middle_name=data.middle_name,
        last_name=data.last_name,
        primary_phone=data.primary_phone,
        email_id=data.email_id,
        dob=data.dob,
        create_date=data.create_date,
        update_date=current_datetime.today(),
        admin_user=request.user,
        history_status='delete'
    )

    helper_history.save()
    HistoryModel(helper=helper_history, date=current_datetime.today()).save()
    data.delete()

    messages.warning(request, "Data remove successfully!")
    return HelperListViews(request)


# helper  update
@login_required
def HelperEditView(request, id):
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
        job_cat = JobCat.objects.all()
    except:
        # exception handle
        messages.error(
            request, 'Something error try again! may be network issue!')

    # all model object get as of our requirement
    helper = HelperModel.objects.get(id=id)
    helper_skill = HelperSkillSetModel.objects.filter(helper=helper)
    helper_additional_skill = HelperAdditionalSkillSetModel.objects.filter(
        helper=helper)
    helper_language = HelperPreferredLanguageModel.objects.filter(
        helper=helper)
    job_role = HelperJobRoleModel.objects.filter(helper=helper)

    fm = HelperEditForm(instance=helper)  # form

    if request.method == "POST":
        # all additional input get
        skill_inp = request.POST.getlist('skill')
        add_skill_inp = request.POST.getlist('ad-skill')
        language_inp = request.POST.getlist('language')
        job_role_inp = request.POST.getlist('job_role')
        id_pdf = request.FILES.get('id_pdf')

        fm = HelperEditForm(request.POST, request.FILES,
                            instance=helper)  # all input value

        # language empty or not check
        language_inpIsEmpty = False
        for i in language_inp:
            if i.strip() != "":
                language_inpIsEmpty = True
                break

        # if language all are empty under the code not executed
        if (not language_inpIsEmpty):
            messages.error(request, "language must mandatory!")
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
                if i.strip() != "":
                    HelperSkillSetModel(helper=helper, skill=i.strip()).save()

            # additional skill update
            for i in add_skill_inp:
                if i.strip() != "":
                    HelperAdditionalSkillSetModel(
                        helper=helper, additional_skill=i.strip()).save()

            # language update
            for i in language_inp:
                if i.strip() != "":
                    HelperPreferredLanguageModel(
                        helper=helper, language=i.strip()).save()

            # language update
            for i in job_role_inp:
                if i.strip() != "":
                    HelperJobRoleModel(helper=helper, job=i.strip()).save()

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
            if not HelperHistoryModel.objects.filter(Q(helper_id=data.helper_id) & Q(history_status='update')).exists():
                helper_history = HelperHistoryModel(
                    helper_id=data.helper_id,
                    first_name=data.first_name,
                    middle_name=data.middle_name,
                    last_name=data.last_name,
                    primary_phone=data.primary_phone,
                    email_id=data.email_id,
                    dob=data.dob,
                    create_date=data.create_date,
                    update_date=current_datetime.today(),
                    admin_user=request.user,
                    history_status='update'
                )

                helper_history.save()

                HistoryModel(
                    helper=HelperHistoryModel.objects.get(
                        Q(helper_id=data.helper_id) & Q(history_status='update')),
                    date=current_datetime
                ).save()

            else:
                helper_history = HelperHistoryModel.objects.filter(
                    Q(helper_id=data.helper_id) & Q(history_status='update'))
                helper_history.update(
                    helper_id=data.helper_id,
                    first_name=data.first_name,
                    middle_name=data.middle_name,
                    last_name=data.last_name,
                    primary_phone=data.primary_phone,
                    email_id=data.email_id,
                    dob=data.dob,
                    create_date=data.create_date,
                    update_date=current_datetime.today(),
                    admin_user=request.user,
                    history_status='update'
                )
                HistoryModel.objects.filter(helper=HelperHistoryModel.objects.get(
                    Q(helper_id=data.helper_id) & Q(history_status='update'))).update(
                    helper=HelperHistoryModel.objects.get(
                        Q(helper_id=data.helper_id) & Q(history_status='update')),
                    date=current_datetime
                )

            messages.success(request, 'Data updated successfully!')
        else:
            messages.error(request, 'please enter valid data!')

    data = {
        'fm': fm,
        'skill': helper_skill,
        'additional_skill': helper_additional_skill,
        'helper_language': helper_language,
        'job_role': HelperJobRoleModel.objects.filter(helper=helper),
        'locations': location_values,
        'locality': helper.locality,
        'job_cat': job_cat
    }
    return render(request, 'helper_edit.html', data)


# helper phone exist or not logic


@login_required
def HelperPhoneNoValidateDetailsView(request, id):
    helper = HelperModel.objects.get(id=id)
    data = {
        'helper': helper,
        'language': HelperPreferredLanguageModel.objects.filter(helper=helper),
        'skill': HelperSkillSetModel.objects.filter(helper=helper),
        'additional_skill': HelperAdditionalSkillSetModel.objects.filter(helper=helper),
        'job_role': HelperJobRoleModel.objects.filter(helper=helper),
    }
    return render(request, 'helper_valid_check.html', data)


# accept helper


@login_required
def HelperPhoneNoValidateAcceptView(request, id):
    helper = HelperModel.objects.get(id=id)
    helper.phone_valid = False
    helper.save()
    return redirect('home')


# reject helper


@login_required
def HelperPhoneNoValidateRejectedView(request, id):
    helper = HelperModel.objects.get(id=id)
    helper.delete()
    return redirect('home')


# lead random id generate
def lead_generate_id(id):
    # Generate a random number
    random_num = str(id + 1000000000).encode()

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

        leads = LeadModel.objects.all().order_by('-create_date')
    except:
        # exception handle
        messages.error(
            request, 'Something error try again! may be network issue!')

    data = {
        'data': leads,
        'length': len(leads)
    }
    return render(request, 'lead_list.html', data)


# lead details show
@login_required
def LeadDetailsView(request, no):
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
            'name': leads.name,
            'phone': leads.phone,
            'email': leads.email_id,
            'addr': leads.address,
            'id': leads.lead_id,
            'locality': leads.locality,
            'near_by': leads.near_by,
            'availability': leads.availability_status
        }
    except:
        # exception handle
        messages.error(
            request, 'Something error try again! may be network issue!')

    return render(request, 'lead_details.html', data)


# update the lead


@login_required
def LeadEditView(request, no):
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
        job_cat = JobCat.objects.all()
    except:
        # exception handle
        messages.error(
            request, 'Something error try again! may be network issue!')

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
        excluded_roles = ['nanny', ' housekeeper', ' caregiver']
        included_roles = [
            role for role in job_category if role not in excluded_roles]

        data = {
            'name': leads.name,
            'phone': leads.phone,
            'email': leads.email_id,
            'addr': leads.address,
            'locality': leads.locality,
            'near_by': leads.near_by,
            'availability': leads.availability_status,
            'locations': location_values,
            'flat_number': leads.flat_number,
            'lead_req_date': leads.lead_req_date,
            'lead_placement_date': leads.lead_placement_date,
            'lead_status2': leads.lead_status2,
            'additional_comment': leads.additional_comment,
            'job_role': leads.job_category,
            'other_roles': ', '.join(included_roles),
            'lead_source': leads.lead_source,
            'role_on_demand_start_date': leads.role_on_demand_start_date,
            'role_on_demand_start_from_time': leads.role_on_demand_start_from_time,
            'role_on_demand_start_to_time': leads.role_on_demand_start_to_time,
            'role_on_demand_end_date': leads.role_on_demand_end_date,
            'role_on_demand_end_from_time': leads.role_on_demand_end_from_time,
            'role_on_demand_end_to_time': leads.role_on_demand_end_to_time,
            'job_cat': job_cat
        }

        # POST
        if request.method == "POST":

            # all value get by input in lead_edit.html
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            addr = request.POST['addr']
            locality = request.POST['locality']
            near_by = request.POST.get('near_by', False)
            availability = request.POST['availability']
            flat_number = request.POST['flat_num']
            lead_req_date = request.POST['LeadRequirementDate']
            lead_placement_date = request.POST['LeadPlacementDate']
            lead_status = request.POST['LeadStatus']
            additional_comment = request.POST['AdditionalComment']
            job_role = ', '.join(request.POST.getlist('job_role'))
            lead_source = request.POST['LeadSource']

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
            if LeadModel.objects.get(id=no):
                lead_data_all = LeadModel.objects.get(id=no)
                lead_data_all.lead_id = leads.lead_id
                lead_data_all.name = name
                lead_data_all.phone = phone
                lead_data_all.email_id = email
                lead_data_all.address = addr
                lead_data_all.availability_status = availability
                lead_data_all.locality = locality
                lead_data_all.near_by = near_by
                lead_data_all.lead_status = "pending"
                lead_data_all.flat_number = flat_number
                lead_data_all.lead_req_date = lead_req_date
                lead_data_all.lead_placement_date = lead_placement_date
                lead_data_all.lead_status2 = lead_status
                lead_data_all.lead_source = lead_source
                lead_data_all.additional_comment = additional_comment
                lead_data_all.job_category = job_role
                if request.POST['Start_Date'] != '':
                    lead_data_all.role_on_demand_start_date = request.POST['Start_Date']
                    lead_data_all.role_on_demand_start_from_time = request.POST.get(
                        's_StartDuration')
                    lead_data_all.role_on_demand_start_to_time = request.POST.get(
                        's_EndDuration')
                    lead_data_all.role_on_demand_end_date = request.POST['End_Date']
                    lead_data_all.role_on_demand_end_from_time = request.POST.get(
                        'e_StartDuration')
                    lead_data_all.role_on_demand_end_to_time = request.POST.get(
                        'e_EndDuration')
                lead_data_all.save()
            # lead_history model
            if not leadHistoryModel.objects.filter(Q(lead_id=leads.lead_id) & Q(history_status='update')).exists():
                lead_history = leadHistoryModel(
                    lead_id=leads.lead_id,
                    name=name,
                    phone=phone,
                    email=email,
                    admin_user=request.user,
                    history_status='update'
                )
                lead_history.save()

                # history model
                HistoryModel(lead=lead_history).save()

            else:
                lead_history = leadHistoryModel.objects.filter(
                    Q(lead_id=leads.lead_id) & Q(history_status='update'))
                lead_history.update(
                    lead_id=leads.lead_id,
                    name=name,
                    phone=phone,
                    email=email,
                    admin_user=request.user,
                    history_status='update'
                )

                HistoryModel.objects.filter(
                    lead=leadHistoryModel.objects.get(Q(lead_id=leads.lead_id) & Q(history_status='update'))).update(
                    lead=leadHistoryModel.objects.get(
                        Q(lead_id=leads.lead_id) & Q(history_status='update')),
                    date=current_datetime.today()
                )

            # message to success
            messages.success(request, 'Data updated successful!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:

        messages.error(
            request, f'Something error try again! may be network issue!')
    return render(request, 'lead_edit.html', data)


@login_required
def SkillEditView(request, id):
    data = {}
    try:
        current_datetime = datetime.now()

        skillall = Skills.objects.get(id=id)

        data = {
            'name': skillall.name,

        }

        # POST
        if request.method == "POST":

            # all value get by input in lead_edit.html
            name = request.POST['skll_name']

            if Skills.objects.get(id=id):
                skillall.name = name
                skillall.save()

            # message to success
            messages.success(request, 'Data updated successful!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:

        messages.error(
            request, f'Something error try again! may be network issue!')
    return render(request, 'skills_edit.html', data)


@login_required
def SkilladdView(request):
    data = {}
    try:
        current_datetime = datetime.now()

        data = {

        }

        # POST
        if request.method == "POST":
            # all value get by input in lead_edit.html
            name = request.POST['skll_name']

            skill = Skills(name=name)
            skill.save()

            # message to success
            messages.success(request, 'Data updated successful!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:

        messages.error(
            request, f'Something error try again! may be network issue!')
    return render(request, 'skills_add.html', data)


@login_required
def job_categoryEditView(request, id):
    data = {}
    try:
        current_datetime = datetime.now()

        job_catall = JobCat.objects.get(id=id)

        data = {
            'name': job_catall.name,

        }

        # POST
        if request.method == "POST":

            # all value get by input in lead_edit.html
            name = request.POST['job_cat_name']

            if JobCat.objects.get(id=id):
                job_catall.name = name
                job_catall.save()

            # message to success
            messages.success(request, 'Data updated successful!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:

        messages.error(
            request, f'Something error try again! may be network issue!')
    return render(request, 'job_catall_edit.html', data)


@login_required
def job_categoryaddView(request):
    data = {}
    try:
        current_datetime = datetime.now()

        data = {

        }

        # POST
        if request.method == "POST":
            # all value get by input in lead_edit.html
            name = request.POST['job_cat_name']

            job_catall = JobCat(name=name)
            job_catall.save()

            # message to success
            messages.success(request, 'Data updated successful!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:

        messages.error(
            request, f'Something error try again! may be network issue!')
    return render(request, 'job_catall_add.html', data)


@login_required
def localityEditView(request, id):
    data = {}
    try:
        current_datetime = datetime.now()

        locality = Localities.objects.get(id=id)

        data = {
            'name': locality.name,

        }

        # POST
        if request.method == "POST":

            # all value get by input in lead_edit.html
            name = request.POST['loc_name']

            if Localities.objects.get(id=id):
                locality.name = name
                locality.save()

            # message to success
            messages.success(request, 'Data updated successful!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:

        messages.error(
            request, f'Something error try again! may be network issue!')
    return render(request, 'locality_edit.html', data)


@login_required
def localityaddView(request):
    data = {}
    try:
        current_datetime = datetime.now()

        data = {

        }

        # POST
        if request.method == "POST":
            # all value get by input in lead_edit.html
            name = request.POST['loc_name']

            locality = Localities(name=name)
            locality.save()

            # message to success
            messages.success(request, 'Data updated successful!')

            # redirect with same page
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:

        messages.error(
            request, f'Something error try again! may be network issue!')
    return render(request, 'locality_add.html', data)


@login_required
def job_categoryDeleteView(request, id):
    try:
        current_datetime = datetime.now()

        job_cat = JobCat.objects.get(id=id)

        # delete the row by help of row num
        job_cat.delete()

        # success message
        messages.success(request, 'data remove successful!')
    except:
        # exception handle
        messages.error('Data not to be deleted something error try again!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def SkillDeleteView(request, id):
    try:
        current_datetime = datetime.now()

        skill = Skills.objects.get(id=id)

        # delete the row by help of row num
        skill.delete()

        # success message
        messages.success(request, 'data remove successful!')
    except:
        # exception handle
        messages.error('Data not to be deleted something error try again!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def localityDeleteView(request, id):
    try:
        current_datetime = datetime.now()

        locality = Localities.objects.get(id=id)

        # delete the row by help of row num
        locality.delete()

        # success message
        messages.success(request, 'data remove successful!')
    except:
        # exception handle
        messages.error('Data not to be deleted something error try again!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# delete data from sheet


@login_required
def LeadDeleteView(request, no):
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
            lead_id=id,
            name=name,
            phone=phone,
            email=email,
            admin_user=request.user,
            update_date=current_datetime.today(),
            history_status='delete'
        )
        lead_history.save()

        # history
        HistoryModel(
            lead=lead_history
        ).save()

        # delete the row by help of row num
        leads.delete()

        # success message
        messages.success(request, 'data remove successful!')
        return LeadList(request)
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
        job_cat = JobCat.objects.all()
    except:
        # exception handle
        messages.error(
            request, 'Some error try again! may be network issue!')

    data = {
        'locations': location_values,
        'job_cat': job_cat
    }
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
            near_by = request.POST.get('near_by', False)
            availability = request.POST['availability']
            flat_number = request.POST['flat_num']
            if request.POST['LeadRequirementDate'] != '':
                try:
                    lead_req_date = datetime.date.fromisoformat(request.POST['LeadRequirementDate'])
                except Exception as e:
                    messages.warning(request, 'Ignored invalid data for, LeadRequirementDate.')
                    print('LeadRequirementDate: Invalid date format!' + e.__str__())
                    lead_req_date = None
            else:
                lead_req_date = None

            if request.POST['LeadPlacementDate'] != '':
                try:
                    lead_placement_date = datetime.date.fromisoformat(request.POST['LeadPlacementDate'])
                except Exception as e:
                    messages.warning(request, 'Ignored invalid data for, LeadPlacementDate.')
                    print('LeadPlacementDate: Invalid date format!' + e.__str__())
                    lead_placement_date = None
            else:
                lead_placement_date = None

            lead_status = request.POST['LeadStatus']
            additional_comment = request.POST['AdditionalComment']
            job_role = ', '.join(request.POST.getlist('job_role'))
            lead_source = request.POST['LeadSource']
            # id generate
            leads = LeadModel.objects.all()
            id = lead_generate_id(leads.count() + 20)

            # near_by field
            if near_by == 'on':
                near_by = True

            # all value in list format
            lst = [name, phone, email, addr, " ", " ", " ",
                   "pending", id, locality, near_by, availability]

            # row append in sheet
            # current_sheet.append_row(lst)

            # notification
            lead = id
            employee = request.user
            msg = "pending message"
            status = "pending"
            LeadStatusNotificationModel(
                lead=lead,
                employee=employee,
                status=status,
                msg=msg
            ).save()

            # lead_history mode
            lead_history = leadHistoryModel(
                lead_id=id,
                name=name,
                phone=phone,
                email=email,
                admin_user=request.user,
                history_status='create'
            )
            lead_history.save()
            # main lead model
            lead_data_all = LeadModel(
                lead_id=id,
                name=name,
                phone=phone,
                email_id=email,
                address=addr,
                availability_status=availability,
                # locality
                locality=locality,
                near_by=near_by,
                lead_status="pending",
                admin_user=request.user,
                flat_number=flat_number,
                lead_req_date=lead_req_date,
                lead_placement_date=lead_placement_date,
                lead_status2=lead_status,
                lead_source=lead_source,
                additional_comment=additional_comment,
                job_category=job_role)
            if request.POST['Start_Date'] != '':
                try:
                    lead_data_all.role_on_demand_start_date = datetime.date.fromisoformat(request.POST['Start_Date'])
                except Exception as e:
                    messages.warning(request, 'Ignored invalid data for, Start_Date.')
                    print('Start_Date: Invalid data, ' + request.POST['Start_Date'])
                    lead_data_all.role_on_demand_start_date = None

                try:
                    lead_data_all.role_on_demand_start_from_time = datetime.time.fromisoformat(request.POST.get('s_StartDuration'))
                except Exception as e:
                    messages.warning(request, 'Ignored invalid data for, s_StartDuration.')
                    print('s_StartDuration: Invalid data, ' + request.POST['s_StartDuration'])
                    lead_data_all.role_on_demand_start_from_time = None

                try:
                    lead_data_all.role_on_demand_start_to_time = datetime.time.fromisoformat(request.POST.get('s_EndDuration'))
                except Exception as e:
                    messages.warning(request, 'Ignored invalid data for, s_StartDuration.')
                    print('s_EndDuration: Invalid data, ' + request.POST['s_EndDuration'])
                    lead_data_all.role_on_demand_start_to_time = None

                try:
                    lead_data_all.role_on_demand_end_date = datetime.date.fromisoformat(request.POST['End_Date'])
                except Exception as e:
                    messages.warning(request, 'Ignored invalid data for, End_Date.')
                    print('End_Date: Invalid data, ' + request.POST['End_Date'])
                    lead_data_all.role_on_demand_end_date = None

                try:
                    lead_data_all.role_on_demand_end_from_time = datetime.time.fromisoformat(request.POST.get('e_StartDuration'))
                except Exception as e:
                    messages.warning(request, 'Ignored invalid data for, e_StartDuration.')
                    print('e_StartDuration: Invalid data, ' + request.POST['e_StartDuration'])
                    lead_data_all.role_on_demand_end_from_time = None

                try:
                    lead_data_all.role_on_demand_end_to_time = datetime.time.fromisoformat(request.POST.get('e_EndDuration'))
                except Exception as e:
                    messages.warning(request, 'Ignored invalid data for, e_EndDuration.')
                    print('e_EndDuration: Invalid data, ' + request.POST['e_EndDuration'])
                    lead_data_all.role_on_demand_end_to_time = None
            print('Saving: ' + str(lead_data_all))
            lead_data_all.save()

            # history model
            HistoryModel(
                lead=lead_history,
            ).save()

            messages.success(request, "Data add successful!")
            return LeadList(request)
        except Exception as e:
            messages.error(request, f'Invalid Lead. Error:' + e.__str__())
            print(traceback.format_exc())
            data = {
                'lead': lead_data_all
            }
            return render(request, 'lead_add.html', data)

    return render(request, 'lead_add.html', data)


@login_required
def LeadStatusUpdateView(request, row):
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

        messages.success(request, "Data update successful.!")
    except:
        # exception handle
        messages.error(
            request, 'Something error try again! may be network issue!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def HistoryView(request):
    data = {
        'data': HistoryModel.objects.all().order_by('-date')
    }
    return render(request, 'history.html', data)


def HistoryDetailsView(request, id):
    data = {
        'data': HistoryModel.objects.get(id=id)
    }
    return render(request, "history_details.html", data)
