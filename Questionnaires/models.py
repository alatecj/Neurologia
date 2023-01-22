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
    # eval_sequence sluzi na odkazovanie sa na otazky v pripadoch, ak su vyhodnocovane v inom poradi, ako zobrazovane
    # napr. pri liveerpool seizure scale - kde otazky zobrazujeme v poradi 1,2,3,4,6,7,13,14..., ale vyhodnocujeme v
    # poradi 1-9, 10-20
    eval_sequence = models.PositiveSmallIntegerField(null=True, blank=True)
    text = models.CharField(max_length=200)
    # section_text sluzi na pridanie textu pred niektorou z otazok - napriklad nejaky text vysvetlujuci co bude v dalsej
    # sekcii
    section_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Choice(models.Model):
    class Meta:
        ordering = ('question', 'id')

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
    comment_before = models.CharField(max_length=200, blank=True)
    comment_after = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vyšetrenie {self.id}"


class Response(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="qre_responses")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="patient_responses")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="choice_responses")
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name="exam_responses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice.text
