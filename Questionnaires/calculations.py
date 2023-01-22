from Questionnaires.models import Examination


def calc_faq(exa):
    total = 0
    for i in exa.exam_responses.all():
        total += i.choice.points
    return f"Výsledok vyšetrenia je {total} bodov."


def calc_hads(exa):
    response_dict = {}
    responses = exa.exam_responses.all()
    for response in responses:
        response_dict[response.question.sequence] = response.choice.points
    vseobecne = sum(response_dict.values())
    uzkost = response_dict.pop(2) + response_dict.pop(4) + response_dict.pop(6) + response_dict.pop(8) + \
             response_dict.pop(11) + response_dict.pop(12) + response_dict.pop(14)
    depresia = sum(response_dict.values())
    result = f"Všeobecné výsledky: {vseobecne} "
    if vseobecne <= 7:
        result += "(norma)"
    elif vseobecne >= 11:
        result += "(patológia)"
    else:
        result += "(hraničná hodnota)"
    result += f", úzkosť: {uzkost} "
    if uzkost >= 6:
        result += "(patológia)"
    result += f", depresia: {depresia} "
    if depresia >= 6:
        result += "(patológia)"
    return result


def calc_liverpool(exa):
    response_list = []
    responses = exa.exam_responses.all()
    for response in responses:
        tup = (response.question.eval_sequence, response.choice.points)
        response_list.append(tup)
    response_list = sorted(response_list)
    zavaznost, postiktalny = 0, 0
    for x in range(9):
        zavaznost += response_list.pop(0)[1]
    postiktalny = sum(i[1] for i in response_list)
    result = f"Závažnosť: {zavaznost} bodov, postiktálny stav: {postiktalny} bodov."
    return result
