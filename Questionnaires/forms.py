from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field
from django import forms
from django.forms import BaseFormSet
from django_select2 import forms as s2forms
from .models import Choice, Question, Patient, Questionnaire

# formular jednej otázky s odpovedami
class ChoiceForm(forms.Form):
    # nainicializujeme polia s radio buttonmi
    answer = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Choice.objects.none(), )

    def __init__(self, *args, question_id=None, **kwargs, ):
        super().__init__(*args, **kwargs)
        # cez formset sme formularu odovzdali zoznam otazok, zobrazime kazdu z nich a k nej aj moznosti odpovede
        if question_id is not None:
            # vyhladame vsetky moznosti odpovede podla cisla otazky, ktore sme dostali z formsetu
            self.fields['answer'].queryset = Choice.objects.filter(question=question_id)
            # na zaklade id otazky, ktore sme dostali z formsetu vyhladame k danej otazke vsetky informacie
            q = Question.objects.get(pk=question_id)
            # nastavime text otazky na text z databazy
            self.fields['answer'].label = q.text
            # nastavime otazku na required, aby ju zadavatel nemohol preskocit
            self.fields['answer'].required = True
            # pridame volitelny text oddelujuci jednotlive otazky
            self.section_text = q.section_text

            self.helper = FormHelper(self)
            self.helper.form_tag = False
            self.helper.disable_csrf = True

# vytvorime standardny formset
class BaseChoiceFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseChoiceFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            # vypneme atribut html pre form tag vo vygenerovanom HTML
            form.use_required_attribute = True
    # pri inicializacii formsetu vo views.py odovzdame formsetu vsetky otazky daneho formulara
    # tie pomocou nasledovnej funkcionality ulozime do premennej a odovzdame dalej jednotlivym instanciam
    # form objektov daneho formsetu
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        q = kwargs['questions'][index]
        return {'question_id': q}


class NameWidget(s2forms.Select2Widget):
    search_fields = ["first_name__icontains", "last_name__icontains", ]
    queryset = Patient.objects.all()


class PatientForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
                                     widget=NameWidget(attrs={'data-placeholder': "Vyberte pacienta", }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.add_input(Submit('submit', 'Zobraziť'))
        # self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        # self.helper.form_action = 'get_report'


class ExamLookupForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(),
                                     widget=NameWidget(attrs={'data-placeholder': "Vyberte pacienta"}))
    exam_date_start = forms.DateField(required=False,
                                      widget=forms.DateInput(attrs={'type': 'date', 'placeholder': "Od"},
                                                             ))
    exam_date_end = forms.DateField(required=False,
                                    widget=forms.DateInput(attrs={'type': 'date', 'placeholder': "Do"},
                                                           ))
    questionnaire_type = forms.ModelChoiceField(required=False,
                                                queryset=Questionnaire.objects.all(),
                                                empty_label="Vyberte dotaznik")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('patient'),
                    css_class='col-sm-6 col-lg'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('exam_date_start'),
                    css_class='col-sm-6'
                ),
                Div(
                    Field('exam_date_end'),
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('questionnaire_type'),
                    css_class='col'
                ),
                css_class='row'
            ),

        )


class AddPatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'identifier']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': "Krstné meno"}),
            'last_name': forms.TextInput(attrs={'placeholder': "Priezvisko"}),
            'identifier': forms.TextInput(attrs={'placeholder': "Rok narodenia"}),
        }

# upravime niektore vlastnosti formsetu
class ChoiceFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # formularu vygenerovanemu formsetom sa nastavi method="post"
        self.form_method = 'post'
        # pre jednotlive formulare formsetu schovame <form> tag
        self.form_tag = False
        # zmenime rozlozenie radio buttonov kazdeho formulara
        self.layout = Layout(InlineRadios('answer'))


class ReportForm(forms.Form):
    # sem pridame rozne ine veci, napr. id dotaznika, atd.
    patient = forms.ModelChoiceField(queryset=None, label="Pacient")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all()
        self.helper = FormHelper()
        self.helper.form_id = 'reportform'
        self.helper.form_method = 'post'
        self.helper.form_action = 'get_report'
        self.helper.add_input(Submit('submit', 'Zobraziť'))
