from django.contrib import admin
from .models import Questionnaire, Question, Choice, Patient, Examination, Response

# Register your models here.
admin.site.register(Questionnaire)
admin.site.register(Question)

admin.site.register(Patient)
admin.site.register(Examination)
admin.site.register(Response)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'question', 'sequence', 'text', 'points')
    list_filter = ('question__questionnaire',)


admin.site.register(Choice, ChoiceAdmin)

