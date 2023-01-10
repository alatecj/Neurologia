from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from .models import Question, Questionnaire, Response
from django.forms import formset_factory
from .forms import ChoiceForm, BaseChoiceFormSet, PatientForm, ChoiceFormSetHelper
from django.urls import reverse


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
        else:
            print(form.errors)
            return HttpResponseRedirect(reverse("index"))
        qre_id = request.POST['qre_id']
        qs = Question.objects.filter(questionnaire=qre_id).values_list('id', flat=True)
        qaformset = formset_factory(ChoiceForm, formset=BaseChoiceFormSet, extra=len(qs))
        formset = qaformset(request.POST, form_kwargs={'questions': qs})

        if formset.is_valid():
            if form.is_valid():
                pass
            else:
                print(form.errors)

            for form in formset:
                cleanform = form.cleaned_data['answer']
                # FIXME funkcionalitu s examinations este treba dorobit a domysliet.
                print(patient_id)
                # TODO ak nam uzivatel zada zle cislo pacienta, tak nam save zhavaruje - ako tomu predist?
                # mozno https://docs.djangoproject.com/en/4.1/ref/forms/validation/
                bup = Response(questionnaire_id=cleanform.question.questionnaire_id,
                               # FIXME patient_id nesmie byt natvrdo!
                               patient_id=patient_id,
                               question_id=cleanform.question.id,
                               choice_id=cleanform.id,
                               examination_id=1,
                               )
                #print(bup)
                bup.save()

            return HttpResponse("Great!")

        else:
            print(formset.errors)

    else:
        return HttpResponse("POOP")


def reporty(request):
    return HttpResponse("Working on it!")


def index(request):
    return render(request, 'Questionnaires/index.html', {})
