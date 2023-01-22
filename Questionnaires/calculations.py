from Questionnaires.models import Examination


def calc_faq(exa):
    total = 0
    for i in exa.exam_responses.all():
        total += i.choice.points
    return f"Výsledok vyšetrenia je {total}"


def calc_hads(exa):
    response_dict = {}
    responses = exa.exam_responses.all()
    for response in responses:
        response_dict[response.question.sequence] = response.choice.points
    vseobecne = sum(response_dict.values())
    uzkost = response_dict.pop(2) + response_dict.pop(4) + response_dict.pop(6) + response_dict.pop(8) + response_dict.pop(11) + \
             response_dict.pop(12) + response_dict.pop(14)
    depresia = sum(response_dict.values())
    return f"Všeobecne: {vseobecne}, Úzkosť: {uzkost}, Depresia: {depresia}"

