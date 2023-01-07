from django.shortcuts import render, HttpResponse
from .models import Question, Questionnaire, Response
from django.forms import formset_factory
from .forms import ChoiceForm, BaseChoiceFormSet, PatientForm, ChoiceFormSetHelper


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
            pass
        else:
            print(form.errors)
        qre_id = request.POST['qre_id']
        qs = Question.objects.filter(questionnaire=qre_id).values_list('id', flat=True)
        qaformset = formset_factory(ChoiceForm, formset=BaseChoiceFormSet, extra=len(qs))
        formset = qaformset(request.POST, form_kwargs={'questions': qs})

        if formset.is_valid():
            for form in formset:
                cleanform = form.cleaned_data['answer']
                bup = Response(questionnaire_id=cleanform.question.questionnaire_id,
                               patient_id=1,
                               question_id=cleanform.question.id,
                               answer_id=cleanform.id,
                               examination_id=1,
                               )
                bup.save()
            return HttpResponse("GREAT")
        else:
            print(formset.errors)

    else:
        return HttpResponse("POOP")


def reporty(request):
    return HttpResponse("Working on it!")
