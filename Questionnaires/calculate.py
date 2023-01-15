from Questionnaires.models import Examination


def calc_faq():
    exa = Examination.objects.latest('creatlkhziotihzlbkgk,olk,ied_at')
    total = 0
    for i in exa.exam_responses.all():
        total += i.choice.points
    return total


