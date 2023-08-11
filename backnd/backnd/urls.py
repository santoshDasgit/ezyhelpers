"""
URL configuration for backnd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from .views_super import *
from .views_emp import *
urlpatterns = [

    # common for all
    path('admin/', admin.site.urls),
    path('',HomeView,name='home'),
    path('login/',LoginView,name="login"),
    path('logout/',LogoutView,name='logout'),
    path('profile/<id>',ProfileView,name='profile'),
    path('profile_update/<id>/<email>',ProfileUpdateView,name='profile_update'),
    path('email_validate_profile/<id>/<url>',EmailVerifyProfileView,name='email_validate_profile'),
    path('password_change/',PasswordChangedView,name='password_change'),

    path('helper_list',HelperListViews,name='helper_list'),
    path('helper_add/',HelperAddView,name='helper_add'),
    path('helper_view/<id>',HelperDetailsView,name='helper_view'),
    path('helper_status_update/<id>',HelperStatusUpdateView,name='helper_status_update'),
    path('excel_file_helper_upload',ExcelFileHelperFileView,name='excel_file_helper_upload'),
    path('helper_delete/<id>',HelperDeleteView,name='helper_delete'),
    path('helper_edit/<id>',HelperEditView,name='helper_edit'),
    path('helper_pdf/<id>',HelperPdfView,name='helper_pdf'),



    path('lead_list',LeadList,name='lead_list'),
    path('lead_details/<no>',LeadDetailsView,name='lead_details'),
    path('lead_edit/<no>',LeadEditView,name='lead_edit'),
    path('lead_delete/<no>',LeadDeleteView,name='lead_delete'),
    path('lead_add',LeadInsertDataView,name='lead_add'),
    path('lead_status_update/<row>',LeadStatusUpdateView,name='lead_status_update'),


  




    # SuperUser 
    path('super/dashboard',SuperUserDashBoard,name='super_user_dashboard'),
    path('super/user_creation',UserCreationView,name='superuser_user_create'),
    path('super/user_list',UserListViews,name='superuser_user_list'),
    path('super/user_update/<id>',userUpdate,name='superuser_user_update'),
    path('super/user_date/<id>',userDelete,name='superuser_user_delete'),

    # employee
    path('employee/dashboard',EmployeeDashboard,name='employee_dashboard')
    
]
