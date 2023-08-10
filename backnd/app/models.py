from django.db import models
from django.contrib.auth.models import User


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
WEEK=(
        (1,1),
         (2,2),
          (3,3),
           (4,4),
            (5,5),
             (6,6),
              (7,7),
)
class HelperModel(models.Model):
    # model id 
    helper_id = models.CharField(max_length=20,null=True,blank=True,unique=True)
    helper_status = models.CharField(max_length=50,choices=CONTACT_STATUS,default='pending')


    # personal details
    first_name = models.CharField(max_length=100,null=False,blank=False)
    middle_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    primary_phone = models.IntegerField(null=False,blank=False)
    secondary_phone = models.IntegerField(null=True,blank=True)
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
    availability_status_week = models.IntegerField(default=1,choices=WEEK)
    availability_status = models.CharField(max_length=60,choices=AVAILABILITY_STATUS)

    # locality 
    locality = models.CharField(max_length=30,choices=LOCALITY)
    near_by = models.BooleanField(default=False)

    # create and update 
    admin_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(null=True,blank=True)

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
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(null=True,blank=True)




HISTORY_STATUS = (
    ('create','create'),
    ('delate','delete'),
    ('update','update')
)
# helper History Model 
class HelperHistoryModel(models.Model):
    # model id 
    helper_id = models.CharField(max_length=20,null=True,blank=True,unique=True)
    helper_status = models.CharField(max_length=50,choices=CONTACT_STATUS,default='pending')



    # personal details
    first_name = models.CharField(max_length=100,null=False,blank=False)
    middle_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    primary_phone = models.IntegerField(null=False,blank=False)
    secondary_phone = models.IntegerField(null=True,blank=True)
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
    availability_status_week = models.IntegerField(default=1,choices=WEEK)
    availability_status = models.CharField(max_length=60,choices=AVAILABILITY_STATUS)

    # locality 
    locality = models.CharField(max_length=30,choices=LOCALITY)
    near_by = models.BooleanField(default=False)

    # create and update and remove status
    admin_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(null=True,blank=True)
    history_status = models.CharField(max_length=100,choices=HISTORY_STATUS,default='create')

    # History status

    def __str__(self) -> str:
        return self.first_name
   