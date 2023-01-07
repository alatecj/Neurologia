from django.contrib import admin
from .models import Questionnaire, Question, Choice, Patient, Examination, Response

# Register your models here.
admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Patient)
admin.site.register(Examination)
admin.site.register(Response)
