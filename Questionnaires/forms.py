from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML
from django import forms
from django.forms import BaseFormSet
from .models import Choice, Question, Patient


class ChoiceForm(forms.Form):
    answer = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Choice.objects.none(), )

    def __init__(self, *args, question_id=None, **kwargs, ):
        super().__init__(*args, **kwargs)
        if question_id is not None:
            self.fields['answer'].queryset = Choice.objects.filter(question=question_id)
            q = Question.objects.get(pk=question_id)
            self.fields['answer'].label = q.text
            self.fields['answer'].required = True
            self.section_text = q.section_text


class BaseChoiceFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseChoiceFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.use_required_attribute = True

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        q = kwargs['questions'][index]
        return {'question_id': q}


class PatientForm(forms.Form):
    id = forms.IntegerField(required=True, label="ID pacienta")


class ChoiceFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.form_tag = False
        # self.layout = Layout((HTML('{% if form.section_text %}šuba duba{% endif %}')))
        self.layout = Layout((HTML('{% if forloop.first %} Only display text on the first iteration... {% endif %}')))
        # Tu by sme teoreticky vedeli urobit moznosti formulara vodorovne.
        # self.layout = Layout(
        #     InlineRadios('answer'))
        # self.form_class = "form-horizontal"
        # self.label_class = "col-lg-2"
        # self.field_class = "col-lg-8"


class ReportForm(forms.Form):
    # sem pridame rozne ine veci, napr. id dotaznika, atd.
    patient = forms.ModelChoiceField(queryset=None, label="Pacient")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all()
        self.helper = FormHelper()
        self.helper.form_id = 'reportform'
        # self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'get_report'
        self.helper.add_input(Submit('submit', 'Submit'))
