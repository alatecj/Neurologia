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
            if Response.objects.exists():
                last_set = Response.objects.latest('created_at').set + 1
            else:
                last_set = 0

            for form in formset:
                cleanform = form.cleaned_data['answer']
                # FIXME funkcionalitu s examinations este treba dorobit a domysliet.
                bup = Response(questionnaire_id=cleanform.question.questionnaire_id,
                               # FIXME patient_id nesmie byt natvrdo!
                               patient_id=1,
                               question_id=cleanform.question.id,
                               choice_id=cleanform.id,
                               set=last_set,
                               examination_id=1,

                               )
                # bup.save()
            last_set_content = Response.objects.filter(set=last_set-1)
            #
            #
            # TU PREBEHNE KALKULACIA, KTORA BY MALA PREBEHNUT INDE
            #
            #
            set_sum = 0
            for i in last_set_content:
                set_sum += i.choice.points
            print(last_set_content)
            # tu si musime pripravit data, ktore ideme vlastne zobrazovat...
            return render(request, 'Questionnaires/show_result.html', {'patient': 1, 'set_sum': set_sum})

        else:
            print(formset.errors)

    else:
        return HttpResponse("POOP")


def reporty(request):
    return HttpResponse("Working on it!")

