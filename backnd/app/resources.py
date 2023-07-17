from import_export import resources
from .models import LeadModel

class LeadModelResources(resources.ModelResource):
    class Meta:
        model = LeadModel