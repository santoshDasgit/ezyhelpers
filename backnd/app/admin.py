from django.contrib import admin
from .models import *
# Register your models here.

# Helper model 
admin.site.register(HelperModel)
admin.site.register(HelperAdditionalDetailsModel)
admin.site.register(HelperPreferredLanguageModel)

