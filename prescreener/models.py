from django.db import models
import datetime

##################### Reference Table ##############################

class QuestionType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class QuestionCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    survey_category_image = models.FileField(null=True, blank=True, upload_to='surveycategory/')

class QuestionOperator(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)

class QuestionTypeOperator(models.Model):
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, null=True, blank=True)
    question_operator = models.ForeignKey(QuestionOperator, on_delete=models.CASCADE, null=True, blank=True)

#####################################################################

class QuestionLibrary(models.Model):
    language = models.CharField(max_length=100, null=True, blank=True)
    position_value = models.CharField(max_length=100, null=True, blank=True)
    question_id = models.CharField(max_length=100, null=True, blank=True)
    question_name = models.TextField(null=True, blank=True)
    question_text = models.CharField(max_length=100, blank=True, null=True)
    instruction = models.CharField(max_length=100, null=True, blank=True)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name="question_type", null=True, blank=True)
    question_category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name="question_category", null=True, blank=True)
    is_base_question = models.BooleanField(default=True)


class QuestionLibraryWithLanguages(models.Model):
    base_queestion = models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE ,max_length=100, null=True, blank=True, related_name='base_queestion')
    created_question_language = models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE ,max_length=100, null=True, blank=True,related_name='created_question_language')
    
class Prescreener(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    generated_link = models.URLField(null=True, blank=True)
    enable_otp_verification = models.BooleanField(blank=True)
    project = models.CharField(max_length=100, null=True, blank=True)

class QuestionChoice(models.Model):
    option_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    text = models.CharField(max_length=100, null=True, blank=True)
    question_library = models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE, related_name="question_choice", null=True, blank=True)
    # question_choice = models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE, related_name="question_choices", null=True, blank=True)

class PrescreenerQuestionLibrary(models.Model):
    prescreener = models.ForeignKey(Prescreener, on_delete=models.CASCADE, related_name="prescreener", null=True, blank=True)
    question_library = models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE, related_name="question_library", null=True, blank=True)
    

class UserSurvey(models.Model):
    panelist_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, blank=True)
    dob = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    tid = models.TextField(null=True, blank=True)
    campaign_id = models.IntegerField(null=True, blank=True)
    supplier_id = models.IntegerField(null=True, blank=True)
    date_of_joining = models.DateField(default=datetime.date.today, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    profile_image = models.FileField(null=True, blank=True, upload_to='profileImage/')

class Answer(models.Model):
    user_survey=models.ForeignKey(UserSurvey, on_delete=models.CASCADE, null=True, blank=True)
    answers = models.TextField(null=True, blank=True)
    question_library=models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE, null=True, blank=True, related_name='questions_library')

    prescreener_id = models.IntegerField(null=True, blank=True)
    campaign_id = models.IntegerField(null=True, blank=True)
    pe_campaign_id = models.IntegerField(null=True, blank=True)


class ExternalSamplePanelistAnswer(models.Model):
    panelist_id = models.CharField(max_length=200, null=True,blank=True)
    answers = models.TextField(null=True, blank=True)
    question_library=models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE, null=True, blank=True)

    prescreener_id = models.IntegerField(null=True, blank=True)
    campaign_id = models.IntegerField(null=True, blank=True)
    pe_campaign_id = models.IntegerField(null=True, blank=True)

class DuplicateorFraudPanelistID(models.Model):
    panelist_id = models.CharField(max_length=200, null=True,blank=True)
    project_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    IE = models.CharField(max_length=100, null=True, blank=True)
    campaign_id = models.IntegerField(null=True, blank=True)
    survey_start_time = models.TextField(null=True, blank=True)
    survey_end_time = models.TextField(null=True, blank=True)
    browser = models.TextField(null=True, blank=True)
    os = models.TextField(null=True, blank=True)
    ip_adress = models.TextField(null=True, blank=True)
    user_country = models.TextField(null=True, blank=True)
    client_id = models.TextField(null=True, blank=True)

    supplier_id = models.CharField(max_length=100, null=True, blank=True)
    supplier_name = models.CharField(max_length=100, null=True, blank=True)
    threat_potential = models.CharField(max_length=100, null=True, blank=True)
    threat_potential_score = models.CharField(max_length=100, null=True, blank=True)
    duplicate_score = models.CharField(max_length=100, null=True, blank=True)
    
    # new field added
    county_mismath = models.CharField(max_length=100, null=True, blank=True)

class BuildQueryOpearator(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

