from django.contrib import admin
from .models import *
# Register your models here.

# Helper model 
admin.site.register(HelperModel)
admin.site.register(HelperAdditionalSkillSetModel)
admin.site.register(HelperSkillSetModel)
admin.site.register(HelperPreferredLanguageModel)
admin.site.register(EmployeeModel)
admin.site.register(LeadStatusNotificationModel)
admin.site.register(HelperHistoryModel)
admin.site.register(leadHistoryModel)
admin.site.register(HistoryModel)
admin.site.register(HelperJobRoleModel)

