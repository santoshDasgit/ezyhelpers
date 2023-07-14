from django.contrib import admin
from .models import *
# Register your models here.


# Lead model 
admin.site.register(LeadModel)
admin.site.register(LeadAdditionalDetailsModel)
admin.site.register(LeadPreferredLanguageModel)

