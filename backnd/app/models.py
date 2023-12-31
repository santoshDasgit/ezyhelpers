from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


# employee user model
class EmployeeModel(models.Model):
    # create and update 
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(null=True,blank=True)
    employee = models.ForeignKey(User,on_delete=models.CASCADE)



# <<-----------------------------------------Helper models ----------------------------------------->>

# state 
STATE = (
('andhra_pradesh','Andhra Pradesh'),
('arunachal_pradesh','Arunachal Pradesh'),
('assam','Assam'),
('bihar','Bihar'),
('chhattisgarh','Chhattisgarh'),
('goa','Goa'),
('gujarat','Gujarat'),
('haryana','Haryana'),
('himachal_pradesh','Himachal Pradesh'),
('jharkhand','Jharkhand'),
('karnataka','Karnataka'),
('kerala','Kerala'),
('madhya_pradesh','Madhya Pradesh'),
('maharashtra','Maharashtra'),
('manipur','Manipur'),
('meghalaya','Meghalaya'),
('mizoram','Mizoram'),
('nagaland','Nagaland'),
('odisha','Odisha'),
('punjab','Punjab'),
('rajasthan','Rajasthan'),
('sikkim','Sikkim'),
('tamil_nadu','Tamil Nadu'),
('telangana','Telangana'),
('tripura','Tripura'),
('uttar_pradesh','Uttar Pradesh'),
('uttarakhand','Uttarakhand'),
('west_bengal','West Bengal'),

)

# country 
COUNTRY = (
    ('india','INDIA'),
)

# contact status 
CONTACT_STATUS = (
    ('placed','Placed'),
    ('pending','Pending'),
    ('need_to_contact','Need to contact'),
)

LOCALITY = (
    ('a','a'),
    ('b','b'),
    ('c','c'),
    ('d','d'),
    
)

EXPERIENCE = (
    ('0-3 month','0-3 month'),
    ('3-6 month','3-6 month'),
    ('6-9 month','6-9 month'),
    ('1 year','1 year'),
    ('1.5 year','1.5 year'),
    ('2 year','2 year'),
    ('2.5 year','2.5 year'),
    ('3 year','3 year'),
    ('3.5 year','3.5 year'),
    ('4 year','4 year'),
    ('4.5 year','4.5 year'),
    ('5 year','5 year'),
    ('5.5 year','5.5 year'),
    ('6 year','6 year'),
    ('6.5 year','6.5 year'),
    ('6 year+','6 year+'),
)

AVAILABILITY_STATUS = (
    ('live_in','Live in'),
     ('on_demand','On demand'),
     ('full_time','Full time'),
     ('part_time','Part time'),
     ('misc','Misc'),
) 



# pdf allow 
def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

ID_TYPE = (
    ('dl','DL'),
    ('aadhar','AADHAR'),
    ('pan','PAN')
)
    
CALL_STATUS = (
    ('yes','Yes'),
    ('no','No'),
    ('not called','Not called')
)
class HelperModel(models.Model):
    # model id 
    helper_id = models.CharField(max_length=20,null=True,blank=True,unique=True)
    helper_status = models.CharField(max_length=50,choices=CONTACT_STATUS,default='pending')


    # personal details
    first_name = models.CharField(max_length=100,null=False,blank=False)
    middle_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    primary_phone = models.CharField(max_length=100,null=False,blank=False,default='')
    secondary_phone = models.CharField(max_length=100,null=True,blank=True,default='')
    email_id = models.CharField(max_length=100,null=True,blank=True,default='Name@ezyhelpers.com')
    dob = models.DateField()

    # address
    street = models.CharField(max_length=100,null=False,blank=False)
    city = models.CharField(max_length=100,null=False,blank=False)
    zipcode = models.IntegerField(null=False,blank=False)
    state = models.CharField(max_length=100,choices=STATE,null=False,blank=False)
    country = models.CharField(max_length=100,choices=COUNTRY,null=False,blank=False)
    additional_comment = models.TextField(blank=True,null=True)

    # work
    work_experience = models.CharField(max_length=30,choices=EXPERIENCE)
    availability_status_week = models.CharField(max_length=400)
    availability_status = models.CharField(max_length=60,choices=AVAILABILITY_STATUS)

    # locality 
    locality = models.CharField(max_length=30,choices=LOCALITY)
    near_by = models.BooleanField(default=False)

    # create and update 
    admin_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(null=True,blank=True)

    # id proved
    id_pdf = models.FileField(upload_to='pdfs/', validators=[validate_pdf],null=True,blank=True)
    id_type = models.CharField(max_length=100,blank=True,null=True,choices=ID_TYPE)

    # call status 
    call_status = models.CharField(max_length=100,choices=CALL_STATUS,default=None,null=True)

    # if phone exist it convert to True
    phone_valid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.first_name
     

# skill set 
class HelperSkillSetModel(models.Model):
    helper = models.ForeignKey(HelperModel,on_delete=models.CASCADE)
    skill = models.CharField(max_length=200)
    

# Helper languages
class HelperPreferredLanguageModel(models.Model):
    helper = models.ForeignKey(HelperModel,on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    def __str__(self):
        return self.language


# Helper additional details 
class HelperAdditionalSkillSetModel(models.Model):
    helper = models.ForeignKey(HelperModel,on_delete=models.CASCADE)
    additional_skill = models.CharField(max_length=100)

    def __str__(self):
        return self.additional_skill

# Helper job role   
class HelperJobRoleModel(models.Model):
    helper = models.ForeignKey(HelperModel,on_delete=models.CASCADE)
    job = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f"{self.helper} __ {self.job}"


LEAD_CONTACT_STATUS = (
    ('pending','Pending'),
    ('first contact','First contact'),
    ('follow up','Follow up'),
    ('failed','Failed'),
    ('confirmed','Confirmed'),
)

# lead notification 
class LeadStatusNotificationModel(models.Model):
    lead = models.CharField(max_length=100)
    employee = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=50,choices=LEAD_CONTACT_STATUS,default='pending')
    msg = models.CharField(max_length=400)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True,blank=True)




# helper History Model 

HISTORY_STATUS = (
    ('create','create'),
    ('delete','delete'),
    ('update','update')
)
   

class HelperHistoryModel(models.Model):
    # model id 
    helper_id = models.CharField(max_length=20,null=True,blank=True)
    
    # personal details
    first_name = models.CharField(max_length=100,null=False,blank=False)
    middle_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    primary_phone = models.CharField(max_length=100,null=False,blank=False)
    email_id = models.CharField(max_length=100,null=True,blank=True)
    dob = models.DateField()

    # create and update and remove status
    admin_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True,blank=True)
    history_status = models.CharField(max_length=100,choices=HISTORY_STATUS,default='create')

    # History status
    def __str__(self) -> str:
        return f'{self.first_name} __ {self.history_status}'

class leadHistoryModel(models.Model):
    # personal details
    lead_id = models.CharField(max_length=20,null=True,blank=True)
    name = models.CharField(max_length=100,null=False,blank=False)
    phone = models.CharField(max_length=100,null=False,blank=False)
    email = models.CharField(max_length=100,null=True,blank=True)

    # create and update and remove status
    admin_user = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True,blank=True)
    history_status = models.CharField(max_length=100,choices=HISTORY_STATUS,default='create')
    def __str__(self) -> str:
        return f'{self.name}'


class HistoryModel(models.Model):
    lead = models.ForeignKey(leadHistoryModel,on_delete=models.CASCADE,null=True,blank=True)
    helper = models.ForeignKey(HelperHistoryModel,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.helper} {self.lead}'
    
class LeadModel(models.Model): 

    # personal details
    name = models.CharField(max_length=100,null=False,blank=False)
    phone = models.CharField(max_length=100,null=False,blank=False,default='')
    email_id = models.CharField(max_length=100,null=True,blank=True,default='Name@ezyhelpers.com')
    address = models.TextField(blank=True,null=True)
    availability_status = models.CharField(max_length=60,choices=AVAILABILITY_STATUS)
    # locality 
    locality = models.CharField(max_length=30,choices=LOCALITY)
    near_by = models.BooleanField(default=False)

    # create and update 
    admin_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    update_date = models.DateTimeField(blank=True,null=True)
    lead_status = models.CharField(max_length=100,default="")
    additional_comment = models.TextField(blank=True,null=True)
    agent = models.TextField(blank=True,null=True)
    phone_valid_status=models.CharField(max_length=100,blank=True,null=True)
    lead_id=models.CharField(max_length=20,null=True,blank=True,unique=True)
    flat_number = models.CharField(max_length=200,null=True,blank=True)
    lead_req_date = models.DateField(blank=True,null=True)
    lead_placement_date = models.DateField(blank=True,null=True)
    lead_status2 = models.CharField(max_length=200,blank=True,null=True)
    role_on_demand_start_date = models.DateField(blank=True,null=True)
    role_on_demand_start_from_time = models.TimeField(blank=True,null=True)
    role_on_demand_start_to_time = models.TimeField(blank=True,null=True)
    role_on_demand_end_date = models.DateField(blank=True,null=True)
    role_on_demand_end_from_time = models.TimeField(blank=True,null=True)
    role_on_demand_end_to_time = models.TimeField(blank=True,null=True)
    lead_source = models.CharField(max_length=200,blank=True,null=True)
    job_category= models.CharField(max_length=200,null=True,blank=True)

    def __str__(self) -> str:
        return self.name
 
class Localities(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,unique=True)

class Skills(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,unique=True)
