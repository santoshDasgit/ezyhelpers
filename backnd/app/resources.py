from import_export import resources
from .models import HelperModel

class HelperModelResources(resources.ModelResource):
    class Meta:
        model = HelperModel