from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#-------------Reference Table ---------------------#
class SurveyGoal(models.Model):
    name    = models.CharField(max_length=250, blank=True, null=True)
    description= models.CharField(max_length=250, blank=True, null=True)
    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True,null=True)
    last_update_timestamp=models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True,null=True)

class IndustryType(models.Model):
    name    = models.CharField(max_length=250, blank=True, null=True)
    description= models.CharField(max_length=250, blank=True, null=True)
    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True,null=True)
    last_update_timestamp=models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True,null=True)

class SurveyCategory(models.Model):
    name    = models.CharField(max_length=250, blank=True, null=True)
    description= models.CharField(max_length=250, blank=True, null=True)
    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True,null=True)
    last_update_timestamp=models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True,null=True)

class Element(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

class Option(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    option_type = models.CharField(max_length=100, null=True, blank=True)

#-------------Reference Table ---------------------#

class Survey(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    surveycategory = models.ForeignKey(SurveyCategory,on_delete=models.CASCADE, blank=True, null=True,related_name='surveycategory')
    type_of_responses= models.CharField(max_length=250, blank=True, null=True)
    survey_format= models.CharField(max_length=250, blank=True, null=True)
    number_of_responses= models.CharField(max_length=250, blank=True, null=True)
    estimate_cost= models.CharField(max_length=250, blank=True, null=True)
    estimated_completion_date=models.DateField(max_length=250, blank=True, null=True)
    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True,null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    live_survey_link= models.CharField(max_length=250, blank=True, null=True)
    test_survey_link= models.CharField(max_length=250, blank=True, null=True)
    description= models.CharField(max_length=250, blank=True, null=True)
    tags= models.CharField(max_length=250, blank=True, null=True)
    directory= models.CharField(max_length=250, blank=True, null=True)
    primary_language= models.CharField(max_length=250, blank=True, null=True)
    surveygoal= models.ForeignKey(SurveyCategory,on_delete=models.CASCADE, blank=True, null=True)
    industrytype= models.ForeignKey(IndustryType,on_delete=models.CASCADE, blank=True, null=True)


class Document(models.Model):
    doc_1 = models.CharField(max_length=250, blank=True, null=True)
    doc_2 = models.CharField(max_length=250, blank=True, null=True)
    doc_3 = models.CharField(max_length=250, blank=True, null=True)
    survey= models.ForeignKey(Survey,on_delete=models.CASCADE, blank=True, null=True)

class QuotasSQ(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    survey= models.ForeignKey(Survey,on_delete=models.CASCADE, blank=True, null=True)

class Attributes(models.Model):
    name= models.CharField(max_length=250, blank=True, null=True)
    limit= models.CharField(max_length=250, blank=True, null=True)
    total= models.CharField(max_length=250, blank=True, null=True)
    need= models.CharField(max_length=250, blank=True, null=True)



class ElementOption(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE, null=True, blank=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)

class Questions(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    column = models.CharField(max_length=100, null=True, blank=True)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, null=True, blank=True)
    conditions = models.JSONField(null=True, blank=True)

class QuestionOptions(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True, blank=True)

class SurveyPage(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True, blank=True)

class SurveyPanelQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True, blank=True)
    survey_page = models.ForeignKey(SurveyPage, on_delete=models.CASCADE, null=True, blank=True)

class SurveyQuestionareSurvey(models.Model):
    panelist_id = models.CharField(max_length=100, null=True, blank=True)
    question_id = models.CharField(max_length=100, null=True, blank=True)
    option_id = models.CharField(max_length=100, null=True, blank=True)

