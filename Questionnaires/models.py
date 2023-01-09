from django.db import models

# Create your models here.


class Questionnaire(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="questions")
    sequence = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    sequence = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=200)
    points = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Patient(models.Model):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Examination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="examinations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Response(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="qre_responses")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="patient_responses")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="choice_responses")
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name="exam_responses")
    # set nam identifikuje vsetky response objekty vytvorene z jedneho formsetu
    set = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

