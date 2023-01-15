from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from .models import Question, Questionnaire, Response, Patient, Examination
from django.forms import formset_factory
from .forms import ChoiceForm, BaseChoiceFormSet, PatientForm, ChoiceFormSetHelper, ReportForm
from django.urls import reverse
from django.contrib import messages


# Create your views here.


def display_questionnaire(request, questionnaire_id):
    patientform = PatientForm()
    qre_id = Questionnaire.objects.get(pk=questionnaire_id)
    qs = Question.objects.filter(questionnaire=qre_id).values_list('id', flat=True)
    qaformset = formset_factory(ChoiceForm, formset=BaseChoiceFormSet, extra=len(qs))
    formset = qaformset(form_kwargs={'questions': qs})
    helper = ChoiceFormSetHelper()
    return render(request, 'Questionnaires/display_qre.html',
                  {'formset': formset, 'helper': helper, 'qre': qre_id, 'patientform': patientform})


def process(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient_id = form.cleaned_data['id']
            if not Patient.objects.filter(id=patient_id):
                # vytvor django message, ze cislo pacienta je zle!
                messages.add_message(request, messages.ERROR, "Zlé číslo pacienta!")
                # vratime sa na predchadzajucu stranku
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            print(form.errors)
            return HttpResponseRedirect(reverse("index"))
        qre_id = request.POST['qre_id']
        qs = Question.objects.filter(questionnaire=qre_id).values_list('id', flat=True)
        qaformset = formset_factory(ChoiceForm, formset=BaseChoiceFormSet, extra=len(qs))
        formset = qaformset(request.POST, form_kwargs={'questions': qs})

        if formset.is_valid():
            exam = Examination(patient_id=patient_id)
            exam.save()

            for form in formset:
                cleanform = form.cleaned_data['answer']
                # FIXME funkcionalitu s examinations este treba dorobit a domysliet.
                bup = Response(questionnaire_id=cleanform.question.questionnaire_id,
                               patient_id=patient_id,
                               question_id=cleanform.question.id,
                               choice_id=cleanform.id,
                               examination=exam,
                               )
                # print(bup)
                bup.save()

            return HttpResponse("Great!")

        else:
            print(formset.errors)

    else:
        return HttpResponse("POOP")


def get_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            exam = Examination.objects.filter(patient=form.cleaned_data['patient_id'])

            return render(request, 'Questionnaires/show_report.html', {'exam': exam})
    else:
        form = ReportForm()
    return render(request, 'Questionnaires/get_report.html', {
        'form': form
    })


def index(request):
    return render(request, 'Questionnaires/index.html', {})
