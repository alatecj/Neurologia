from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from .models import Question, Questionnaire, Response, Patient, Examination
from django.forms import formset_factory
from .forms import ChoiceForm, BaseChoiceFormSet, PatientForm, ChoiceFormSetHelper, ReportForm, AddPatientForm
from django.urls import reverse
from django.contrib import messages
from .calculations import *
from django.contrib.auth import logout, authenticate, login
import datetime


# Create your views here.


def display_questionnaire(request, questionnaire_id):
    form = PatientForm()
    qre_id = Questionnaire.objects.get(pk=questionnaire_id)
    qs = Question.objects.filter(questionnaire=qre_id).values_list('id', flat=True)
    qaformset = formset_factory(ChoiceForm, formset=BaseChoiceFormSet, extra=len(qs))
    formset = qaformset(form_kwargs={'questions': qs})
    helper = ChoiceFormSetHelper()
    return render(request, 'Questionnaires/display_qre.html',
                  {'formset': formset, 'helper': helper, 'qre': qre_id, 'form': form})


def process(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            if not Patient.objects.filter(id=patient.id):
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
            exam = Examination(patient_id=patient.id)
            exam.save()

            for form in formset:
                cleanform = form.cleaned_data['answer']
                bup = Response(questionnaire_id=cleanform.question.questionnaire_id,
                               patient_id=patient.id,
                               question_id=cleanform.question.id,
                               choice_id=cleanform.id,
                               examination=exam,
                               )
                bup.save()
            messages.success(request, "Dotazník zaregistrovaný.")
            return HttpResponseRedirect(reverse('index'))

        else:
            print(formset.errors)

    else:
        return HttpResponse("POOP")


def get_report(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            print("zap")
            exam = Examination.objects.filter(patient=form.cleaned_data['patient'])
            return render(request, 'Questionnaires/get_report.html', {'form': form,
                                                                      'exam': exam})
    else:
        print("zup")
        form = PatientForm()
    return render(request, 'Questionnaires/get_report.html', {
        'form': form
    })


def index(request):
    if request.user.is_authenticated:
        now = datetime.datetime.now()
        last_10_exams = Examination.objects.order_by('-id')[:10]
        context = {'current_time': now, 'exam': last_10_exams}
        return render(request, 'Questionnaires/index.html', context)
    else:
        return render(request, "Questionnaires/login.html")


def show_report(request, exam_id):
    exam = Examination.objects.get(pk=exam_id)
    qre_id = exam.exam_responses.all().first().questionnaire_id
    # TODO tie hardcoded values pre id questionnairov by mohli byt nejake dynamickejsie... (vyhodnocovanie cez json?)
    match qre_id:
        case 1:
            result = calc_faq(exam)
        case 2:
            result = calc_hads(exam)
        case 3:
            result = calc_faq(exam)
        case 4:
            result = calc_liverpool(exam)
        case 5:
            result = calc_sf36(exam)
        case _:
            result = calc_faq(exam)
    # result = calc_faq(exam)
    # result = calc_hads(exam)
    return render(request, 'Questionnaires/show_report.html', {'exam': exam, 'result': result})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def login_view(request):
    print("šuch")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "Questionnaires/login.html", {"message": "Nesprávne meno/heslo."})
    else:
        return render(request, "Questionnaires/login.html")


def add_patient(request):
    if request.method == "POST":
        form = AddPatientForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            new_patient = Patient(name=form.cleaned_data['name'], identifier=form.cleaned_data['identifier'])
            new_patient.save()
            messages.warning(request, 'Pacient pridaný.')
            return HttpResponseRedirect(reverse('index'))

    else:
        form = AddPatientForm()
        return render(request, "Questionnaires/add_patient.html", {'form': form})


def stroop_test(request):
    return render(request, 'Questionnaires/stroop.html')


def stroop_game(request):
    return render(request, 'Questionnaires/stroop_game.html')


def patientview(request):
    form = PatientForm()
    return render(request, 'Questionnaires/patient_view.html', {'form': form})
