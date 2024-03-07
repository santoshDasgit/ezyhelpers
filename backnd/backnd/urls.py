from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import *
from .views_emp import *
from .views_super import *

urlpatterns = [

    # common for all
    path('admin/', admin.site.urls),
    path('', HomeView, name='home'),
    path('login/', LoginView, name="login"),
    path('logout/', LogoutView, name='logout'),
    path('profile/<id>', ProfileView, name='profile'),
    path('profile_update/<id>/<email>', ProfileUpdateView, name='profile_update'),
    path('email_validate_profile/<id>/<url>',
         EmailVerifyProfileView, name='email_validate_profile'),
    path('password_change/', PasswordChangedView, name='password_change'),

    path('helper_list', HelperListViews, name='helper_list'),
    path('helper_add/', HelperAddView, name='helper_add'),
    path('helper_view/<id>', HelperDetailsView, name='helper_view'),
    path('helper_status_update/<id>', HelperStatusUpdateView,
         name='helper_status_update'),
    path('excel_file_helper_upload', ExcelFileHelperFileView,
         name='excel_file_helper_upload'),
    path('excel_file_lead_upload', ExcelFileLeadFileView,
         name='excel_file_lead_upload'),
    path('excel_file_lead_upload_duplicate_accept', ExcelFileLeadFileDuplicateAcceptView,
         name='excel_file_lead_upload_duplicate_accept'),
    path('excel_file_locality_upload', ExcelFileLocalityFileView,
         name='excel_file_locality_upload'),
    path('excel_file_skill_upload', ExcelFileSkillsFileView,
         name='excel_file_skill_upload'),
    path('job_category_upload', ExcelFilejob_category_upload,
         name='job_category_upload'),
    path('job_category_Edit_View/<id>', job_categoryEditView,
         name='job_category_Edit_View'),
    path('job_category_add_View', job_categoryaddView, name='job_categoryaddView'),
    path('job_category_delete/<id>', job_categoryDeleteView,
         name='job_category_delete'),
    path('Skill_Edit_View/<id>', SkillEditView, name='Skill_Edit_View'),
    path('Skill_add_View', SkilladdView, name='SkilladdView'),
    path('skill_delete/<id>', SkillDeleteView, name='skill_delete'),
    path('locality_Edit_View/<id>', localityEditView, name='locality_Edit_View'),
    path('locality_add_View', localityaddView, name='localityaddView'),
    path('locality_delete/<id>', localityDeleteView, name='locality_delete'),
    path('helper_delete/<id>', HelperDeleteView, name='helper_delete'),
    path('helper_edit/<id>', HelperEditView, name='helper_edit'),
    path('helper_pdf/<id>', HelperPdfView, name='helper_pdf'),
    path('helper__phone_validate_view/<id>',
         HelperPhoneNoValidateDetailsView, name='helper__phone_validate_view'),
    path('helper__phone_validate_accept/<id>',
         HelperPhoneNoValidateAcceptView, name='helper__phone_validate_accept'),
    path('helper__phone_validate_reject/<id>',
         HelperPhoneNoValidateRejectedView, name='helper__phone_validate_reject'),

    path('history', HistoryView, name='history'),
    path('history_view/<id>', HistoryDetailsView, name='history_view'),

    path('lead_list', LeadList, name='lead_list'),
    path('lead_details/<no>', LeadDetailsView, name='lead_details'),
    path('lead_edit/<no>', LeadEditView, name='lead_edit'),
    path('lead_delete/<no>', LeadDeleteView, name='lead_delete'),
    path('lead_add', LeadInsertDataView, name='lead_add'),
    path('lead_status_update/<row>',
         LeadStatusUpdateView, name='lead_status_update'),

    # SuperUser
    path('super/dashboard', SuperUserDashBoard, name='super_user_dashboard'),
    path('super/user_creation', UserCreationView, name='superuser_user_create'),
    path('super/user_list', UserListViews, name='superuser_user_list'),
    path('super/user_update/<id>', userUpdate, name='superuser_user_update'),
    path('super/user_date/<id>', userDelete, name='superuser_user_delete'),

    # employee
    path('employee/dashboard', EmployeeDashboard, name='employee_dashboard')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
