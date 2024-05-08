from import_export import resources
from .models import *

class QuestionLibResource(resources.ModelResource):
    class Meta:
        model = QuestionLibrary
        fields = ('question_name' ,'question_text','question_type' ,'question_category')