from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# employee user model
class EmployeeModel(models.Model):
    # create and update
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)


# <<-----------------------------------------Helper models ----------------------------------------->>
# state
STATE = (
    ('andhra_pradesh', 'Andhra Pradesh'),
    ('arunachal_pradesh', 'Arunachal Pradesh'),
    ('assam', 'Assam'),
    ('bihar', 'Bihar'),
    ('chhattisgarh', 'Chhattisgarh'),
    ('goa', 'Goa'),
    ('gujarat', 'Gujarat'),
    ('haryana', 'Haryana'),
    ('himachal_pradesh', 'Himachal Pradesh'),
    ('jharkhand', 'Jharkhand'),
    ('karnataka', 'Karnataka'),
    ('kerala', 'Kerala'),
    ('madhya_pradesh', 'Madhya Pradesh'),
    ('maharashtra', 'Maharashtra'),
    ('manipur', 'Manipur'),
    ('meghalaya', 'Meghalaya'),
    ('mizoram', 'Mizoram'),
    ('nagaland', 'Nagaland'),
    ('odisha', 'Odisha'),
    ('punjab', 'Punjab'),
    ('rajasthan', 'Rajasthan'),
    ('sikkim', 'Sikkim'),
    ('tamil_nadu', 'Tamil Nadu'),
    ('telangana', 'Telangana'),
    ('tripura', 'Tripura'),
    ('uttar_pradesh', 'Uttar Pradesh'),
    ('uttarakhand', 'Uttarakhand'),
    ('west_bengal', 'West Bengal'),

)

# country
COUNTRY = (
    ('india', 'INDIA'),
)

# contact status
CONTACT_STATUS = (
    ('placed', 'Placed'),
    ('pending', 'Pending'),
    ('need_to_contact', 'Need to contact'),
)

LOCALITY = (
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd'),

)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

YES_NO = (
    ('N', 'No'),
    ('Y', 'Yes'),
)

EXPERIENCE = (
    ('0-3 month', '0-3 month'),
    ('3-6 month', '3-6 month'),
    ('6-9 month', '6-9 month'),
    ('1 year', '1 year'),
    ('1.5 year', '1.5 year'),
    ('2 year', '2 year'),
    ('2.5 year', '2.5 year'),
    ('3 year', '3 year'),
    ('3.5 year', '3.5 year'),
    ('4 year', '4 year'),
    ('4.5 year', '4.5 year'),
    ('5 year', '5 year'),
    ('5.5 year', '5.5 year'),
    ('6 year', '6 year'),
    ('6.5 year', '6.5 year'),
    ('6 year+', '6 year+'),
)

AVAILABILITY_STATUS = (
    ('live_in', 'Live in'),
    ('on_demand', 'On demand'),
    ('full_time', 'Full time'),
    ('part_time', 'Part time'),
    ('misc', 'Misc'),
)


# pdf allow
def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

def validate_image(value):
    if not value.name.endswith('.jpeg'):
        raise ValidationError('Only JPEG files are allowed.')

ID_TYPE = (
    ('dl', 'DL'),
    ('aadhar', 'AADHAR'),
    ('pan', 'PAN')
)

CALL_STATUS = (
    ('yes', 'Yes'),
    ('no', 'No'),
    ('not called', 'Not called')
)


class HelperModel(models.Model):
    # model id
    helper_id = models.CharField(
        max_length=20, null=True, blank=True, unique=True)
    helper_status = models.CharField(
        max_length=50, choices=CONTACT_STATUS, default='pending')

    # personal details
    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)

    # Contact Number
    primary_phone = models.CharField(
        max_length=100, null=False, blank=False, default='')

    secondary_phone = models.CharField(
        max_length=100, null=True, blank=True, default='')
    email_id = models.CharField(
        max_length=100, null=True, blank=True, default='Name@ezyhelpers.com')
    dob = models.DateField(null=True, blank=True)

    # address
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    state = models.CharField(
        max_length=100, choices=STATE, null=True, blank=True)
    country = models.CharField(
        max_length=100, choices=COUNTRY, null=True, blank=True)

    # Comments
    additional_comment = models.TextField(blank=True, null=True)

    # work
    work_experience = models.CharField(max_length=30, choices=EXPERIENCE)
    availability_status_week = models.CharField(max_length=400)

    # Helper Type
    availability_status = models.CharField(max_length=60, choices=AVAILABILITY_STATUS, null=True, blank=True)

    # locality
    locality = models.CharField(max_length=30, choices=LOCALITY)
    near_by = models.BooleanField(default=False)

    # create and update
    admin_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(null=True, blank=True)

    photo = models.FileField(
        upload_to='images/', validators=[validate_image], null=True, blank=True)

    # ID Proof Copy (Drive Link - Public)
    id_pdf = models.FileField(
        upload_to='pdfs/', validators=[validate_pdf], null=True, blank=True)
    id_type = models.CharField(
        max_length=100, blank=True, null=True, choices=ID_TYPE)

    # call status
    call_status = models.CharField(
        max_length=100, choices=CALL_STATUS, default=None, null=True)

    # if phone exist it convert to True
    phone_valid = models.BooleanField(default=False)

    # Job Role 2
    job_role_2 = models.CharField(max_length=100, null=True, blank=True)

    # Helper Address / Locality
    helper_locality = models.CharField(max_length=60, null=True, blank=True)

    # Currently Working In (Society)
    society = models.CharField(max_length=60, null=True, blank=True)

    # Listed By
    listed_by = models.CharField(max_length=60, null=False, blank=False, default='')

    # Language Known
    language_known = models.CharField(max_length=60, null=True, blank=True)

    # Age
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    # Gender
    gender = models.CharField(max_length=30, choices=GENDER, null=True, blank=True)

    # Do you work on Sundays?
    sunday = models.CharField(max_length=30, choices=YES_NO, null=True, blank=True)

    # Do you have a smartphone?
    smartphone = models.CharField(max_length=30, choices=YES_NO, null=True, blank=True)

    # Do you use WhatsApp
    whatsApp = models.CharField(max_length=30, choices=YES_NO, null=True, blank=True)

    # Available Hours Start Time 1
    start_time_1 = models.TimeField(null=True, blank=True)

    # Available Hours End Time 1
    end_time_1 = models.TimeField(null=True, blank=True)

    # Available Hours Start Time 2
    start_time_2 = models.TimeField(null=True, blank=True)

    # Available Hours End Time 2
    end_time_2 = models.TimeField(null=True, blank=True)

    # Available Hours Start Time 3
    start_time_3 = models.TimeField(null=True, blank=True)

    # Available Hours End Time 3
    end_time_3 = models.TimeField(null=True, blank=True)

    # Available Hours Start Time 4
    start_time_4 = models.TimeField(null=True, blank=True)

    # Available Hours End Time 4
    end_time_4 = models.TimeField(null=True, blank=True)

    # Charges
    charges = models.TextField(null=True, blank=True)

    # Preferences
    preferences = models.CharField(max_length=60, null=True, blank=True)

    # ID Proof Status
    id_proof_status = models.CharField(max_length=100, null=True, blank=True)

    # Aadhar Verification
    aadhar_verification = models.CharField(max_length=100, null=True, blank=True)

    # Other ID proof
    other_id_proof = models.CharField(max_length=100, null=True, blank=True)

    # Police Verification
    police_verification = models.CharField(max_length=100, null=True, blank=True)

    # Date of 1st engagement
    engagement_date = models.DateField(auto_now_add=False, null=True, blank=True)

    # Previous Employer Name
    previous_employer_name = models.CharField(max_length=100, null=True, blank=True)

    # Previous Employer Contact No
    previous_employer_contact = models.CharField(max_length=100, null=True, blank=True)

    # Previous Employer Society
    previous_employer_society = models.CharField(max_length=60, null=True, blank=True)

    # Rating
    rating = models.PositiveSmallIntegerField(null=True, blank=True)

    # Remarks
    remarks = models.TextField(blank=True, null=True)

    # Attempt 2
    attempt_2 = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        serialized = "helper_id:"
        if self.helper_id is None or self.helper_id == '':
            serialized += ""
        else:
            serialized += self.helper_id

        serialized += ",first_name:" + self.first_name
        serialized += ",middle_name:"
        if self.middle_name is None or self.middle_name == '':
            serialized += ""
        else:
            serialized += self.middle_name
        serialized += ",last_name:" + self.last_name

        # Contact Number
        serialized += ",primary_phone:" + str(self.primary_phone)

        # Job Role 2
        serialized += ",job_role_2:" + str(self.job_role_2)

        # Helper Type
        serialized += ",availability_status:" + str(self.availability_status)

        # Helper Address / Locality
        serialized += ",helper_locality:" + str(self.helper_locality)

        # Currently Working In (Society)
        serialized += ",society:" + str(self.society)

        # Listed By
        serialized += ",listed_by:" + str(self.listed_by)

        # Language Known
        serialized += ",language_known:" + str(self.language_known)

        # Age
        serialized += ",age:" + str(self.age)

        # Gender
        serialized += ",gender:" + str(self.gender)

        # Do you work on Sundays?
        serialized += ",sunday:" + str(self.sunday)

        # Do you have a smartphone?
        serialized += ",smartphone:" + str(self.smartphone)

        # Do you use WhatsApp
        serialized += ",whatsApp:" + str(self.whatsApp)

        # Available Hours Start Time 1
        serialized += ",start_time_1:" + str(self.start_time_1)

        # Available Hours End Time 1
        serialized += ",end_time_1:" + str(self.end_time_1)

        # Available Hours Start Time 2
        serialized += ",start_time_2:" + str(self.start_time_2)

        # Available Hours End Time 2
        serialized += ",end_time_2:" + str(self.end_time_2)

        # Available Hours Start Time 3
        serialized += ",start_time_3:" + str(self.start_time_3)

        # Available Hours End Time 3
        serialized += ",end_time_3:" + str(self.end_time_3)

        # Available Hours Start Time 4
        serialized += ",start_time_4:" + str(self.start_time_4)

        # Available Hours End Time 4
        serialized += ",end_time_4:" + str(self.end_time_4)

        # Charges
        serialized += ",charges:" + str(self.charges)

        # Preferences
        serialized += ",preferences:" + str(self.preferences)

        # ID Proof Status
        serialized += ",id_proof_status:" + str(self.id_proof_status)

        # Aadhar Verification
        serialized += ",aadhar_verification:" + str(self.aadhar_verification)

        # ID Proof Copy (Drive Link - Public)
        serialized += ",id_pdf:"
        if self.id_pdf is None or self.id_pdf == '':
            serialized += ""
        else:
            serialized += str(self.id_pdf)

        # Other ID proof
        serialized += ",other_id_proof:" + str(self.other_id_proof)

        # Police Verification
        serialized += ",police_verification:" + str(self.police_verification)

        # Date of 1st engagement
        serialized += ",engagement_date:" + str(self.engagement_date)

        # Previous Employer Name
        serialized += ",previous_employer_name:" + str(self.previous_employer_name)

        # Previous Employer Contact No
        serialized += ",previous_employer_contact:" + str(self.previous_employer_contact)

        # Previous Employer Society
        serialized += ",previous_employer_society:" + str(self.previous_employer_society)

        # Rating
        serialized += ",rating:" + str(self.rating)

        # Remarks
        serialized += ",remarks:" + str(self.remarks)

        # Comments
        serialized += ",additional_comment:"
        if self.additional_comment is None or self.additional_comment == '':
            serialized += ""
        else:
            serialized += self.additional_comment

        # Attempt 2
        serialized += ",attempt_2:" + str(self.attempt_2)

        return serialized


# skill set
class HelperSkillSetModel(models.Model):
    helper = models.ForeignKey(HelperModel, on_delete=models.CASCADE)
    skill = models.CharField(max_length=200)


# Helper languages
class HelperPreferredLanguageModel(models.Model):
    helper = models.ForeignKey(HelperModel, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


# Helper additional details
class HelperAdditionalSkillSetModel(models.Model):
    helper = models.ForeignKey(HelperModel, on_delete=models.CASCADE)
    additional_skill = models.CharField(max_length=100)

    def __str__(self):
        return self.additional_skill


# Helper job role


class HelperJobRoleModel(models.Model):
    helper = models.ForeignKey(HelperModel, on_delete=models.CASCADE)
    job = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.helper} __ {self.job}"


LEAD_CONTACT_STATUS = (
    ('pending', 'Pending'),
    ('first contact', 'First contact'),
    ('follow up', 'Follow up'),
    ('failed', 'Failed'),
    ('confirmed', 'Confirmed'),
)


# lead notification


class LeadStatusNotificationModel(models.Model):
    lead = models.CharField(max_length=100)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=50, choices=LEAD_CONTACT_STATUS, default='pending')
    msg = models.CharField(max_length=400)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)


# helper History Model
HISTORY_STATUS = (
    ('create', 'create'),
    ('delete', 'delete'),
    ('update', 'update')
)


class HelperHistoryModel(models.Model):
    # model id
    helper_id = models.CharField(max_length=20, null=True, blank=True)

    # personal details
    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    primary_phone = models.CharField(max_length=100, null=False, blank=False)
    email_id = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField()

    # create and update and remove status
    admin_user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)
    history_status = models.CharField(
        max_length=100, choices=HISTORY_STATUS, default='create')

    # History status
    def __str__(self) -> str:
        return f'{self.first_name} __ {self.history_status}'


class leadHistoryModel(models.Model):
    # personal details
    lead_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=True, blank=True)

    # create and update and remove status
    admin_user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)
    history_status = models.CharField(
        max_length=100, choices=HISTORY_STATUS, default='create')

    def __str__(self) -> str:
        return f'{self.name}'


class HistoryModel(models.Model):
    lead = models.ForeignKey(
        leadHistoryModel, on_delete=models.CASCADE, null=True, blank=True)
    helper = models.ForeignKey(
        HelperHistoryModel, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.helper} {self.lead}'


class LeadModel(models.Model):
    # Owner Name
    name = models.CharField(max_length=100, null=False, blank=False)

    # Contact No
    phone = models.CharField(max_length=100, null=False, blank=False, default='')

    # Email ID
    email_id = models.CharField(
        max_length=100, null=True, blank=True, default='Name@ezyhelpers.com')

    # Job Role
    availability_status = models.CharField(max_length=60, choices=AVAILABILITY_STATUS)

    # Type
    job_category = models.CharField(max_length=200, null=True, blank=True)

    # Lead-in Date
    lead_in_date = models.DateTimeField(blank=True, null=True)

    # Requirement Start Time
    requirement_start_time = models.TimeField(blank=True, null=True)

    # Requirement End Time
    requirement_end_time = models.TimeField(blank=True, null=True)

    # Society
    society = models.CharField(max_length=200, null=True, blank=True)

    # Flat No
    flat_number = models.CharField(max_length=200, null=True, blank=True)

    # helper Requirement Form Fill Status
    form_fill_status = models.CharField(max_length=60, null=True, blank=True)

    # Lead Status
    lead_status = models.CharField(max_length=100, null=True, blank=True, default='')

    # Helper Name
    helper_name = models.CharField(max_length=100, null=True, blank=True)

    # Helper Number
    helper_no = models.CharField(max_length=100, null=True, blank=True)

    # Actual Status
    actual_status = models.CharField(max_length=100, null=True, blank=True)

    # Lead Lost Reason
    lead_lost_reason = models.CharField(max_length=100, null=True, blank=True)

    # Date of Placement
    lead_placement_date = models.DateField(blank=True, null=True)

    # Date of Exit
    exit_date = models.DateField(blank=True, null=True)

    # ID Proof Type
    identity_type = models.TextField(blank=True, null=True)

    # ID Proof Status
    identity_status = models.TextField(blank=True, null=True)

    # ID proof shared with the customer
    identity_shared = models.CharField(max_length=60, blank=True, null=True)

    # Employer Application Form
    application_form = models.TextField(blank=True, null=True)

    # Total Duration
    duration = models.TextField(blank=True, null=True)

    # Payment Date
    payment_date = models.DateField(blank=True, null=True)

    # Payment Status
    payment_status = models.CharField(max_length=60, blank=True, null=True)

    # Payment Mode
    payment_mode = models.CharField(max_length=60, blank=True, null=True)

    # Receivables / Salary
    salary = models.PositiveIntegerField(blank=True, null=True)

    # Paid - 3rd Party
    third_party = models.TextField(blank=True, null=True)

    # Ezy Commission
    commission = models.TextField(blank=True, null=True)

    # Lead Source
    lead_source = models.CharField(max_length=200, blank=True, null=True)

    # Sales Person
    sales_person = models.CharField(max_length=100, blank=True, null=True)

    # Comments
    additional_comment = models.TextField(blank=True, null=True)

    # Remarks
    remarks = models.TextField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    # locality
    locality = models.CharField(max_length=30, choices=LOCALITY)

    near_by = models.BooleanField(default=False)

    # create and update
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    update_date = models.DateTimeField(blank=True, null=True)
    agent = models.TextField(blank=True, null=True)
    phone_valid_status = models.CharField(max_length=100, blank=True, null=True)
    lead_id = models.CharField(
        max_length=20, null=True, blank=True, unique=True)
    lead_req_date = models.DateField(blank=True, null=True)
    lead_status2 = models.CharField(max_length=200, blank=True, null=True)
    role_on_demand_start_date = models.DateField(blank=True, null=True)
    role_on_demand_start_from_time = models.TimeField(blank=True, null=True)
    role_on_demand_start_to_time = models.TimeField(blank=True, null=True)
    role_on_demand_end_date = models.DateField(blank=True, null=True)
    role_on_demand_end_from_time = models.TimeField(blank=True, null=True)
    role_on_demand_end_to_time = models.TimeField(blank=True, null=True)

    def __str__(self) -> str:
        serialized = "lead_id:" + self.lead_id + ",name:" + self.name + ",phone:" + str(self.phone)

        # Email ID
        if self.email_id is not None:
            serialized += ',email_id:' + str(self.email_id)
        else:
            serialized += ',email_id:'

        # Job Role
        serialized += ',availability_status:' + str(self.availability_status)

        # Type
        serialized += ',job_category:' + str(self.job_category)

        # Lead-in Date
        serialized += ',lead_in_date:' + str(self.lead_in_date)

        # Requirement Start Time
        serialized += ',requirement_start_time:' + str(self.requirement_start_time)

        # Requirement End Time
        serialized += ',requirement_end_time:' + str(self.requirement_end_time)

        # Society
        if self.society is not None:
            serialized += ',society:' + str(self.society)
        else:
            serialized += ',society:'

        # Flat No
        if self.flat_number is not None:
            serialized += ',flat_number:' + str(self.flat_number)
        else:
            serialized += ',flat_number:'

        # helper Requirement Form Fill Status
        if self.form_fill_status is not None:
            serialized += ',form_fill_status:' + str(self.form_fill_status)
        else:
            serialized += ',form_fill_status:'

        # Lead Status
        if self.lead_status is not None:
            serialized += ',lead_status:' + str(self.lead_status)
        else:
            serialized += ',lead_status:'

        # Helper Name
        if self.helper_name is not None:
            serialized += ',helper_name:' + str(self.helper_name)
        else:
            serialized += ',helper_name:'

        # Helper Number
        if self.helper_no is not None:
            serialized += ',helper_no:' + str(self.helper_no)
        else:
            serialized += ',helper_no:'

        # Actual Status
        if self.actual_status is not None:
            serialized += ',actual_status:' + str(self.actual_status)
        else:
            serialized += ',actual_status:'

        # Lead Lost Reason
        if self.lead_lost_reason is not None:
            serialized += ',lead_lost_reason:' + str(self.lead_lost_reason)
        else:
            serialized += ',lead_lost_reason:'

        # Date of Placement
        if self.lead_placement_date is not None:
            serialized += ',lead_placement_date:' + str(self.lead_placement_date)
        else:
            serialized += ',lead_placement_date:'

        # Date of Exit
        if self.exit_date is not None:
            serialized += ',exit_date:' + str(self.exit_date)
        else:
            serialized += ',exit_date:'

        # ID Proof Type
        if self.identity_type is not None:
            serialized += ',identity_type:' + str(self.identity_type)
        else:
            serialized += ',identity_type:'

        # ID Proof Status
        if self.identity_status is not None:
            serialized += ',identity_status:' + str(self.identity_status)
        else:
            serialized += ',identity_status:'

        # ID proof shared with the customer
        if self.identity_shared is not None:
            serialized += ',identity_shared:' + str(self.identity_shared)
        else:
            serialized += ',identity_shared:'

        # Employer Application Form
        if self.application_form is not None:
            serialized += ',application_form:' + str(self.application_form)
        else:
            serialized += ',application_form:'

        # Total Duration
        if self.duration is not None:
            serialized += ',duration:' + str(self.duration)
        else:
            serialized += ',duration:'

        # Payment Date
        if self.payment_date is not None:
            serialized += ',payment_date:' + str(self.payment_date)
        else:
            serialized += ',payment_date:'

        # Payment Status
        if self.payment_status is not None:
            serialized += ',payment_status:' + str(self.payment_status)
        else:
            serialized += ',payment_status:'

        # Payment Mode
        if self.payment_mode is not None:
            serialized += ',payment_mode:' + str(self.payment_mode)
        else:
            serialized += ',payment_mode:'

        # Receivables / Salary
        if self.salary is not None:
            serialized += ',salary:' + str(self.salary)
        else:
            serialized += ',salary:'

        # Paid - 3rd Party
        if self.third_party is not None:
            serialized += ',third_party:' + str(self.third_party)
        else:
            serialized += ',third_party:'

        # Ezy Commission
        if self.commission is not None:
            serialized += ',commission:' + str(self.commission)
        else:
            serialized += ',commission:'

        # Lead Source
        if self.lead_source is not None:
            serialized += ',lead_source:' + str(self.lead_source)
        else:
            serialized += ',lead_source:'

        # Sales Person
        if self.sales_person is not None:
            serialized += ',sales_person:' + str(self.sales_person)
        else:
            serialized += ',sales_person:'

        # Comments
        if self.additional_comment is not None:
            serialized += ',additional_comment:' + str(self.additional_comment)
        else:
            serialized += ',additional_comment:'

        # Remarks
        if self.remarks is not None:
            serialized += ',remarks:' + str(self.remarks)
        else:
            serialized += ',remarks:'

        return serialized


class Localities(models.Model):
    name = models.CharField(max_length=100, null=False,
                            blank=False, unique=True)


class Skills(models.Model):
    name = models.CharField(max_length=100, null=False,
                            blank=False, unique=True)


class JobCat(models.Model):
    name = models.CharField(max_length=100, null=False,
                            blank=False, unique=True)
