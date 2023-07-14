from django import forms
from .models import *

class LeadForm(forms.ModelForm):
    class Meta:
        model = LeadModel
        fields = ['first_name','middle_name','last_name','primary_phone','secondary_phone',
                  'email_id','street','city','zipcode','state','country','additional_comment'
                  
                  ]
        widgets = {
          
            'last_name': forms.DateTimeInput(attrs={'class': 'form-control my-2'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'primary_phone': forms.NumberInput(attrs={'class': 'form-control my-2','title':"Enter valid number",'pattern':"[1-9]{1}[0-9]{9}"}),
            'secondary_phone': forms.NumberInput(attrs={'class': 'form-control my-2','title':"Enter valid number",'pattern':"[1-9]{1}[0-9]{9}"}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control my-2'}),
            'street': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'city': forms.TextInput(attrs={'class': 'form-control my-2'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control my-2'}),
            'state': forms.Select(attrs={'class': 'form-control my-2'}),
            'country': forms.Select(attrs={'class': 'form-control my-2'}),
            'additional_comment':forms.Textarea(attrs={'class': 'form-control my-2','rows':'2'}),
           
          
           
          
        }
        # labels = {
        #     'lead_id':'',
        #     'contact_status':''
        # }