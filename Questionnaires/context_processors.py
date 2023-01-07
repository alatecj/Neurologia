from .models import Questionnaire


def form_processor(request):
    qres = Questionnaire.objects.all()
    return {'qres': qres}
