from crispy_forms.helper import FormHelper
from django import forms
from django.forms import BaseFormSet
from .models import Choice, Question


class ChoiceForm(forms.Form):
    answer = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Choice.objects.none())

    def __init__(self, *args, question_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if question_id is not None:
            self.fields['answer'].queryset = Choice.objects.filter(question=question_id)
            q = Question.objects.get(pk=question_id)
            self.fields['answer'].label = q.text
            self.fields['answer'].required = True


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
        # Tu by sme teoreticky vedeli urobit moznosti formulara vodorovne.
        # self.layout = Layout(
        #     InlineRadios('answer'))
        # self.form_class = "form-horizontal"
        # self.label_class = "col-lg-2"
        # self.field_class = "col-lg-8"


class ReportForm(forms.Form):
    # sem pridame rozne ine veci, napr. id dotaznika, atd.
    patient_id = forms.IntegerField(required=True, label="ID pacienta")
