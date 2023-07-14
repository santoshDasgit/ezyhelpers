from django.db import models



# <<-----------------------------------------Lead models ----------------------------------------->>

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
    ('pending','Pending'),
    ('first_contact','First Contact'),
    ('follow_up','Follow Up'),
    ('failed','Field'),
    ('conformed','Conformed'),
)

class LeadModel(models.Model):
    # model id 
    lead_id = models.CharField(max_length=20,null=True,blank=True,unique=True)
    lead_status = models.CharField(max_length=20,choices=CONTACT_STATUS,default='pending')

    # personal details
    first_name = models.CharField(max_length=100,null=False,blank=False)
    middle_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    primary_phone = models.IntegerField(null=False,blank=False)
    secondary_phone = models.IntegerField(null=True,blank=True)
    email_id = models.CharField(max_length=100,null=False,blank=False)

    # address
    street = models.CharField(max_length=100,null=False,blank=False)
    city = models.CharField(max_length=100,null=False,blank=False)
    zipcode = models.IntegerField(null=False,blank=False)
    state = models.CharField(max_length=100,choices=STATE,null=False,blank=False)
    country = models.CharField(max_length=100,choices=COUNTRY,null=False,blank=False)
    additional_comment = models.TextField(blank=True,null=True)

# Lead languages
class LeadPreferredLanguageModel(models.Model):
    lead = models.ForeignKey(LeadModel,on_delete=models.CASCADE)
    language = models.CharField(max_length=100)

class LeadAdditionalDetailsModel(models.Model):
    lead = models.ForeignKey(LeadModel,on_delete=models.CASCADE)
    additional_details = models.CharField(max_length=100)

