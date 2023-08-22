from django import forms
from .models import *

class HelperForm(forms.ModelForm):
    class Meta:
        model = HelperModel
        fields = ['first_name','middle_name','last_name','primary_phone','secondary_phone',
                  'email_id','dob','street','city','zipcode','state','country','work_experience','availability_status','availability_status_week','additional_comment',
                  'locality','near_by','id_pdf','call_status','id_type'
                  
                  ]
        widgets = {
          
            'last_name': forms.DateTimeInput(attrs={'class': 'form-control my-2'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'primary_phone': forms.TextInput(attrs={'class': 'form-control my-2','maxlength':'10','pattern':'[1-9]{1}[0-9]{9}', 'title':'Please enter exactly 10 digits'}),
            'secondary_phone': forms.TextInput(attrs={'class': 'form-control my-2','maxlength':'10','pattern':'[1-9]{1}[0-9]{9}','title':'Please enter exactly 10 digits'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control my-2'}),
            'street': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'city': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control my-2'}),
            'state': forms.Select(attrs={'class': 'form-control my-2'}),
            'country': forms.Select(attrs={'class': 'form-control my-2'}),
            'availability_status_week': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'availability_status': forms.Select(attrs={'class': 'form-control my-2'}),
            'work_experience': forms.Select(attrs={'class': 'form-control my-2'}),
            'additional_comment':forms.Textarea(attrs={'class': 'form-control my-2','rows':'2'}),
            'additional_comment':forms.Textarea(attrs={'class': 'form-control my-2','rows':'2'}),
            'locality':forms.Select(attrs={'class': 'form-control my-2','rows':'2'}),
            'near_by':forms.CheckboxInput(attrs={'class': 'mb-4'}),
            'dob':forms.DateInput(attrs={'class': 'form-control my-2','type':'date','rows':'2'}),
            'id_pdf':forms.FileInput(attrs={'class': 'form-control my-2','accept':'.pdf','required':'required','rows':'2'}),
            'id_type':forms.Select(attrs={'class': 'form-control my-2','required':'required','rows':'2'}),
            'call_status':forms.Select(attrs={'class': 'form-control my-2','required':'required','rows':'2'}),
           
          
        }
        labels = {
            'first_name':"first name <b class='text-danger'>*</b>",
            'last_name':"last name <b class='text-danger'>*</b>",
            'primary_phone':"Primary Phone <b class='text-danger'>*</b>",
             'email_id':"Email id <b class='text-danger'>*</b>",
             'street':"Street <b class='text-danger'>*</b>",
             'city':"City <b class='text-danger'>*</b>",
            'zipcode':"Zipcode <b class='text-danger'>*</b>",
            'state':"State <b class='text-danger'>*</b>",
            'country':"Country <b class='text-danger'>*</b>",
            'work_experience':"Working experience <b class='text-danger'>*</b>",
            'availability_status_week':"Availability Status(weekly)<b class='text-danger'>*</b>",
            'additional_comment':"Additional comment <b class='text-danger'>*</b>",
            'near_by':" <b class='mb-4'>Near by</b>",
            'work_experience':" Work experience <b class='text-danger'>* </b>",
            'dob':" DOB <b class='text-danger'>* </b>",
            'availability_status':" Availability status <b class='text-danger'>* </b>",
            'locality':" Locality <b class='text-danger'>* </b>",
            'call_status':" Call status <b class='text-danger'>* </b>",
            'id_type':" <b class='mb-4'>id prove type <b class='text-danger'>*</b></b>",
            'id_pdf':" <b class='mb-4'>id file upload as pdf <b class='text-danger'>*</b></b>",
          
        }


class HelperEditForm(forms.ModelForm):
    class Meta:
        model = HelperModel
        fields = ['first_name','middle_name','last_name','primary_phone','secondary_phone',
                  'email_id','dob','street','city','zipcode','state','country','work_experience','availability_status','availability_status_week','additional_comment',
                  'locality','near_by','id_pdf','call_status','id_type'
                  
                  ]
        widgets = {
          
            'last_name': forms.DateTimeInput(attrs={'class': 'form-control my-2'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'primary_phone': forms.TextInput(attrs={'class': 'form-control my-2','maxlength':'10','pattern':'[1-9]{1}[0-9]{9}', 'title':'Please enter exactly 10 digits'}),
            'secondary_phone': forms.TextInput(attrs={'class': 'form-control my-2','maxlength':'10','pattern':'[1-9]{1}[0-9]{9}','title':'Please enter exactly 10 digits'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control my-2'}),
            'street': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'city': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control my-2'}),
            'state': forms.Select(attrs={'class': 'form-control my-2'}),
            'country': forms.Select(attrs={'class': 'form-control my-2'}),
            'availability_status_week': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'availability_status': forms.Select(attrs={'class': 'form-control my-2'}),
            'work_experience': forms.Select(attrs={'class': 'form-control my-2'}),
            'additional_comment':forms.Textarea(attrs={'class': 'form-control my-2','rows':'2'}),
            'additional_comment':forms.Textarea(attrs={'class': 'form-control my-2','rows':'2'}),
            'locality':forms.Select(attrs={'class': 'form-control my-2','rows':'2'}),
            'near_by':forms.CheckboxInput(attrs={'class': 'mb-4'}),
            'dob':forms.DateInput(attrs={'class': 'form-control my-2','type':'date','rows':'2'}),
            'id_pdf':forms.FileInput(attrs={'class': 'form-control my-2','accept':'.pdf','rows':'2'}),
            'id_type':forms.Select(attrs={'class': 'form-control my-2','required':'required','rows':'2'}),
            'call_status':forms.Select(attrs={'class': 'form-control my-2','required':'required','rows':'2'}),
          
        }
        labels = {
            'first_name':"first name <b class='text-danger'>*</b>",
            'last_name':"last name <b class='text-danger'>*</b>",
            'primary_phone':"Primary Phone <b class='text-danger'>*</b>",
             'email_id':"Email id <b class='text-danger'>*</b>",
             'street':"Street <b class='text-danger'>*</b>",
             'city':"City <b class='text-danger'>*</b>",
            'zipcode':"Zipcode <b class='text-danger'>*</b>",
            'state':"State <b class='text-danger'>*</b>",
            'country':"Country <b class='text-danger'>*</b>",
            'work_experience':"Working experience <b class='text-danger'>*</b>",
            'availability_status_week':"Availability Status(weekly)<b class='text-danger'>*</b>",
            'additional_comment':"Additional comment <b class='text-danger'>*</b>",
            'near_by':" <b class='mb-4'>Near by</b>",
            'work_experience':" Work experience <b class='text-danger'>* </b>",
            'dob':" DOB <b class='text-danger'>* </b>",
            'availability_status':" Availability status <b class='text-danger'>* </b>",
            'locality':" Locality <b class='text-danger'>* </b>",
            'call_status':" Call status <b class='text-danger'>* </b>",
            'id_type':" <b class='mb-4'>id prove type <b class='text-danger'>*</b></b>",
            'id_pdf':" <b class='mb-4'>id file upload as pdf <b class='text-danger'>*</b></b>",
          
        }

